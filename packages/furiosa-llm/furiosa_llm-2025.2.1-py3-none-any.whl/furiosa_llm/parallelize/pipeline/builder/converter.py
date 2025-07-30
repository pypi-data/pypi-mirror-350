from collections import defaultdict
import copy
from functools import reduce
from hashlib import blake2b
from itertools import chain
import logging
import operator
import os
from time import time
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

from furiosa_torch_ext.torch_ext import preprocess
from safetensors import safe_open
import torch
from torch._guards import detect_fake_mode
from torch._subclasses.fake_tensor import FakeTensor, FakeTensorMode
from torch.func import functionalize
from torch.fx import GraphModule, Node
from torch.fx.experimental.proxy_tensor import make_fx
from torch.fx.passes.shape_prop import TensorMetadata

from furiosa_llm.parallelize.compiler_config import BlockType, CompilerConfigContext
from furiosa_llm.parallelize.export.graphmodule import serialize_gm
from furiosa_llm.parallelize.export.tensor import (
    ParamfileFormat,
    ParamFileInfo,
    get_saved_param_names,
    save_tensors,
)
from furiosa_llm.parallelize.hash import (
    hash_fx_graph,
    hash_fx_graph_excluding_num_paged_attention_blocks,
    hash_tensor,
)
import furiosa_llm.parallelize.model_rewriter.mppp_config as mrw
from furiosa_llm.parallelize.model_rewriter.mppp_config import Device, ShardSpec
from furiosa_llm.parallelize.model_rewriter.ops.types import SingleDeviceCommOp
from furiosa_llm.parallelize.model_rewriter.ops.utils import is_single_dev_comm_op
from furiosa_llm.parallelize.node_meta import (
    ConstantKind,
    get_constant_kind,
    get_device_id,
    get_gm_hash,
    get_original_name,
    get_spec,
    get_unsharded_tensor_meta,
    has_original_name,
    set_device_id,
    set_gm_hash,
    set_original_name,
    set_spec,
    set_to_be_embedded,
    set_to_be_input,
    should_be_embedded,
    should_be_input,
)
from furiosa_llm.parallelize.pipeline.builder.single_device_comm_op_converter import (
    convert_to_single_device_comm_ops,
)
from furiosa_llm.parallelize.pipeline.builder.transform import partition_gm
from furiosa_llm.parallelize.pipeline.builder.utils import get_tensor_name, is_getitem
from furiosa_llm.parallelize.pipeline.types import (
    CommSuperTask,
    CompSuperTask,
    DataBlobId,
    DeviceId,
    InOutputSuperTask,
    MetaData,
    MetadataTensor,
    MetadataTensors,
    MetadataTensorSlice,
    MetadataTensorSlices,
    NameAfterMakeFx,
    ParamFileId,
    ParamInfo,
    ParamValue,
    Pipeline,
    Placements,
    SuperTask,
    SuperTaskId,
    SuperTaskKind,
    TensorInfo,
    TensorInfoWithPlacement,
)
from furiosa_llm.parallelize.utils import (
    get_fake_mode,
    propagate_shape_info_without_real_computation,
    zip_equal,
)
from furiosa_llm.parallelize.visualize import draw_graph
from furiosa_llm.utils import get_logger_with_tz

logger = get_logger_with_tz(logging.getLogger(__name__))

SUBMOD_PREFIX = "submod"
DEFAULT_PARAM_FILE_ID = ParamFileId("0")
ADDITIONAL_PARAM_FILE_ID = ParamFileId("1")

MAX_EMBEDDABLE_CONSTANT_SIZE = 1024  # 1KB

DTYPE_TO_SIZE = {
    torch.float16: 2,
    torch.float32: 4,
    torch.int32: 4,
    torch.float: 4,
    torch.float64: 4,
    torch.double: 8,
    torch.bfloat16: 2,
    torch.half: 2,
    torch.uint8: 1,
    torch.int8: 1,
    torch.int16: 2,
    torch.short: 2,
    torch.int32: 4,
    torch.int: 4,
    torch.int64: 8,
    torch.long: 8,
    torch.bool: 1,
}

_is_comm_supertask = is_single_dev_comm_op

COMPILED_CACHE_SUB_DIR = "compiled_graphs"


def _is_comp_supertask(node):
    return node.op == "call_module" and node.name.startswith(SUBMOD_PREFIX)


def _tensor_exists_in_file(tensor_name: str, param_file_info: ParamFileInfo) -> bool:
    file_format = param_file_info.format
    if file_format == ParamfileFormat.SAFETENSORS:
        # The example shows safe_open with 'with clause'; https://huggingface.co/docs/safetensors/index
        # It still causes 'error: "safe_open" has no attribute "__enter__"'. Why? for workaround, ignore it.
        with safe_open(param_file_info.path, framework="pt", device="cpu") as f:  # type: ignore
            # If this is a shared tensor, get actually stored tensor's name.
            if metadata := f.metadata():
                tensor_name = metadata.get(tensor_name, tensor_name)
            return tensor_name in f.keys()
    else:
        raise NotImplementedError(f"file format {file_format} is not supported")


class InOutputTensorInfo(TensorInfoWithPlacement):
    original_name: str
    idx: int
    device: DeviceId
    kind: str  # either "input" or "output"

    def __init__(
        self,
        tensor_info: TensorInfoWithPlacement,
        original_name: str,
        idx: int,
        device_id: DeviceId,
        kind: str,
    ):
        super().__init__(tensor_info.shape, tensor_info.dtype, tensor_info.placements)
        self.original_name = original_name
        self.idx = idx
        self.device_id = device_id
        assert kind in ("input", "output")
        self.kind = kind


