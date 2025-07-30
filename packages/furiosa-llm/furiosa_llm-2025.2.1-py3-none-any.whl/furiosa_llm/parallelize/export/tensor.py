from dataclasses import dataclass
from enum import Enum
import json
import os
from pathlib import Path
from time import time
from typing import Dict, List, Mapping, Tuple, Union

from safetensors import safe_open
from safetensors.torch import _find_shared_tensors
from safetensors.torch import load as sf_torch_load
from safetensors.torch import save as sf_torch_save
from safetensors.torch import save_file
import torch


def _tensors_with_same_storage_and_length(tensor1: torch.Tensor, tensor2: torch.Tensor) -> bool:
    return (
        tensor1.data_ptr() == tensor2.data_ptr()
        and tensor1.nelement() == tensor2.nelement()
        and tensor1.dtype == tensor2.dtype
    )


def _preprocess_for_safetensors(
    tensors: Mapping[str, torch.Tensor],
) -> Tuple[Dict[str, torch.Tensor], Dict[str, str]]:
    tensors_ = dict(tensors)

    # This is needed because `_find_shared_tensors` calls `view(-1)` to get tensor's address range.
    # TODO: find way to check overlapping tensors without making it contiguous.
    for name, tensor in tensors_.items():
        try:
            tensor.view(-1)
        except RuntimeError:
            tensors_[name] = tensor.contiguous()

    shared_pointers = _find_shared_tensors(tensors_)

    # This is a workaround for shared tensors in model dict. (`Link shared tensor <https://huggingface.co/docs/safetensors/en/torch_shared_tensors>`_).
    # ``save_model`` API can save shared tensors, but individual shared tensor cannot be loaded from it because only one of shared tensors
    # covering the entire buffer are stored. Even if there is a mapping between excluded tensors to stored one, this is not
    # sufficient because it doesn't include which part of the stored one is excluded one. So, we now restrict all shared tensors to have
    # exactly same data ptr and length, and this can cover most of the cases we are interested in.
    metadata = {}

    for names in shared_pointers:
        if len(names) > 1:
            names_ = list(names)
            # To enforce same representative tensor across executions.
            names_.sort()
            for name in names_[1:]:
                # TODO: find a way to handle shared tensors that are not exactly same.
                if not _tensors_with_same_storage_and_length(tensors[name], tensors[names_[0]]):
                    raise RuntimeError(
                        "Shared tensors that are not exactly same cannot be saved right now"
                    )
                # save mapping info for excluded one to stored one.
                metadata[name] = names_[0]
                del tensors_[name]

    # Make all tensors contiguous before saving.
    return {k: v.contiguous() for k, v in tensors_.items()}, metadata


class ParamfileFormat(str, Enum):
    SAFETENSORS = "safetensors"
    TORCHSAVE = "torch.save"
    TORCHEXPORT = "torch.export"


def serialize_tensors(
    tensors: Mapping[str, torch.Tensor],
    format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
) -> bytes:
    if format is ParamfileFormat.SAFETENSORS:
        # Safetensors doesn't provide function for deserializing metadata with tensors.
        # So we just tensors with same storages duplicately. For efficient saving without duplication, use save_tensors.

        # tensors, metadata = _preprocess_for_safetensors(tensors)
        return sf_torch_save({k: v.contiguous() for k, v in tensors.items()})
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")


def deserialize_tensors(
    data: bytes,
    format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
) -> Dict[str, torch.Tensor]:
    if format is ParamfileFormat.SAFETENSORS:
        return sf_torch_load(data)
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")


def save_tensors(
    tensors: Mapping[str, torch.Tensor],
    path: Union[str, os.PathLike],
    format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
) -> None:
    if format is ParamfileFormat.SAFETENSORS:
        tensors, metadata = _preprocess_for_safetensors(tensors)
        save_file(dict(tensors), path, metadata)
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")


def write_without_concurrency_issue(
    data: Union[str, bytes, Dict[str, torch.Tensor]],
    path: Union[str, os.PathLike],
    tensor_save_format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
) -> None:
    path = Path(path)
    # Write to temp file and move it when it's done.
    while True:
        try:
            tmp_filename = f"{path.name}-{time()}.tmp"
            if isinstance(data, str):
                with open(path.parent / tmp_filename, "x") as f:
                    f.write(data)
            elif isinstance(data, bytes):
                with open(path.parent / tmp_filename, "xb") as f:
                    f.write(data)
            else:
                save_tensors(data, path.parent / tmp_filename, tensor_save_format)
            break
        except FileExistsError:
            # Other process might tries to save to same tmp file. In this case, try again with other time suffix.
            pass
    os.replace(path.parent / tmp_filename, path)


def save_model(
    model: torch.nn.Module,
    path: Union[str, os.PathLike],
    format: str = "safetensors",
):
    if format == "safetensors":
        # FIXME: Use Union operator '|' after Python 3.8 deprecation
        merged_tensors = {**model.state_dict(), **dict(model.named_buffers())}
        write_without_concurrency_issue(merged_tensors, path)
    else:
        raise ValueError(f"Invalid param save format {format}")


def load_tensors(
    path: os.PathLike, format: ParamfileFormat = ParamfileFormat.SAFETENSORS
) -> Mapping[str, torch.Tensor]:
    tensors: Dict[str, torch.Tensor] = {}

    if format == ParamfileFormat.SAFETENSORS:
        # The example shows safe_open with 'with clause'; https://huggingface.co/docs/safetensors/index
        # It still causes 'error: "safe_open" has no attribute "__enter__"'. Why? for workaround, ignore it.
        with safe_open(path, framework="pt", device="cpu") as f:  # type: ignore
            for key in f.keys():
                tensors[key] = f.get_tensor(key)
        return tensors
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")


def get_tensor_with_safetensors_fp(f, tensor_name: str) -> torch.Tensor:
    if metadata := f.metadata():
        tensor_name = metadata.get(tensor_name, tensor_name)
    return f.get_tensor(tensor_name)


@dataclass
class ParamFileInfo:
    path: str
    format: ParamfileFormat

    def __hash__(self):
        return hash(json.dumps({"path": self.path, "format": self.format}))


def get_saved_param_names(param_info: ParamFileInfo) -> List[str]:
    if param_info.format == ParamfileFormat.SAFETENSORS:
        with safe_open(param_info.path, framework="pt", device="cpu") as f:  # type: ignore
            keys = list(f.keys())
            if metadata := f.metadata():
                keys += list(metadata.keys())
            return keys
    else:
        raise NotImplementedError(f"param saved format {param_info.format} is not supported yet")
