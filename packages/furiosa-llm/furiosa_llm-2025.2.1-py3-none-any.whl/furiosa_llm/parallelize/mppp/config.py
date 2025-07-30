from abc import ABC
import dataclasses
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
import json
import os
import re
import typing
from typing import Dict, List, Optional

import torch
from typing_extensions import Self, TypeAlias


class ReduceOp(Enum):
    SUM = "sum"
    AVG = "avg"
    MAX = "max"
    MIN = "min"

    def __repr__(self) -> str:
        return self.value


class Placement(ABC): ...


@dataclass(frozen=True)
class Partial(Placement):
    reduce_op: ReduceOp
    type: str = "partial"

    def __post_init__(self):
        assert self.type == "partial"


@dataclass(frozen=True)
class Shard(Placement):
    dim: int
    type: str = "shard"

    def __post_init__(self):
        assert self.type == "shard"


@dataclass(frozen=True)
class Replicate(Placement):
    type: str = "replicate"

    def __post_init__(self):
        assert self.type == "replicate"


NodeId: TypeAlias = str


class DeviceMesh(List):
    def __post_init__(self):
        try:
            torch.tensor(self, dtype=torch.int)
        except Exception:
            raise ValueError(
                "DeviceMesh must be a n-dimensional int type array with fixed dimension sizes"
            )


@dataclass
class ShardSpec:
    placements: List[Placement]
    mesh: DeviceMesh

    def _to_brief_str(self) -> str:
        return f"({self.placements}, {self.mesh})"


class TensorId(NodeId): ...


NPU_PE_RANGE_IDX_RE = re.compile(r"(\d)-(\d)")
POSSIBLE_FUSION_GRANULARITY = {1, 2, 4, 8}


def _verify_device(device: str) -> None:
    kind, *rest = device.split(":")
    if kind == "cpu":
        if rest and (len(rest) != 1 or not rest[0].isdigit()):
            raise ValueError(f"Invalid device string: {device}")
    elif kind == "rngd":
        # furiosa-torch representation with device index
        if len(rest) != 2 or not rest[0].isdigit() or not rest[1].isdigit():
            raise ValueError(f"Invalid device string: {device}")
        if int(rest[1]) not in POSSIBLE_FUSION_GRANULARITY:
            raise ValueError(f"Invalid num pe: {rest[1]}")
    elif kind == "npu":
        # Example of allowed formats: "npu:0:0", "npu:1:*", "npu:1:0-3", "npu:2".
        if not rest[0].isdigit():
            raise ValueError(f"Invalid npu index: {rest[0]}")

        if len(rest) == 1:
            # npu:1
            return

        if len(rest) != 2:
            raise ValueError(f"Invalid device string: {device}")

        if rest[1].isdigit():
            if int(rest[1]) > 7:
                raise ValueError(f"Invalid pe index: {rest[1]}")
        elif NPU_PE_RANGE_IDX_RE.match(rest[1]):
            start_, end_ = rest[1].split("-")
            start, end = int(start_), int(end_) + 1  # Make end inclusive
            core_range = end - start
            if core_range in POSSIBLE_FUSION_GRANULARITY and end % core_range == 0:
                pass
            else:
                raise ValueError(f"Invalid pe index range: {rest[1]}")
        elif rest[1] == "*":
            pass
        else:
            raise ValueError(f"Invalid device string: {device}")
    else:
        raise ValueError(f"Invalid device string: {device}")