def _propagate_device_id(gm: GraphModule):
    """Propagate meta["device_id"]"""
    for node in gm.graph.nodes:
        if node.op in ("placeholder", "get_attr"):
            assert "device_id" in node.meta
            continue
        elif node.op == "output":
            continue
        else:
            if len(node.args) == 0:
                assert "device_id" in node.meta
                continue
            # propagate device_id
            device_id = get_device_id(node.args[0])
            assert all(
                device_id == get_device_id(arg) for arg in node.args if isinstance(arg, Node)
            )
            set_device_id(node, device_id)


def _get_saved_name(param_file_info: ParamFileInfo, tensor_name: str) -> str:
    """This is for shared tensors, one of which is stored in parameter file."""
    if param_file_info.format == ParamfileFormat.SAFETENSORS:
        with safe_open(param_file_info.path, framework="pt", device="cpu") as f:  # type: ignore
            if metadata := f.metadata():
                tensor_name = metadata.get(tensor_name, tensor_name)
            return tensor_name
    else:
        raise NotImplementedError("Only SAFETENSORS format is supported currently")


def _node_to_be_embedded(node: Node, actual_tensor: torch.Tensor) -> bool:
    if should_be_embedded(node):
        return True
    elif should_be_input(node):
        return False
    else:
        # If not marked, only embed constants with size of smaller than or equal to ``MAX_EMBEDDABLE_CONSTANT_SIZE``.
        return _get_tensor_size(actual_tensor) <= MAX_EMBEDDABLE_CONSTANT_SIZE


def _maybe_embed_attr_node(node: Node, gm: GraphModule) -> None:
    if node.op != "get_attr":
        return

    attr_name = node.target
    assert isinstance(attr_name, str)
    actual_tensor = getattr(gm, attr_name)

    if not _node_to_be_embedded(node, actual_tensor):
        return

    # Actual tensor should not be fake tensor.
    if isinstance(actual_tensor, FakeTensor):
        raise ValueError("All get_attr nodes without original name should not be fake tensor")

    if any(not _is_comp_supertask(user) for user in node.users):
        # If any non-comp-supertask user exists, this node cannot be embedded.
        assert not should_be_embedded(node)
        return

    # Embed attr node into submodule. The node will exist as a constant embedded in the sub-GraphModule,
    # instead of being exposed as an input.
    for user in tuple(node.users):
        # All users are sub GraphModule nodes.
        assert _is_comp_supertask(user)

        # Do we need to relax this assumption?
        assert isinstance(user, Node)
        assert user.op == "call_module" and isinstance(user.target, str)
        submod = getattr(gm, user.target)
        assert isinstance(submod, GraphModule)

        assert not hasattr(submod, attr_name)

        # Find first non placeholder node in sub GraphModule, so that
        # we can insert get_attr node before it.
        input_idx = user.args.index(node)
        original_placeholder = tuple(submod.graph.nodes)[input_idx]
        first_non_placeholder_node = tuple(submod.graph.nodes)[len(user.args)]
        assert first_non_placeholder_node.op != "placeholder"

        # create get_attr node inside sub GraphModule and replace placeholder node with it.
        if isinstance(actual_tensor, torch.nn.Parameter):
            submod.register_parameter(attr_name, actual_tensor)
        else:
            assert isinstance(actual_tensor, torch.Tensor)
            submod.register_buffer(attr_name, actual_tensor)

        with submod.graph.inserting_before(first_non_placeholder_node):
            new_node = submod.graph.get_attr(attr_name)
        new_node.meta = original_placeholder.meta.copy()

        original_placeholder.replace_all_uses_with(new_node)
        submod.graph.erase_node(original_placeholder)

        # change submod node (in global graph)'s args
        user.args = tuple(arg for arg in user.args if arg != node)
        submod.recompile()
    gm.graph.erase_node(node)


def _get_tensor_size(tensor: torch.Tensor) -> int:
    """Get size of the tensor in bytes. This function calculates size with just shape and dtype (i.e., doesn't consider actual physical size)."""
    return reduce(operator.mul, tensor.size(), DTYPE_TO_SIZE[tensor.dtype])


def _is_not_constant_node(node: Node) -> bool:
    if node.op == "get_attr":
        return False
    elif node.op == "placeholder":
        return True
    elif is_getitem(node):
        return any(_is_not_constant_node(arg) for arg in node.args if isinstance(arg, Node))
    else:
        return True


def _get_hash_for_get_attr_node(node: Node, gm: GraphModule) -> str:
    if get_constant_kind(node) is ConstantKind.WEIGHT:
        # Don't hash weight parameters and just consider them as unique ones for performance reason.
        return str(hash(get_original_name(node)))
    else:
        return hash_tensor(getattr(gm, cast(str, node.target)))


def _mark_not_repeating_constants_for_blocks_to_be_input(gm: GraphModule):
    """Mark not repeating constant tensors (get_attr nodes) for blocks (i.e., not all corresponding constants for blocks are not same) to be inputs of each block (sub GraphModule)"""

    hash_to_subgms: MutableMapping[str, List[Tuple[Node, GraphModule]]] = defaultdict(list)

    # Group submodules by hash value.
    for node in gm.graph.nodes:
        if not _is_comp_supertask(node):
            continue
        sub_gm = getattr(gm, node.target)
        hash_ = get_gm_hash(node)
        if hash_ is None:
            continue

        # Append tuple of call_module node for the submodule and submodule's GraphModule.
        hash_to_subgms[hash_].append((node, sub_gm))

    # Let's call call_module node in global fx graph as "call_submod_node",
    # and call_submod_node's arg nodes in global fx graph as "submod_input_node".
    for subgms in hash_to_subgms.values():
        if len(subgms) == 1:
            # This submodule is not a repeated one.
            continue

        num_submod_inputs = len(subgms[0][0].args)
        assert all(len(submod_info[0].args) == num_submod_inputs for submod_info in subgms)

        for input_idx in range(num_submod_inputs):
            submod_input_nodes: List[Node] = [
                cast(Node, call_submod_node.args[input_idx]) for call_submod_node, _ in subgms
            ]
            assert all(isinstance(node, Node) for node in submod_input_nodes)

            # If this submod_input_node is not a constant (i.e., other submod's output), we don't do anything.
            if any(
                _is_not_constant_node(submod_input_node) for submod_input_node in submod_input_nodes
            ):
                # If any of submod_input node is not a constant, it's impossible to embed it (because value for each submodule can be different.).
                assert all(
                    not set_to_be_embedded(submod_input_node)
                    for submod_input_node in submod_input_nodes
                    if not _is_not_constant_node(submod_input_node)
                )
                continue

            assert all(
                isinstance(submod_input_node, Node) and submod_input_node.op == "get_attr"
                for submod_input_node in submod_input_nodes
            )

            # Input constants for submodules.
            constant_inputs = [
                getattr(gm, cast(str, submod_input_node.target))
                for submod_input_node in submod_input_nodes
            ]
            constant_tensor_hashes = set(
                _get_hash_for_get_attr_node(submod_input_node, gm)
                for submod_input_node in submod_input_nodes
            )

            if len(constant_tensor_hashes) > 1:
                # Input constant value is not same for all repeating submodules.
                # we should make it as an input.
                logger.debug(
                    f"Not Embedding constant tensor {submod_input_nodes} into submodules, shape: {constant_inputs[0].shape}"
                )
                for sub_gm, input_constant_node in zip_equal(subgms, submod_input_nodes):
                    assert isinstance(input_constant_node, Node)
                    assert not should_be_embedded(
                        input_constant_node
                    ), f"node {input_constant_node} was marked to be embedded, but needed to be made as an input for blockwise compile."
                    set_to_be_input(input_constant_node)


def _add_hash_for_sub_gms(gm: GraphModule, include_gm_name: bool):
    for node in gm.graph.nodes:
        if not _is_comp_supertask(node):
            continue
        assert node.name.startswith(SUBMOD_PREFIX)
        sub_gm = getattr(gm, node.target)

        submod_input_node_tensor_metas = [arg.meta["tensor_meta"] for arg in node.args]

        # Fill tensor meta info for placeholder nodes in sub GraphModule. This is needed for FX graph hashing.
        for input_node, tensor_meta in zip(sub_gm.graph.nodes, submod_input_node_tensor_metas):
            assert input_node.op == "placeholder"
            input_node.meta["tensor_meta"] = tensor_meta

        # TODO: change `include_tensor_stride_info` option to True after graphmodule exporter
        # to restore stride info across gm save and load. Currently, all constant tensors become
        # contiguous in the process of saving GraphModule for caching, might losing its original
        # stride. To make hash value and blob id consistent whether or not cached graphmodule is used,
        # we do not include stride information now.
        hash_ = hash_fx_graph(sub_gm, include_tensor_stride_info=False)
        if include_gm_name:
            hash_ = blake2b(str((hash_, node.name)).encode("ascii")).hexdigest()
        set_gm_hash(node, hash_)