# TODO: move this to furiosa-llm/device.py
class Device(str):

    def __init__(self, val: str):
        _verify_device(val)

    @cached_property
    def kind(self) -> str:
        return self.split(":", maxsplit=1)[0]

    @cached_property
    def idx(self) -> Optional[int]:
        splitted = self.split(":")
        if len(splitted) == 1:
            return None
        elif len(splitted) >= 2:
            return int(splitted[1])
        else:
            raise ValueError(f"Invalid device string: {self}")

    @cached_property
    def pe_idx(self) -> str:
        """Returns pe index of the device.
        Returns one of the two forms: "4-7" (for fusioned one), "2" (for single pe)."""
        kind, *rest = self.split(":")

        if kind != "npu":
            raise ValueError("Only npu devices have pe indexes.")

        if len(rest) == 1 or rest[1] == "*":
            return "0-7"
        elif len(rest) == 2:
            return rest[1]
        else:
            raise ValueError(f"Invalid npu device string: {self}")

    def split_into_single_pes(self) -> List[Self]:
        if self.kind != "npu":
            raise ValueError("Only npu devices can be split into pes.")
        splitted_pe_idx = self.pe_idx.split("-")
        if len(splitted_pe_idx) == 1:
            return [self]
        elif len(splitted_pe_idx) == 2:
            start, end = splitted_pe_idx
            return [type(self)(f"npu:{self.idx}:{i}") for i in range(int(start), int(end) + 1)]
        else:
            raise ValueError(f"Invalid npu device string: {self}")

    def to_torch_device_with_cpu_idx(self) -> torch.device:
        # npu:x:y representation cannot be converted to torch device. So consider it as CPU for now.
        # TODO: fix this to cover all kind of representations for NPU once it's established.
        if self.kind == "npu":
            return torch.device("cpu")
        elif self.kind == "rngd":
            # "rngd:x:y" representation is only for furiosa-torch.
            # When it's converted to torch device, only its first index is used.
            # Fusion information will be passed with environment variable.
            return torch.device(f"rngd:{self.idx}")
        elif self.idx is not None:
            return torch.device(self.kind, self.idx)
        else:
            return torch.device(self.kind)

    def to_torch_device(self) -> torch.device:
        # Ignore device index if kind is "cpu".
        if self.kind == "cpu":
            return torch.device("cpu")
        else:
            return self.to_torch_device_with_cpu_idx()

    @property
    def num_pe(self) -> int:
        if self.kind == "rngd":
            # FIXME: "rngd:x:y" representation is only for furiosa-torch.
            # Two indices (x, y) mean device index and number of fusioned pes respectively.
            return int(self.rsplit(":", maxsplit=1)[-1])
        elif self.kind == "npu":
            return len(self.split_into_single_pes())
        else:
            raise ValueError("num_pe should not be called for non-npu devices.")


@dataclass
class DynamicTensorSpec:
    src: NodeId
    dst: NodeId
    spec: ShardSpec

    def __iter__(self):
        yield self.src
        yield self.dst
        yield self.spec


class MpppConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, torch.Tensor):
            return obj.tolist()
        elif isinstance(obj, ReduceOp):
            return obj.value
        return super().default(obj)


class SerializationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def _dict_to_dataclass(cls, data):
    if isinstance(data, (str, int)):
        return cls(data)
    elif dataclasses.is_dataclass(cls):
        obj = cls(**data)  # type: ignore[assignment]
        type_hints = typing.get_type_hints(cls)
        for f in dataclasses.fields(cls):
            name = f.name
            new_field_obj = _dict_to_dataclass(type_hints[name], getattr(obj, name))
            setattr(obj, name, new_field_obj)
        return obj
    elif isinstance(data, list) and typing.get_origin(cls) is list:
        d_type = typing.get_args(cls)[0]
        return [_dict_to_dataclass(d_type, d) for d in data]
    elif isinstance(data, dict) and typing.get_origin(cls) is dict:
        k_type, v_type = typing.get_args(cls)
        return {
            _dict_to_dataclass(k_type, k): _dict_to_dataclass(v_type, v) for k, v in data.items()
        }
    else:
        try:
            if isinstance(data, dict):
                obj = cls(**data)
            else:
                obj = cls(data)
        except TypeError:
            for subclass in cls.__subclasses__():
                try:
                    obj = subclass(**data)
                    return obj
                except TypeError:
                    pass
            raise SerializationError(f"Cannot deserialize {data} to {cls}")
    return data


class DeviceId(str): ...


@dataclass
class MpppConfig:
    name: str
    devices: Dict[DeviceId, Device]
    static_tensors: Dict[TensorId, ShardSpec]
    dynamic_tensors: List[DynamicTensorSpec]

    @classmethod
    def from_str(cls, val: str) -> "MpppConfig":
        return _dict_to_dataclass(cls, json.loads(val))

    @classmethod
    def load(cls, path: os.PathLike) -> "MpppConfig":
        with open(path, "r") as f:
            return cls.from_str(f.read())

    def to_json(self) -> str:
        return json.dumps(
            dataclasses.asdict(self),
            cls=MpppConfigEncoder,
            indent=4,
            allow_nan=False,
            sort_keys=True,
        )

    def export(self, path: os.PathLike):
        with open(path, "w") as f:
            f.write(self.to_json())