class GraphModuleConverter:
    """Convert rewritten GraphModule to Pipeline"""

    tensors: Dict[NameAfterMakeFx, Union[TensorInfo, ParamInfo, InOutputTensorInfo]]
    supertasks: Dict[SuperTaskId, SuperTask]

    def __init__(
        self,
        model: GraphModule,
        devices: Mapping[DeviceId, Device],
        device_id_map: Mapping[mrw.DeviceId, DeviceId],
    ):
        self.model = model

        self.tensors = {}
        self.supertasks = {}

        self.devices = dict(devices)
        self.device_id_map = device_id_map

        self._next_supertask_id = 0

        self._unsharded_shape_per_input: Dict[str, Tuple[int, ...]] = {}
        self._unsharded_shape_per_output: Dict[str, Tuple[int, ...]] = {}

        self.data_blobs: Dict[DataBlobId, str] = {}
        self._next_blob_id = 0

        self._gm_hash_to_data_blob_id: Dict[str, DataBlobId] = {}

    def convert(
        self,
        pipeline_name: str,
        param_file_info: Optional[ParamFileInfo],
        comp_supertask_kind: SuperTaskKind,
        # current context: model_qname, beam_size, phase, bucket
        compiler_config_context: CompilerConfigContext,
        one_supertask_per_device: bool,
        additional_param_file_info: Optional[ParamFileInfo],
        original_model_params: Dict[str, torch.Tensor],
        use_color_for_partitioning: bool,
        embed_all_constants_into_graph: bool,
        cache_dir: Optional[os.PathLike] = None,
    ) -> Pipeline:
        """Convert ``self.model`` into ``Pipeline``"""
        fake_mode = get_fake_mode((*self.model.parameters(), *self.model.buffers()))

        # Generate fake arg tensors used for tracing.
        # Intentionally ignore cpu index via self._get_torch_device() to ensure created fake tensors are on exactly same device as constants (real tensors) in the model.
        # Real tensors loses cpu index information when it's created, but fake tensors preserve it. And when two kind of tensors created
        # with same torch cpu device with index (e.g., "cpu:1") are used together as inputs of certain operator, the operator fails to run
        # because two devices (cpu device without index and cpu device with index) are regarded as different ones by FakeTensor operators.
        # This doesn't affect GraphModule conversion process because this fake args are used only for Shape Propagation and derived device info
        # is not used.
        def _get_unsharded_tensor_meta(node: Node) -> TensorMetadata:
            tensor_meta = get_unsharded_tensor_meta(node)
            if not isinstance(tensor_meta, TensorMetadata):
                raise ValueError(
                    f"Expect all placeholder nodes are single tensor, but {node} is not."
                )
            return tensor_meta

        example_fake_args = tuple(
            GraphModuleConverter._get_fake_slice(
                _get_unsharded_tensor_meta(node),
                cast(ShardSpec, get_spec(node)),
                device=self._get_torch_device(node),
                fake_mode=fake_mode,
            )
            for node in self.model.graph.nodes
            if node.op == "placeholder"
        )

        self.pipeline_name = pipeline_name

        # transform rewritten fx graph
        self.model = GraphModuleConverter._transform_gm(
            self.model,
            example_fake_args,
            one_supertask_per_device,
            use_color_for_partitioning,
            embed_all_constants_into_graph,
        )

        param_files = {}

        params_to_be_saved = self._get_additional_params_to_save(param_file_info)

        if params_to_be_saved:
            if not additional_param_file_info:
                raise ValueError(
                    "There's additional parameters to save, but `additional_param_file_info` is not given."
                )
            save_tensors(
                {
                    param_name: original_model_params[param_name]
                    for param_name in params_to_be_saved
                },
                additional_param_file_info.path,
                additional_param_file_info.format,
            )
            param_files[ADDITIONAL_PARAM_FILE_ID] = additional_param_file_info

        if param_file_info:
            param_files[DEFAULT_PARAM_FILE_ID] = param_file_info

        logger.info("Add tensors and supertasks")
        start = time()
        self._add_tensors(param_files)
        self._add_supertasks(comp_supertask_kind, compiler_config_context, cache_dir)
        logger.info("Add tensors and supertasks took %.2f seconds", time() - start)

        self.metadata = self._construct_metadata()

        # convert ``InOutputTensorInfo`` to ``TensorInfo``
        def convert_to_tensor_info(info) -> TensorInfo:
            return (
                TensorInfo(info.shape, info.dtype) if isinstance(info, InOutputTensorInfo) else info
            )

        self.tensors = {name: convert_to_tensor_info(info) for name, info in self.tensors.items()}

        return Pipeline(
            name=pipeline_name,
            devices=dict(self.devices),
            tensors=self.tensors,
            supertasks=cast(
                Dict[SuperTaskId, Union[InOutputSuperTask, CompSuperTask, CommSuperTask]],
                self.supertasks,
            ),
            metadata=self.metadata,
            blobs=self.data_blobs,
            param_files=param_files,
            # TODO: add proper device constraints after implementing interface for it.
            device_constraints=[],
        )

    def _get_additional_params_to_save(
        self,
        param_file_info: Optional[ParamFileInfo],
    ) -> Set[str]:
        if param_file_info:
            saved_param_names = set(get_saved_param_names(param_file_info))
        else:
            saved_param_names = set()

        # Save params that are not in ``param_file``, but in the model.
        return set(
            get_original_name(node)
            for node in self.model.graph.nodes
            if node.op == "get_attr" and get_original_name(node) not in saved_param_names
        )

    @staticmethod
    def _transform_gm(
        gm: GraphModule,
        example_args: Sequence,
        one_supertask_per_device: bool,
        use_color_for_partitioning: bool,
        embed_all_constants_into_graph: bool,
    ) -> GraphModule:
        # Propagate shape info. This information is needed for
        # single device communication op conversion.
        # TODO: remove this after fix model rewriter to add tensor meta info for all newly created nodes.
        logger.info("Propagating shape info for fx graph")
        start = time()

        propagate_shape_info_without_real_computation(gm, example_args)

        logger.info("Propagating shape info took %.2f seconds", time() - start)

        # Convert multi-device comm ops to single device comm ops.
        convert_to_single_device_comm_ops(gm)
        draw_graph(gm, "stage4")

        # Cluster adjacent computation nodes that runs on same device without communication operation.
        # Computation nodes are grouped into multiple call_module nodes, each of which exactly corresponds to single ``SuperTask``.
        logger.info("Partitioning GraphModule into sub GraphModules")
        start = time()
        gm = partition_gm(gm, SUBMOD_PREFIX, one_supertask_per_device, use_color_for_partitioning)
        logger.info("Partitioning GraphModule took %.2f seconds", time() - start)

        _propagate_device_id(gm)

        # Add hash value for each sub GraphModule.
        _add_hash_for_sub_gms(gm, embed_all_constants_into_graph)

        draw_graph(gm, "stage5")

        start = time()
        # Embed some get_attr nodes into sub``GraphModule``s according to each node's marked state.
        GraphModuleConverter._embed_get_attr_nodes_into_submodules(
            gm, use_color_for_partitioning, embed_all_constants_into_graph
        )

        draw_graph(gm, "stage6")

        return gm

    @staticmethod
    def _embed_get_attr_nodes_into_submodules(
        gm: GraphModule, use_colors_for_partitioning: bool, embed_all: bool
    ):
        """Embed get_attr nodes according to their marked constant embedding policies.

        This function determines whether each get_attr node should be embedded or not with the following rules:
        * If node is marked to be embedded (using ``set_to_be_embedded``), then it will be embedded into submodules as constant.
        * If node is marked to be an input (using ``set_to_be_input``), then it will be an input (placeholder node) of submodules.
        * Otherwise (not marked), make it as an input only if the size of constant tensor that the node refers to is greater than ``MAX_EMBEDDABLE_CONSTANT_SIZE``.

        If ``use_colors_for_partitioning=True``, set of constants that are in same position in each colored subgraph but have different values will be
            marked to be inputs. get_attr nodes referring to these constants should have not been marked to be embedded.
            For set of constants that are in same position in each colored subgraph and have same value will follow the above rules.
        """
        if embed_all:
            for node in gm.graph.nodes:
                if node.op != "get_attr":
                    continue
                set_to_be_embedded(node)
        else:
            if use_colors_for_partitioning:
                start = time()
                _mark_not_repeating_constants_for_blocks_to_be_input(gm)
                logger.info(
                    "Marking not repeating constants for blocks takes %.2f seconds", time() - start
                )

        for node in gm.graph.nodes:
            _maybe_embed_attr_node(node, gm)

        gm.recompile()

    def _construct_metadata(self) -> MetaData:
        unsharded_tensors = MetadataTensors({}, {})
        tensor_slices = MetadataTensorSlices({}, {})

        for name, tensor_slice_info in self.tensors.items():
            # we only care about input/output tensors
            if not isinstance(tensor_slice_info, InOutputTensorInfo):
                continue
            original_name = tensor_slice_info.original_name

            sliced_tensor_meta = MetadataTensorSlice(
                placements=tensor_slice_info.placements,
                origin=original_name,
                dtype=tensor_slice_info.dtype,
                device=tensor_slice_info.device_id,
            )
            assert tensor_slice_info.kind in ("input", "output")
            kind = tensor_slice_info.kind + "s"

            getattr(tensor_slices, kind)[name] = sliced_tensor_meta
            tensors = getattr(unsharded_tensors, kind)

            if original_name not in tensors:
                unsharded_shape = (
                    self._unsharded_shape_per_input[original_name]
                    if tensor_slice_info.kind == "input"
                    else self._unsharded_shape_per_output[original_name]
                )

                # if there's no original tensor info, generate  it.
                tensors[original_name] = MetadataTensor(
                    shape=list(unsharded_shape),
                    dtype=tensor_slice_info.dtype,
                    idx=tensor_slice_info.idx,
                )
        return MetaData(unsharded_tensors, tensor_slices)

    def _add_supertasks(
        self,
        comp_supertask_kind: SuperTaskKind,
        # current context: model_qname, beam_size, phase, bucket
        compiler_config_context: CompilerConfigContext,
        cache_dir: Optional[os.PathLike],
    ):
        self._add_input_supertask(self.model)
        self._add_output_supertask(self.model)

        # Add normal (comm/comp) supertasks.
        # To guarantee consistent supertask order for the same graph, create supertasks in the order of node name.
        # Node names are in the form of "submod_0", "submod_d0_b3", "submod_d0"
        def _get_supertask_key(node: Node):
            ret = []
            for id_ in node.name.split("_")[1:]:
                if not id_[0].isdigit():
                    ret.append(int(id_[1:]))
                else:
                    ret.append(int(id_))
            return ret

        self.model.graph.lint()

        # Sort nodes by device that it runs on first, and sort by topological order among nodes on same devices.
        for _, node in sorted(
            (
                (i, node)
                for i, node in enumerate(self.model.graph.nodes)
                if _is_comm_supertask(node) or _is_comp_supertask(node)
            ),
            key=lambda x: (get_device_id(x[1]), x[0]),
        ):
            supertask = self._get_supertask_from_node(
                node, comp_supertask_kind, compiler_config_context, cache_dir
            )
            self._add_new_supertask(supertask)

    @staticmethod
    def compile_gm_and_get_preprocessed_gm_hash(
        gm: GraphModule,
        example_input: Sequence,
        target_npu: str,
        target_ir: str,
        compiler_config: Optional[Mapping],
        dump_path: Optional[str],
        cache_dir: Optional[os.PathLike],
    ) -> Tuple[Any, str]:
        try:
            from furiosa.native_compiler import compile  # type: ignore[import]
        except ImportError:
            logger.error(
                "furiosa-native-compiler is required to compile GraphModule into DFG/EDF format"
            )
            raise

        gm = preprocess(gm, example_input)
        hash_after_preprocess = hash_fx_graph_excluding_num_paged_attention_blocks(gm)

        try:
            if os.environ.get("ENFORCE_DFG_COMPILE") == "1":
                target_ir = "dfg"
                logger.info("Enforced DFG compilation method invoked; returning compiled DFG")
            compiled = compile(
                gm,
                example_input,
                target_ir=target_ir,
                config=compiler_config,
                skip_trace=True,
                skip_preprocess=True,
                target_npu=target_npu,  # FIXME: it should be given according to super task
                only_cpu_tasks=False,
                dump_path=dump_path,
                dump_tag=hash_after_preprocess,
                cache_dir=f"{cache_dir}/{COMPILED_CACHE_SUB_DIR}",
            )
            return compiled, hash_after_preprocess
        except Exception as e:
            raise RuntimeError(f"Compilation failed with error {e}")

    @staticmethod
    def get_target_npu_from_device(device: Device) -> str:
        dev_kind, *rest = device.split(":")
        if dev_kind not in ("npu", "rngd"):
            raise ValueError("target ir is dfg or edf, but device kind is not npu or rngd")

        if len(rest) != 2:
            raise ValueError(f"Invalid device string: {device}")

        if dev_kind == "rngd":
            num_pe = device.num_pe
            if num_pe == 1:
                return "renegade"
            else:
                return f"renegade-{num_pe}pe"

        index_info = rest[-1].split("-")

        # npu device can be "npu:1:0", "npu:0:0-3", "npu:2:2-3"
        if len(index_info) == 1:
            # single pe
            if not index_info[0].isdigit():
                raise ValueError(f"Invalid device string: {device}")
            target_npu = "renegade"
        elif len(index_info) == 2:
            # fusioned pe
            start, end = index_info
            num_pes = int(end) - int(start) + 1
            if num_pes < 2:
                raise ValueError(f"Invalid device string: {device}")
            target_npu = f"renegade-{num_pes}pe"
        else:
            raise ValueError(f"Invalid device string: {device}")
        return target_npu

    def _next_data_blob_id(
        self,
    ) -> DataBlobId:
        self._next_blob_id += 1
        ret = DataBlobId(str(self._next_blob_id - 1))
        assert ret not in self.data_blobs
        return ret

    def _get_data_blob_id(
        self,
        node: Node,
        comp_supertask_kind: SuperTaskKind,
        # current context: model_qname, beam_size, phase, bucket
        compiler_config_context: CompilerConfigContext,
        cache_dir: Optional[os.PathLike] = None,
    ) -> DataBlobId:
        if gm_hash := get_gm_hash(node):
            blob_id = self._gm_hash_to_data_blob_id.get(gm_hash, DataBlobId(gm_hash))
        else:
            blob_id = self._next_data_blob_id()

        if blob_id in self.data_blobs:
            return blob_id

        # Dump an intermediate artifact (e.g., DFG, ir graphs, dot graphs) for debugging purpose
        dump_path = os.getenv("FURIOSA_COMPILE_DUMP_PATH")

        device_id = self._get_device_id(node)
        assert isinstance(node.target, str)
        submod = getattr(self.model, node.target)
        assert all(isinstance(arg, Node) for arg in node.args)
        tensor_metas = (arg.meta["tensor_meta"] for arg in node.args)  # type: ignore
        fake_mode = detect_fake_mode() or FakeTensorMode(allow_non_fake_inputs=True)
        with fake_mode:
            example_input = tuple(
                torch.zeros(
                    tensor_meta.shape,
                    dtype=tensor_meta.dtype,
                    device=self.devices[device_id].to_torch_device(),
                )
                for tensor_meta in tensor_metas
            )
        if comp_supertask_kind == SuperTaskKind.FX:
            # preprocess submod GraphModule for serialization.
            submod = GraphModuleConverter._preprocess_gm_for_serialization(submod, node)
            data = serialize_gm(submod)
        elif comp_supertask_kind in (SuperTaskKind.DFG, SuperTaskKind.EDF):
            # IMPORTANT: Compiler config generation part part in this function must be kept same as `_compile_supertasks_in_pipeline` in api.py.
            target_ir = comp_supertask_kind.value
            target_npu = GraphModuleConverter.get_target_npu_from_device(self.devices[device_id])

            compiler_config_context = copy.deepcopy(compiler_config_context)
            compiler_config_context.num_pe = self.devices[device_id].num_pe

            # TODO: improve logging
            # logging only if blockwise compile is used now.
            splitted = node.name.split("_")
            if len(splitted) == 3 and splitted[-1].startswith("c"):
                block_id = int(splitted[-1][1:])
                # This pipeline is generated with blockwise compile.
                logger.info(
                    f"Compiling pipeline {self.pipeline_name}, block={block_id}, target_npu={target_npu}"
                )

                # FIXME: This hack is just for MLPerf.
                # because `if blob_id in self.data_blobs` ensures that only one mid block passes through this code path,
                # we can identify mid blocks for id == 1 (although it is very unstable)
                block_type = {
                    0: BlockType.FIRST,
                    1: BlockType.MID,
                }.get(block_id, BlockType.LAST)
                compiler_config_context.block_type = block_type
            else:
                compiler_config_context.block_type = BlockType.WHOLE

            compiler_config = compiler_config_context.load_config()
            logger.info(f"Using compiler config {compiler_config}")

            # TODO: Use 4pe for now by default, and it should be given from a super task's metadata later.
            data, preprocessed_gm_hash = (
                GraphModuleConverter.compile_gm_and_get_preprocessed_gm_hash(
                    submod,
                    example_input,
                    target_npu,
                    target_ir,
                    compiler_config,
                    dump_path,
                    cache_dir,
                )
            )
            blob_id = DataBlobId(preprocessed_gm_hash)
            if gm_hash:
                self._gm_hash_to_data_blob_id[gm_hash] = blob_id
        else:
            raise NotImplementedError("dfg format is not supported currently")

        self.data_blobs[blob_id] = data
        return blob_id

    def _get_supertask_from_node(
        self,
        node: Node,
        comp_supertask_kind: SuperTaskKind,
        # current context: model_qname, beam_size, phase, bucket
        context: CompilerConfigContext,
        cache_dir: Optional[os.PathLike],
    ) -> SuperTask:
        assert _is_comm_supertask(node) or _is_comp_supertask(node)

        inputs = []
        for input_node in node.args:
            assert isinstance(input_node, Node)
            inputs.append(NameAfterMakeFx(get_tensor_name(input_node)))

        # tensor_meta value can be `None`.
        tensor_meta = node.meta.get("tensor_meta", None)
        if tensor_meta is None:
            tensor_meta = ()

        num_outputs = (
            1
            if isinstance(tensor_meta, torch.fx.passes.shape_prop.TensorMetadata)
            else len(tensor_meta)
        )

        outputs = (
            [
                NameAfterMakeFx(get_tensor_name(node)),
            ]
            if num_outputs == 1
            else [NameAfterMakeFx(get_tensor_name(node, i)) for i in range(num_outputs)]
        )

        supertask: Optional[SuperTask] = None

        device_id = self._get_device_id(node)
        assert isinstance(device_id, DeviceId)

        if _is_comp_supertask(node):
            # comp node
            blob_id = self._get_data_blob_id(node, comp_supertask_kind, context, cache_dir)

            supertask = CompSuperTask(
                kind=comp_supertask_kind,
                data_blob=DataBlobId(blob_id),
                inputs=inputs,
                outputs=outputs,
                device=device_id,
            )
        else:
            # comm supertask
            my_device_id = get_device_id(node)
            assert isinstance(my_device_id, mrw.DeviceId)
            assert isinstance(node.target, SingleDeviceCommOp)
            comm_op = node.target

            def convert_device_ids(metadata: Dict) -> Dict:
                return {
                    k: self.device_id_map[v] if isinstance(v, mrw.DeviceId) else v
                    for k, v in metadata.items()
                }

            supertask = CommSuperTask(
                kind=comm_op.kind(),
                inputs=inputs,
                outputs=outputs,
                device=device_id,
                group=str(comm_op.group.id),
                device_idx=comm_op.group.index(my_device_id),
                metadata=convert_device_ids(comm_op.metadata()),
            )

        assert isinstance(supertask, SuperTask)

        return supertask

    def _add_input_supertask(self, gm: GraphModule):
        placeholder_nodes = tuple(filter(lambda x: x.op == "placeholder", gm.graph.nodes))
        # Do we need to raise error?
        if not all(len(node.users) > 0 for node in placeholder_nodes):
            logger.warning("Some placeholder nodes in rewritten model are not used.")
        input_names = [NameAfterMakeFx(get_tensor_name(node)) for node in placeholder_nodes]

        self.input_supertask = InOutputSuperTask(
            kind=SuperTaskKind.INPUT,
            inputs=[],
            outputs=input_names,
        )

        self._add_new_supertask(self.input_supertask)

    def _add_output_supertask(self, gm: GraphModule):
        output_node = next(filter(lambda x: x.op == "output", gm.graph.nodes))
        output_names = [NameAfterMakeFx(get_tensor_name(node)) for node in output_node.args[0]]

        self.output_supertask = InOutputSuperTask(
            kind=SuperTaskKind.OUTPUT,
            inputs=output_names,
            outputs=[],
        )

        self._add_new_supertask(self.output_supertask)

    @staticmethod
    def _preprocess_gm_for_serialization(gm: GraphModule, node: Node) -> GraphModule:
        fake_mode = get_fake_mode(chain(gm.parameters(), gm.buffers()))
        original_allow_non_fake_inputs = fake_mode.allow_non_fake_inputs
        fake_mode.allow_non_fake_inputs = True
        try:
            # All submodules accept only nodes as an input.
            assert all(isinstance(arg, Node) for arg in node.args)

            # derive example inputs from node info
            tensor_metas = (cast(Node, arg).meta["tensor_meta"] for arg in node.args)

            gm_devices = set(tensor.device for tensor in chain(gm.parameters(), gm.buffers()))
            assert len(gm_devices) <= 1
            gm_device = gm_devices.pop() if len(gm_devices) > 0 else torch.device("cpu")

            with fake_mode:
                inputs = [
                    torch.zeros(tensor_meta.shape, dtype=tensor_meta.dtype, device=gm_device)
                    for tensor_meta in tensor_metas
                ]

            # lower graphmodule into aten level.
            lowered_gm = make_fx(functionalize(gm, remove="mutations_and_views"))(*inputs)

            gm.graph.lint()
            output_node = next(iter(reversed(lowered_gm.graph.nodes)))
            assert output_node.op == "output"
            node_args = output_node.args[0]

            # If GraphModule's output node args format doesn't follow what ``GraphModuleSerializer`` expects, transform it.
            # This happens when gm has no output.
            # https://github.com/pytorch/pytorch/blob/7bcf7da3a268b435777fe87c7794c382f444e86d/torch/_export/serde/serialize.py#L369-L375
            if not isinstance(node_args, (tuple, list, torch.fx.Node)):
                assert node_args is None
                output_node.args = ((),)

            return lowered_gm
        finally:
            fake_mode.allow_non_fake_inputs = original_allow_non_fake_inputs

    @staticmethod
    def _get_fake_slice(
        tensor_meta: TensorMetadata,
        spec: mrw.ShardSpec,
        device: torch.device,
        fake_mode: FakeTensorMode,
    ) -> FakeTensor:
        sliced_shape = list(tensor_meta.shape)
        for placement, dim_width in zip(spec.placements, spec.mesh.size()):
            if placement.is_shard():
                dim = cast(mrw.Shard, placement).dim
                assert sliced_shape[dim] % dim_width == 0
                sliced_shape[dim] //= dim_width
        with fake_mode:
            return cast(
                FakeTensor, torch.empty(sliced_shape, dtype=tensor_meta.dtype, device=device)
            )

    def _get_torch_device(self, node: Node) -> torch.device:
        device_id = get_device_id(node)
        assert isinstance(device_id, mrw.DeviceId)
        return self.devices[self.device_id_map[device_id]].to_torch_device()

    def _get_device_id(self, node: Node) -> DeviceId:
        dev_id = get_device_id(node)
        assert isinstance(dev_id, mrw.DeviceId)
        return self.device_id_map[dev_id]

    def _add_new_supertask(self, super_task: SuperTask):
        id = self._get_next_supertask_id()
        self.supertasks[id] = super_task

    def _get_next_supertask_id(self) -> SuperTaskId:
        self._next_supertask_id += 1
        return SuperTaskId(str(self._next_supertask_id - 1))

    def _add_tensors(
        self,
        param_files: Mapping[ParamFileId, ParamFileInfo],
    ):
        """Add `TensorInfo` for all node in FX graph"""

        # Track index of original placeholder node in original FX graph that placeholder originates from.
        original_placeholder_idx_cnt = 0

        placeholder_met = set()
        # Prepare mapping from tensor name to saved ParamFileInfo in advance.
        constant_name_to_param_file = {}
        for param_file_id, param_file_info in param_files.items():
            for saved_const_name in get_saved_param_names(param_file_info):
                constant_name_to_param_file[saved_const_name] = ParamFileId(param_file_id)

        for node in self.model.graph.nodes:
            if node.op == "placeholder":
                self._add_input_tensor(node, original_placeholder_idx_cnt)
                original_name = get_original_name(node)
                if original_name not in placeholder_met:
                    original_placeholder_idx_cnt += 1
                    placeholder_met.add(original_name)
            elif node.op == "get_attr":
                param_file_id = constant_name_to_param_file[get_original_name(node)]
                param_file_info = param_files[param_file_id]
                self._add_constant_tensor(
                    node,
                    param_file_id,
                    param_file_info,
                )
            elif is_getitem(node):
                tensor_name = get_tensor_name(node)
                assert tensor_name in self.tensors
                # inputs of getitem nodes doesn't need to be handled
                # because we only consider tensors, not tuple of tensors.
                continue
            elif _is_comm_supertask(node) or _is_comp_supertask(node):
                self._add_supertask_output_tensors(node)
            elif node.op == "output":
                self._add_output_tensors(node)
            else:
                raise NotImplementedError(f"node {node.name} is not supported")

    def _add_input_tensor(self, node: Node, original_placeholder_idx: int):
        # Get ``TensorInfoWithPlacement`` for input nodes
        tensor_name = get_tensor_name(node)
        assert tensor_name not in self.tensors
        device_id = self._get_device_id(node)
        assert isinstance(device_id, DeviceId)

        self.tensors[NameAfterMakeFx(tensor_name)] = self._get_inoutput_tensor_info_from_node(
            node,
            kind="input",
            idx=original_placeholder_idx,
        )

        original_name = get_original_name(node)
        if original_name not in self._unsharded_shape_per_input:
            unsharded_tensor_meta = get_unsharded_tensor_meta(node)
            assert isinstance(unsharded_tensor_meta, TensorMetadata)
            self._unsharded_shape_per_input[original_name] = tuple(unsharded_tensor_meta.shape)

    def _add_constant_tensor(
        self, node: Node, param_file_id: ParamFileId, param_file_info: ParamFileInfo
    ):
        assert has_original_name(node), "All get_attr nodes should have original name"
        # parameter or buffer stored in parameter file
        original_name = get_original_name(node)
        assert _tensor_exists_in_file(
            original_name, param_file_info
        ), f"{original_name} does not exist in parameter file."

        param_value = ParamValue(
            param_file_id,
            _get_saved_name(param_file_info, original_name),
            node.name,
            Placements.from_node(node),
        )

        tensor_info = TensorInfo.from_node(node)
        tensor_name = get_tensor_name(node)
        assert tensor_name not in self.tensors
        self.tensors[NameAfterMakeFx(tensor_name)] = ParamInfo(
            tensor_info.shape, tensor_info.dtype, param_value
        )

    def _add_supertask_output_tensors(self, node: Node):
        # all call_module nodes are either submodule containing multiple computation ops
        # or submodule for single collective communication op.
        assert _is_comm_supertask(node) or _is_comp_supertask(node)

        if _is_comp_supertask(node):
            assert isinstance(node.target, str)
            submod = getattr(self.model, node.target)
            assert isinstance(submod, GraphModule)
            submod_placeholders = tuple(
                node for node in submod.graph.nodes if node.op == "placeholder"
            )

            assert len(submod_placeholders) == len(node.args)

        # register output tensors of the node.
        tensor_meta = node.meta.get("tensor_meta", None)
        if isinstance(tensor_meta, torch.fx.passes.shape_prop.TensorMetadata):
            tensor_name = get_tensor_name(node)
            assert tensor_name not in self.tensors
            self.tensors[NameAfterMakeFx(tensor_name)] = TensorInfo.from_node(node)
        elif isinstance(tensor_meta, (list, tuple)):
            for idx, meta in enumerate(tensor_meta):
                tensor_name = get_tensor_name(node, idx)
                assert tensor_name not in self.tensors
                self.tensors[NameAfterMakeFx(tensor_name)] = TensorInfo.from_node_tensor_meta_data(
                    meta
                )
        else:
            # There can be supertasks with no user (child). It can be in-place update ops or communication ops.
            assert len(node.users) == 0

    def _add_output_tensors(self, node: Node):
        args = node.args[0]
        assert node.op == "output"
        assert isinstance(args, tuple)

        specs_for_outputs = []
        original_names = get_original_name(node)

        unsharded_tensor_metas = get_unsharded_tensor_meta(node)
        assert isinstance(unsharded_tensor_metas, tuple)

        unsharded_shapes = []
        for unsharded_tensor_meta in unsharded_tensor_metas:
            assert isinstance(unsharded_tensor_meta, TensorMetadata)
            unsharded_shapes.append(unsharded_tensor_meta.shape)

        specs = get_spec(node)

        if not isinstance(specs, Sequence):
            specs = (specs,)

        assert isinstance(original_names, Sequence)
        assert (
            len(original_names) == len(unsharded_shapes) == len(specs)
        ), "Metadata for output node is not correct"

        for idx, (spec, original_name, unsharded_shape) in enumerate(
            zip(specs, original_names, unsharded_shapes)
        ):
            for _ in spec.mesh.get_all_devices():
                specs_for_outputs.append((idx, spec, original_name))

            assert original_name not in self._unsharded_shape_per_output
            self._unsharded_shape_per_output[original_name] = unsharded_shape

        for arg, (idx, spec, obtained_original_name) in zip(args, specs_for_outputs):
            assert isinstance(arg, Node)
            tensor_name = get_tensor_name(arg)
            assert tensor_name in self.tensors
            set_spec(arg, spec)
            set_original_name(arg, obtained_original_name)

            self.tensors[NameAfterMakeFx(tensor_name)] = self._get_inoutput_tensor_info_from_node(
                arg, kind="output", idx=idx
            )

    def _get_inoutput_tensor_info_from_node(
        self, node: Node, kind: str, idx: int, original_name: Optional[str] = None
    ) -> InOutputTensorInfo:
        tensor_info = TensorInfoWithPlacement.from_node(node)

        # calculate original tensor shape
        original_name = original_name or get_original_name(node)
        device_id = self._get_device_id(node)
        assert isinstance(device_id, DeviceId)
        return InOutputTensorInfo(
            tensor_info,
            original_name,
            idx=idx,
            device_id=device_id,
            kind=kind,
        )
