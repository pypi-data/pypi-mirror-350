import copy
import dataclasses
from functools import cached_property
import glob
from itertools import chain, product
import json
import logging
import os
from pathlib import Path
from pprint import pformat
import tempfile
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
    get_args,
)
import uuid

from furiosa_torch_ext.torch_ext import preprocess
from openai.types.chat import ChatCompletionMessageParam
import torch
from torch._subclasses import FakeTensorMode
from torch.fx import GraphModule
from torch.fx.passes.shape_prop import ShapeProp
import transformers
from transformers import (
    MODEL_FOR_CAUSAL_LM_MAPPING,
    BatchEncoding,
    PretrainedConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    set_seed,
)
import yaml

from furiosa_llm.optimum.modeling import (
    FURIOSA_CONFIG_JSON,
    _is_model_path,
    get_mapped_class_for_optimization,
)
from furiosa_llm.parallelize.export.graphmodule import deserialize_gm
from furiosa_llm.parallelize.model_creation_info import ModelCreationInfo
from furiosa_llm.parallelize.mppp.api import PipelineParallelismMppp
from furiosa_llm.parallelize.mppp.config import DeviceId
from furiosa_llm.parallelize.pipeline.builder.converter import GraphModuleConverter
from furiosa_llm.parallelize.pipeline.types import (
    CompSuperTask,
    DataBlobId,
    Device,
    ParamInfo,
    SuperTaskKind,
    TensorInfo,
    load_partial_param,
)
from furiosa_llm.parallelize.trace import get_param_file_with_cache
from furiosa_llm.server.utils import is_list_of
from furiosa_llm.version import FURIOSA_LLM_VERSION, FuriosaVersionInfo

from .artifact import Artifact, ModelArtifact, ModelMetadataForArtifact
from .artifact.helper import (
    build_pipelines,
    get_buckets_with_output_logits_size,
    get_default_pipeline_metadata,
    override_pp_size_on_pipeline,
    prestep_for_remote_code_model,
)
from .device import get_device_mesh, parse_devices_str
from .models.config_types import (
    Bucket,
    BucketConfig,
    BucketWithOutputLogitsSize,
    GeneratorConfig,
    KvCacheSharingAcrossBeamsConfig,
    LLMBackend,
    ManualBucketConfig,
    MinimalBucketConfig,
    ModelRewritingConfig,
    PagedAttentionConfig,
    ParallelConfig,
    PipelineMetadata,
    PipelineWithMetadata,
    SchedulerConfig,
)
from .models.metadata import LLMConfig, ModelMetadata, get_model_cls_from_pretrained_id
from .optimum import AttentionType, OptimizationConfig, QDtype, QuantizationConfig
from .optimum.types import FuriosaConfig, ModelKind, get_kv_cache_dtype_from_qformat
from .outputs import CompletionOutput, Logprob, RequestOutput
from .parallelize.compiler_config import CompilerConfigContext
from .parallelize.pipeline import Pipeline
from .sampling_params import SamplingParams
from .tokenizer import encode_auto, get_tokenizer
from .utils import get_list_with_no_dup_with_order_preserved, get_logger_with_tz, zip_equal

logger = get_logger_with_tz(logging.getLogger(__name__))

# Default position id for padding
_POSITION_ID_PAD = 1

# Default param file name
_HF_CAUSAL_LM_CLASS_NAMES = set(
    model_cls.__name__ for model_cls in MODEL_FOR_CAUSAL_LM_MAPPING.values()
)

# Default index of the padding block when paged attention model is used.
DEFAULT_PAGED_ATTENTION_PADDING_BLOCK_IDX = 0

CACHE_DIR = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache")) / "furiosa" / "llm"

TokenizerModeType = Literal["auto", "slow"]
ChatTemplateContentFormatOption = Literal["string"]

RAY_LOG_PREFIX = "[furiosa-llm]"

STREAMING_MAX_DECODE_TRIAL = 2


def _get_available_devices() -> List[Device]:
    try:
        import furiosa_smi_py  # type: ignore[import-untyped]
        from furiosa_smi_py import (  # type: ignore[import-not-found, import-untyped]
            CoreStatus,
            list_devices,
        )
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Install furiosa_smi_py to get available devices automatically.")
    except Exception as e:
        raise ImportError(f"Failed to import furiosa_smi_py with error {e}")

    try:
        furiosa_smi_py.init()
        devices = list_devices()
        available_devs = []
        for device in devices:
            # e.g. npu1
            name = device.device_info().name()
            if name[:3] != "npu":
                raise RuntimeError("Unexpected device name: {name}")
            npu_idx = int(name[3:])
            core_status = device.core_status()

            for pe_status in core_status.pe_status():
                # Cannot be compared by reference (using "is") because `CoreStatus` is a Rust enum exposed with PyO3.
                if pe_status.status() == CoreStatus.Available:
                    available_devs.append(Device(f"npu:{npu_idx}:{pe_status.core()}"))
        return available_devs
    except Exception as e:
        raise RuntimeError(f"Failed to get available devices with error {e}")


def _get_bucket_from_pipeline_name(pipeline_name: str) -> Bucket:
    # Returns: tuple of (is_prefill, bucket)
    # Possible pipeline name formats:
    # * f"{model_name}-{mode}-b{bucket.batch_size}-attn{bucket.attention_size} (will be deprecated)
    # * f"{model_name}-kv{bucket.kv_cache_size}-b{bucket.batch_size}-attn{bucket.attention_size}
    _, mode_or_kv_cache_size, b_batch_size, attn_attn_size = pipeline_name.split("-")

    batch_size = int(b_batch_size[1:])
    attn_size = int(attn_attn_size[4:])

    if mode_or_kv_cache_size == "prefill":
        kv_size = 0
    elif mode_or_kv_cache_size == "decode":
        kv_size = attn_size - 1
    else:
        assert mode_or_kv_cache_size.startswith("kv")
        kv_size = int(mode_or_kv_cache_size[2:])

    return Bucket(batch_size, attn_size, kv_size)


class UnexpectedModelKind(Exception):
    def __init__(self, expected_kind: ModelKind, actual_kinds: List[ModelKind]):
        self.expected_kind = expected_kind
        self.actual_kinds = actual_kinds
        super().__init__(
            f"Expected model kind {expected_kind.name}, but got {', '.join([kind.name for kind in actual_kinds])}"
        )


def _get_path_or_hf_download(
    model_id_or_path: Union[str, os.PathLike],
    revision: Optional[str] = None,
    expected_kind: Optional[ModelKind] = None,
) -> Path:
    """If the model_id_or_path is a model_id, download the model from HuggingFace Hub. Otherwise, just return a path."""
    from huggingface_hub import hf_hub_download, snapshot_download

    model_path = model_id_or_path

    if isinstance(model_id_or_path, str) and not _is_model_path(
        model_id_or_path
    ):  # if this is model_id
        model_id: str = str(model_id_or_path)
        furiosa_config_json_path = hf_hub_download(
            repo_id=model_id, filename=FURIOSA_CONFIG_JSON, revision=revision
        )
        furiosa_config = FuriosaConfig.load(furiosa_config_json_path)

        # Downloading a model takes a long time, so we download it only if the model has the disired kind.
        if expected_kind:
            if expected_kind in furiosa_config.model_kinds:
                model_path = snapshot_download(repo_id=model_id, revision=revision)
            else:
                raise UnexpectedModelKind(expected_kind, furiosa_config.model_kinds)

    return Path(model_path)


RELEASE_ARTIFACT_KEYS = {
    "furiosa-ai/bert-large-uncased-INT8-MLPerf",
    "furiosa-ai/DeepSeek-R1-Distill-Llama-8B",
    "furiosa-ai/DeepSeek-R1-Distill-Llama-70B",
    "furiosa-ai/EXAONE-3.5-7.8B-Instruct",
    "furiosa-ai/gpt-j-6b-FP8-MLPerf",
    "furiosa-ai/Llama-2-70b-chat-hf-FP8-MLPerf",
    "furiosa-ai/Llama-3.1-8B-Instruct",
    "furiosa-ai/Llama-3.1-8B-Instruct-FP8",
    "furiosa-ai/Llama-3.3-70B-Instruct",
    "furiosa-ai/Llama-3.3-70B-Instruct-FP8",
}


def _resolve_default_hf_revision(
    model_id_or_path: Union[str, os.PathLike],
    sdk_version: FuriosaVersionInfo,
) -> Optional[str]:
    if not isinstance(model_id_or_path, str):
        return None
    if model_id_or_path in RELEASE_ARTIFACT_KEYS and sdk_version.stage == "release":
        return f"v{sdk_version.version}"
    return None


class LLM:
    """An LLM for generating texts from given prompts and sampling parameters.

    Args:
        model: The name of the pretrained model. This corresponds to
            pretrained_model_name_or_path in HuggingFace Transformers.
        task_type: The type of the task. This corresponds to task in HuggingFace Transformers.
            See https://huggingface.co/docs/transformers/main/en/quicktour#pipeline for more
            details.
        llm_config: The configuration for the LLM. This includes quantization and optimization
            configurations.
        auto_bfloat16_cast: Whether to cast the model to bfloat16 automatically.
            This option is required when neither the model is trained with bfloat16 nor quantized.
        qformat_path: The path to the quantization format file.
        qparam_path: The path to the quantization parameter file.
        quant_ckpt_file_path: The path to the quantized parameters checkpoint file.
        hf_overrides: Additional HuggingFace Transformers model configuration. This is a dictionary
            that includes the configuration for the model.
        bucket_config: Config for bucket generating policy. If not given, the model will use single one batch, `max_seq_len_to_capture` attention size bucket per
            each phase.
        speculative_model: Speculative model for speculative decoding.
        speculative_model_llm_config: The configuration for the speculative model. This includes quantization and optimization
            configurations.
        speculative_model_qformat_path: The path to the quantization format file for the speculative model.
        speculative_model_qparam_path: The path to the quantization parameter file for the speculative model.
        speculative_model_quant_ckpt_file_path: The path to the quantized parameters checkpoint file for the speculative model.
        speculative_model_config: Additional HuggingFace Transformers model configuration for the speculative model. This is a dictionary
            that includes the configuration for the model.
        speculative_model_bucket_config: Config for bucket generating policy. If not given, the model will use single one batch, `max_seq_len_to_capture` attention size bucket per
            each phase.
        speculative_draft_tensor_parallel_size: The number of PEs for each tensor parallelism group in speculative model.
            If not given, it will follow the value of the target model.
            This value will be ignored if `speculative_model` is given as `LLM` instance.
        speculative_draft_data_parallel_size: The size of the data parallelism for running speculative model.
            If not given, it will follow the value of the target model.
            This value will be ignored if `speculative_model` is given as `LLM` instance.
        speculative_draft_pipeline_parallel_size: The size of the pipeline parallelism for running speculative model.
            The argument is valid only for artifacts that use blockwise compilation.
            If not given, it will follow the value of the target model.
            This value will be ignored if `speculative_model` is given as `LLM` instance.
        speculative_draft_num_blocks_per_pp_stage: The number of transformer blocks per each pipeline parallelism stage for running speculative model.
            The argument is valid only for artifacts that use blockwise compilation.
            If not given, it will follow the value of the target model.
            In anyway if only `speculative_draft_pipeline_parallel_size` is provided, transformer blocks of speculative model will be distributed equally.
            This value will be ignored if `speculative_model` is given as `LLM` instance.
        num_speculative_tokens: The number of tokens that specualtive model will generate speculatively during each iteration of the decoding process
        max_seq_len_to_capture: Maximum sequence length covered by LLM engine. Sequence with larger context than this will not be covered.
            The default is 2048.
        max_prompt_len: Maximum prompt sequence length covered by LLM engine. Prompt larger than this cannot be handled.
            If not given, will be obtained from bucket and other configs.
        tensor_parallel_size: The number of PEs for each tensor parallelism group. The default is 4.
        pipeline_parallel_size: The number of pipeline stages for pipeline parallelism. The default is 1,
            which means no pipeline parallelism.
        data_parallel_size: The size of the data parallelism group. If not given, it will be inferred from
            total available PEs and other parallelism degrees.
        trust_remote_code: Trust remote code when downloading the model and tokenizer from HuggingFace.
        tokenizer: The name or path of a HuggingFace Transformers tokenizer.
        tokenizer_mode: The tokenizer mode. "auto" will use the fast tokenizer
            if available, and "slow" will always use the slow tokenizer.
        seed: The seed to initialize the random number generator for sampling.
        devices: The devices to run the model. It can be a single device or a list of devices.
            Each device can be either "npu:X" or "npu:X:\*" where X is a specific device index.
            If not given, available devices will be used.
        param_file_path: The path to the parameter file to use for pipeline generation.
            If not specified, the parameters will be saved in a temporary file which will be
            deleted when ``LLM`` is destroyed.
        param_saved_format: The format of the parameter file. Only possible value is "safetensors" now.
            The default is "safetensors".
        do_decompositions_for_model_rewrite: Whether to decompose some ops to describe various parallelism strategies
            with mppp config. When the value is True, mppp config that matches with the decomposed FX graph should be given.
        comp_supertask_kind: The format that pipeline's supertasks will be represented as.
            Possible values are "fx","dfg", and "edf", and the default is "edf".
        cache_dir: The cache directory for all generated files for this LLM instance.
            When its value is ``None``, caching is disabled. The default is "$HOME/.cache/furiosa/llm".
        backend: The backend implementation to run forward() of a model for the LLM.
            If not specified, the backend will be chosen based on the device kind.
        use_blockwise_compile: If True, each task will be compiled in the unit of transformer block,
            and compilation result for transformer block is generated once and reused. The default is ``True``.
        num_blocks_per_supertask: The number of transformer blocks that will be merged into one supertask. This option is valid
            only when `use_blockwise_compile=True`. The default is 1.
        num_blocks_per_pp_stage: The number of transformers blocks per each pipeline parallelism stage. If not given, transformer blocks will be
            distributed equally.
        embed_all_constants_into_graph: Whether to embed constant tensors into graph or make them as input of the graph and save them as separate files.
            The default is False.
        paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store. This argument must be given
            if model uses paged attention.
        paged_attention_block_size: The maximum number of tokens that can be stored in a single paged attention block. This argument must be given
            if model uses paged attention.
        kv_cache_sharing_across_beams_config: Configuration for sharing kv cache across beams. This argument must be given if and only if
            the model is optimized to share kv cache across beams. If this argument is given, decode phase buckets with batch size of
            ``batch_size`` \* ``kv_cache_sharing_across_beams_config.beam_width`` will be created.
        prefill_chunk_size: Chunk size used for chunked prefill. If the value is `None`, chunked prefill is not used.
        scheduler_config: Configuration for the scheduler, allowing to maximum number of tasks which can be queued to HW, maximum number of samples
            that can be processed by the scheduler, and ratio of spare blocks that are reserved by scheduler.
        packing_type: Packing algorithm. Possible values are "IDENTITY" only for now
        compiler_config_overrides: Overrides for the compiler config. This is a dictionary that includes the configuration for the compiler.
        use_random_weight: If True, the model will be initialized with random weights.
        num_pipeline_builder_workers: number of workers used for building pipelines (except for compilation). The default is 1 (no parallelism).
            Setting this value larger than 1 reduces pipeline building time, especially for large models, but requires much more memory.
        num_compile_workers: number of workers used for compilation. The default is 1 (no parallelism).
        skip_engine: If True, the native runtime engine will not be initialized. This is useful when you need
            the pipelines for other purposes than running them with the engine.
        artifacts_export_path: The path to export the artifacts. With artifacts, you can create ``LLM`` without quantizing or compiling the model again.
    """

    max_seq_len_to_capture: Optional[int]

    def __init__(
        self,
        model: str,
        task_type: Optional[str] = None,
        llm_config: Optional[LLMConfig] = None,
        auto_bfloat16_cast: Optional[bool] = None,
        qformat_path: Optional[os.PathLike] = None,  # FIXME: move to quantization_config
        qparam_path: Optional[os.PathLike] = None,  # FIXME: move to quantization_config
        quant_ckpt_file_path: Optional[os.PathLike] = None,
        hf_overrides: Dict[str, Any] = {},  # aka hf_config
        bucket_config: Optional[BucketConfig] = None,
        speculative_model: Optional[Union[str, "LLM"]] = None,
        speculative_model_llm_config: Optional[LLMConfig] = None,
        speculative_model_qformat_path: Optional[os.PathLike] = None,
        speculative_model_qparam_path: Optional[os.PathLike] = None,
        speculative_model_quant_ckpt_file_path: Optional[os.PathLike] = None,
        speculative_model_config: Dict[str, Any] = {},
        speculative_model_bucket_config: Optional[BucketConfig] = None,
        speculative_draft_tensor_parallel_size: Optional[int] = None,
        speculative_draft_pipeline_parallel_size: Optional[int] = None,
        speculative_draft_data_parallel_size: Optional[int] = None,
        speculative_draft_num_blocks_per_pp_stage: Optional[Sequence[int]] = None,
        num_speculative_tokens: Optional[int] = None,
        max_seq_len_to_capture: int = 2048,
        max_prompt_len: Optional[int] = None,
        tensor_parallel_size: int = 4,
        pipeline_parallel_size: int = 1,
        data_parallel_size: Optional[int] = None,
        tokenizer: Optional[Union[PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
        tokenizer_mode: TokenizerModeType = "auto",
        trust_remote_code: bool = False,
        seed: Optional[int] = None,
        # TODO: change devices default value to None and get devices from furiosa-smi.
        devices: Optional[Union[str, Sequence[Device]]] = None,
        param_file_path: Optional[os.PathLike] = None,
        param_saved_format: Literal["safetensors", "pt"] = "safetensors",
        do_decompositions_for_model_rewrite: bool = False,  # FIXME: move to compiler_config
        comp_supertask_kind: Optional[Literal["edf", "dfg", "fx"]] = None,
        cache_dir: Optional[os.PathLike] = CACHE_DIR,
        backend: Optional[LLMBackend] = None,
        use_blockwise_compile: bool = True,  # FIXME: move to compiler_config
        num_blocks_per_supertask: int = 1,  # FIXME: move to compiler_config
        num_blocks_per_pp_stage: Optional[Sequence[int]] = None,
        embed_all_constants_into_graph: bool = False,
        paged_attention_block_size: int = 1,  # FIXME: move to compiler_config
        kv_cache_sharing_across_beams_config: Optional[
            KvCacheSharingAcrossBeamsConfig
        ] = None,  # FIXME: move to compiler_config / leave this in LLM attr ??
        prefill_chunk_size: Optional[int] = None,
        scheduler_config: SchedulerConfig = SchedulerConfig(),
        packing_type: Literal["IDENTITY"] = "IDENTITY",
        compiler_config_overrides: Optional[Mapping] = None,
        use_random_weight: bool = False,
        num_pipeline_builder_workers: int = 1,
        num_compile_workers: int = 1,
        skip_engine: bool = False,
        artifacts_export_path: Optional[Union[str, os.PathLike]] = None,
        *,
        _cleanup: bool = True,
        _pipelines_with_metadata: Optional[Sequence[PipelineWithMetadata]] = None,
        _custom_buckets: Sequence[Union[Bucket, BucketWithOutputLogitsSize]] = [],
        _optimize_logit_shape: bool = True,
        _model_metadata: Optional[ModelMetadata] = None,
        _unpadded_vocab_size: Optional[int] = None,
        _embedding_layer_as_single_block: bool = False,
        _artifact_id: str = "NO_ARTIFACT_ID",
        **kwargs,
    ):
        self.artifact_id = _artifact_id
        optimize_paged_attention_block_loading = kwargs.pop(
            "optimize_paged_attention_block_loading", True
        )
        sparse_select_version = kwargs.pop("sparse_select_version", "v1.5")
        one_supertask_per_device = kwargs.pop("one_supertask_per_device", True)

        if config := kwargs.pop("config", None):
            logger.warning("`config` is deprecated. use `hf_overrides` instead.")
            if hf_overrides:
                raise ValueError("`config` and `hf_overrides` are given at the same time.")
            hf_overrides = config

        # For Vllm compatibility
        enable_chunked_prefill = kwargs.pop("enable_chunked_prefill", None)
        max_num_batched_tokens = kwargs.pop("max_num_batched_tokens", None)

        if enable_chunked_prefill is not None != max_num_batched_tokens is not None:
            raise ValueError(
                "`enable_chunked_prefill` and `max_num_batched_tokens` must be given at the same time."
            )

        if enable_chunked_prefill:
            assert max_num_batched_tokens is not None
            if prefill_chunk_size is not None:
                raise ValueError(
                    "Both `prefill_chunk_size` and `max_num_batched_tokens` are given. Please provide only one of them."
                )
            prefill_chunk_size = max_num_batched_tokens

        # Set seed in order to guarantee the reproducibility with the same seed number
        if seed is not None:
            set_seed(seed)

        LLM.__verify_tokenizer_mode(tokenizer_mode)

        # Set logging options for ray.
        if "RAY_COLOR_PREFIX" not in os.environ:
            os.environ["RAY_COLOR_PREFIX"] = "1"
        if "RAY_DEDUP_LOGS_ALLOW_REGEX" not in os.environ:
            # For not to dedup our info logs.
            os.environ["RAY_DEDUP_LOGS_ALLOW_REGEX"] = f"INFO:*{RAY_LOG_PREFIX}*"

        if devices is None:
            devices = _get_available_devices()
            logger.info(f"Device is not given, using available device: {devices}")

        assert devices is not None

        # Normalize the devices
        if isinstance(devices, str):
            devices = parse_devices_str(devices)
        LLM.__verify_devices(devices)

        if num_pipeline_builder_workers < 1:
            raise ValueError("`num_pipeline_builder_workers` must be larger than 0")

        if llm_config is None:
            opt_config = self._get_default_opt_config_from_pretrained_id(model, trust_remote_code)
            quant_config = QuantizationConfig.from_qformat(qformat_path) if qformat_path else None
            llm_config = LLMConfig(opt_config, quant_config)

        # To use speculative decoding, special model optimized for speculative decoding is needed.
        if num_speculative_tokens:
            llm_config = LLMConfig(
                llm_config.optimization_config.with_optimizations(
                    {"optimized_for_speculative_decoding": True}
                ),
                llm_config.quantization_config,
            )
        if _model_metadata:
            self.model_metadata = _model_metadata
        else:
            self.model_metadata = ModelMetadata(
                pretrained_id=model,
                task_type=task_type,
                llm_config=llm_config,
                hf_configs=hf_overrides.copy(),
                trust_remote_code=trust_remote_code,
            )

        if auto_bfloat16_cast:
            self.model_metadata = self.model_metadata.with_auto_bfloat16_cast()

        self.model_config = self.model_metadata.config_dict
        self.is_generative_model = self.model_metadata.is_generative_model
        kv_cache_dtype = self.model_metadata.kv_cache_dtype

        if max_seq_len_to_capture > self.model_max_seq_len:
            raise ValueError(
                "`max_seq_len_to_capture` is larger than the model's max number of positions."
            )

        # FIXME: remove `prefill_chunk_size` field from SchedulerConfig and move it to GeneratorConfig.
        if scheduler_config.prefill_chunk_size is not None and prefill_chunk_size is not None:
            raise ValueError(
                "Both `scheduler_config.prefill_chunk_size` and `prefill_chunk_size` are given. Please provide only one of them."
            )
        if scheduler_config.prefill_chunk_size is not None:
            logger.warning(
                "Setting prefill chunk size with `scheduler_config` is deprecated. Please use `enable_chunked_prefill` and `max_num_batched_tokens` instead."
            )
        elif prefill_chunk_size is not None:
            scheduler_config = dataclasses.replace(
                scheduler_config, prefill_chunk_size=prefill_chunk_size
            )

        if bucket_config is None:
            # TODO: always set max_seq_len to model's max_position_embeddings once compiler supports it.
            bucket_config = MinimalBucketConfig(max_seq_len=max_seq_len_to_capture)
        (
            prefill_buckets_with_output_size,
            decode_buckets_with_output_size,
            other_buckets_with_output_size,
        ) = get_buckets_with_output_logits_size(
            self.model_metadata,
            bucket_config,
            max_prompt_len or max_seq_len_to_capture,
            max_seq_len_to_capture,
            num_speculative_tokens,
            scheduler_config.prefill_chunk_size,
            _optimize_logit_shape,
        )

        if _custom_buckets:
            for custom_bucket in _custom_buckets:
                if isinstance(custom_bucket, BucketWithOutputLogitsSize):
                    bucket_with_output_size = custom_bucket
                    bucket = custom_bucket.bucket
                else:
                    assert isinstance(custom_bucket, Bucket)
                    output_logits_size = self.model_metadata.get_output_logits_size(custom_bucket)
                    bucket_with_output_size = BucketWithOutputLogitsSize(
                        custom_bucket, output_logits_size=output_logits_size
                    )
                    bucket = custom_bucket

                if bucket.is_prefill:
                    prefill_buckets_with_output_size.append(bucket_with_output_size)
                elif bucket.input_ids_size == 1:
                    decode_buckets_with_output_size.append(bucket_with_output_size)
                else:
                    other_buckets_with_output_size.append(bucket_with_output_size)

            # remove duplication if any.
            prefill_buckets_with_output_size = get_list_with_no_dup_with_order_preserved(
                prefill_buckets_with_output_size
            )
            decode_buckets_with_output_size = get_list_with_no_dup_with_order_preserved(
                decode_buckets_with_output_size
            )
            other_buckets_with_output_size = get_list_with_no_dup_with_order_preserved(
                other_buckets_with_output_size
            )

        buckets_with_output_size = [
            *prefill_buckets_with_output_size,
            *decode_buckets_with_output_size,
            *other_buckets_with_output_size,
        ]

        # NOTE: Allow no prefill or decode bucket case with skip_engine=True for artifacts building and internal tests.
        if not skip_engine and not prefill_buckets_with_output_size:
            raise ValueError("Prefill buckets must be given.")

        # Find or check max prompt length is valid and set as field.
        if scheduler_config.prefill_chunk_size:
            bucket_max_prompt_len = max_prompt_len or max_seq_len_to_capture
        else:
            bucket_max_prompt_len = (
                max(
                    bucket_with_output_size.bucket.attention_size
                    for bucket_with_output_size in prefill_buckets_with_output_size
                )
                if prefill_buckets_with_output_size
                else 0
            )
        if max_prompt_len is not None:
            if bucket_max_prompt_len < max_prompt_len:
                raise ValueError(
                    f"Generated buckets cannot handle prompts with `max_prompt_len` {max_prompt_len}. Generate larger buckets or decrease `max_prompt_len`."
                )

            self.prompt_max_seq_len = max_prompt_len
        else:
            self.prompt_max_seq_len = bucket_max_prompt_len

        # Find the max attention_size of prefill/decode_buckets and set them as field.
        if decode_buckets_with_output_size:
            bucket_max_seq_len_to_capture = max(
                bucket_with_output_size.bucket.attention_size
                for bucket_with_output_size in decode_buckets_with_output_size
            )
        else:
            bucket_max_seq_len_to_capture = max(
                (
                    bucket_with_output_size.bucket.attention_size
                    for bucket_with_output_size in chain(
                        prefill_buckets_with_output_size, other_buckets_with_output_size
                    )
                ),
            )

        if bucket_max_seq_len_to_capture < max_seq_len_to_capture:
            raise ValueError(
                "There's no bucket to handle `max_seq_len_to_capture` length of sequence. Add bucket of size `max_seq_len_to_capture` or decrease `max_seq_len_to_capture`."
            )
        elif bucket_max_seq_len_to_capture > max_seq_len_to_capture:
            logger.warning(
                "Buckets with larger sequence length than `max_seq_len_to_capture` will be created. This will cause unnecessary overhead."
            )
        self.max_seq_len_to_capture = bucket_max_seq_len_to_capture

        logger.info(
            f"Prefill buckets with output size: {pformat(prefill_buckets_with_output_size)}"
        )
        logger.info(f"Decode buckets with output size: {pformat(decode_buckets_with_output_size)}")
        logger.info(f"Other buckets with output size: {pformat(other_buckets_with_output_size)}")

        prefill_buckets = [
            bucket_with_output_size.bucket
            for bucket_with_output_size in prefill_buckets_with_output_size
        ]
        decode_buckets = [
            bucket_with_output_size.bucket
            for bucket_with_output_size in decode_buckets_with_output_size
        ]
        other_buckets = [
            bucket_with_output_size.bucket
            for bucket_with_output_size in other_buckets_with_output_size
        ]

        LLM.__verify_buckets(prefill_buckets, decode_buckets, kv_cache_sharing_across_beams_config)

        if (
            self.model_metadata.optimize_options.kv_cache_sharing_across_beams
            and kv_cache_sharing_across_beams_config is None
        ):
            raise ValueError(
                "`kv_cache_sharing_across_beams_config` must be given if the model is optimized to share kv cache across beams."
            )

        padding_block_idx = (
            DEFAULT_PAGED_ATTENTION_PADDING_BLOCK_IDX
            if optimize_paged_attention_block_loading
            else None
        )

        if self.model_metadata.attention_type is AttentionType.PAGED_ATTENTION:
            if paged_attention_block_size != 1:
                raise NotImplementedError(
                    "Currently, only paged attention with block_size=1 is supported."
                )
            paged_attention_config = PagedAttentionConfig(
                paged_attention_block_size, padding_block_idx
            )
        else:
            paged_attention_config = None

        self.generator_config = GeneratorConfig(
            _POSITION_ID_PAD,
            get_list_with_no_dup_with_order_preserved(
                (*prefill_buckets, *decode_buckets, *other_buckets)
            ),
            self.model_metadata.model_qname,
            paged_attention_config,
            packing_type,
            kv_cache_sharing_across_beams_config,
            num_speculative_tokens,
            unpadded_vocab_size=_unpadded_vocab_size,
        )

        self.scheduler_config = scheduler_config

        # FIXME: this is a temporary workaround to test decode buckets with more than one input_ids.
        self.custom_buckets = _custom_buckets

        self.model_rewriting_config = ModelRewritingConfig(
            do_decompositions_for_model_rewrite=do_decompositions_for_model_rewrite,
            use_blockwise_compile=use_blockwise_compile,
            embedding_layer_as_single_block=_embedding_layer_as_single_block,
            num_blocks_per_supertask=num_blocks_per_supertask,
            embed_all_constants_into_graph=embed_all_constants_into_graph,
            optimize_logit_shape=_optimize_logit_shape,
        )

        if device_sets_for_actual_use := kwargs.pop("device_sets_for_actual_use", None):
            logger.warning(
                "`device_sets_for_actual_use` is deprecated. Use `{tensor|pipeline|data}_parallel` options instead."
            )
            normalized_dev_mesh = [
                parse_devices_str(device_set) if isinstance(device_set, str) else device_set
                for device_set in device_sets_for_actual_use
            ]
        else:
            dev_mesh = get_device_mesh(
                devices, tensor_parallel_size, pipeline_parallel_size, data_parallel_size
            )
            # Flatten pp_tp_groups to build pipeline. This is 2d-matrix whose elements are dp subgroups.
            normalized_dev_mesh = [
                [dev for tp_group in pp_tp_group for dev in tp_group] for pp_tp_group in dev_mesh
            ]
        logger.info(
            f"Device Mesh currently working is {normalized_dev_mesh} with tp_size={tensor_parallel_size}/pp_size={pipeline_parallel_size}/dp_size={data_parallel_size}"
        )
        if (
            num_blocks_per_pp_stage is not None
            and len(num_blocks_per_pp_stage) != pipeline_parallel_size
        ):
            raise ValueError(
                "`num_blocks_per_pp_stage` should have length of `pipeline_parallel_size`"
            )

        self.parallel_config = ParallelConfig(
            tensor_parallel_size=tensor_parallel_size, pipeline_parallel_size=pipeline_parallel_size
        )

        data_parallel_size = len(normalized_dev_mesh)

        # Build pipelines for first pp_tp_group and replicate them for other pp_tp_groups later.
        first_dp_subgroup_devices = normalized_dev_mesh[0]

        if backend is None:
            dev_kind = devices[0].kind
            if dev_kind == "npu":
                backend = LLMBackend.FURIOSA_RT_V2
            elif dev_kind == "cpu":
                backend = LLMBackend.MOCK_BACKEND_V2
            else:
                raise ValueError(f"Invalid device kind: {dev_kind}")

        if comp_supertask_kind is None:
            if backend in (LLMBackend.FURIOSA_RT_NPU, LLMBackend.FURIOSA_RT_V2):
                comp_supertask_kind = "edf"
            else:
                comp_supertask_kind = "fx"
        if comp_supertask_kind == "dfg":
            logger.info("Using dfg as comp_supertask_kind")
        LLM.__verify_comp_supertask_kind(comp_supertask_kind)

        beam_size_or_none = (
            None
            if self.generator_config.kv_cache_sharing_across_beams_config is None
            else self.generator_config.kv_cache_sharing_across_beams_config.beam_width
        )

        # Get Tokenizer
        self.tokenizer = get_tokenizer(
            model,
            tokenizer,
            tokenizer_mode,
            trust_remote_code=trust_remote_code,
            **kwargs,
        )

        # Please refer to an example at https://huggingface.co/docs/transformers/en/main_classes/text_generation#transformers.GenerationMixin.greedy_search.example
        # Some models like GPT-2 may not have pad_token_id. BTW, when we run a batch of sequence generations,
        # We must need pad_token_id to fill the batch with pad. With Hugging Face Transformers,
        # users should handle this issue. Our goal is to provide a better useability for users.
        # We handle this issue within LLM class.
        self.model_config["pad_token_id"] = self.model_config["eos_token_id"]

        if speculative_model is not None:
            # mimic vllm's behavior
            num_speculative_tokens = num_speculative_tokens or self.model_config.get("n_predict")
            if num_speculative_tokens is None:
                raise ValueError(
                    "`speculative_model` is given, but `num_speculative_tokens` is not given and cannot be obtained from model config."
                )

        compiler_config_context = CompilerConfigContext(
            model_metadata=self.model_metadata,
            beam_size=beam_size_or_none,
            compiler_config_overrides=compiler_config_overrides,
        )

        if _pipelines_with_metadata is not None:
            # FIXME: This pass exists only for supporting `LLM.from_artifacts` and `LLM.load_artifact` API.

            # Only pick pipelines for given buckets.
            buckets_with_output_size_to_include = set(buckets_with_output_size)

            pipelines_with_bucket_info = [
                (
                    BucketWithOutputLogitsSize(
                        _get_bucket_from_pipeline_name(pipeline_with_meta.pipeline.name),
                        pipeline_with_meta.metadata.output_logits_size,
                    ),
                    pipeline_with_meta,
                )
                for pipeline_with_meta in _pipelines_with_metadata
            ]

            pipelines_with_meta: List[PipelineWithMetadata] = [
                pipeline_with_meta
                for bucket_with_output_size, pipeline_with_meta in pipelines_with_bucket_info
                if bucket_with_output_size in buckets_with_output_size_to_include
            ]
            if len(pipelines_with_meta) != len(buckets_with_output_size_to_include):
                needed_buckets = buckets_with_output_size_to_include - set(
                    bucket for bucket, _ in pipelines_with_bucket_info
                )
                raise ValueError(
                    f"Some needed buckets do not exist in the artifacts.\n{needed_buckets}"
                )

            # replace devices in pipelines
            for pipeline_with_meta in pipelines_with_meta:
                pipeline = pipeline_with_meta.pipeline
                if len(pipeline.devices) != len(first_dp_subgroup_devices):
                    raise ValueError(
                        f"The number of devices in the pipeline {pipeline.devices} is different from the number of devices in the first dp subgroup {first_dp_subgroup_devices}."
                    )

                pipeline.devices = {
                    DeviceId(str(i)): dev for i, dev in enumerate(first_dp_subgroup_devices)
                }

            self.pipelines_with_meta = pipelines_with_meta
        else:
            if self.model_metadata.need_quant_artifacts or qparam_path or qformat_path:
                if not (qparam_path and qformat_path):
                    raise ValueError(
                        "To use quantized model, `qparam_path` and `qformat_path` should be given."
                    )
                if not (os.path.exists(qparam_path) and os.path.exists(qformat_path)):
                    raise ValueError(
                        "`qparam_path` or `qformat_path` is invalid. The file does not exist."
                    )
                if self.is_generative_model:
                    assert kv_cache_dtype
                    # Check model's kv cache dtype complies with description of qformat file.
                    self.__verify_kv_cache_dtype_with_qformat(
                        kv_cache_dtype, qformat_path, self.model_metadata
                    )

            model_ = ModelCreationInfo(
                self.model_metadata,
                use_random_weight,
                seed,
                qformat_path=qformat_path,
                qparam_path=qparam_path,
                quant_ckpt_file_path=quant_ckpt_file_path,
            )

            if artifacts_export_path:
                os.environ["FURIOSA_COMPILE_DUMP_PATH"] = str(artifacts_export_path)

            try:
                if trust_remote_code:
                    prestep_for_remote_code_model(model_.metadata, num_pipeline_builder_workers)

                self.build_all_pipelines(
                    model_,
                    buckets_with_output_size,
                    first_dp_subgroup_devices,
                    backend,
                    comp_supertask_kind,
                    one_supertask_per_device,
                    use_blockwise_compile,
                    _embedding_layer_as_single_block,
                    do_decompositions_for_model_rewrite,
                    kv_cache_dtype.to_torch_dtype() if kv_cache_dtype else None,
                    sparse_select_version,
                    num_pipeline_builder_workers,
                    num_compile_workers,
                    embed_all_constants_into_graph,
                    num_blocks_per_supertask,
                    num_blocks_per_pp_stage,
                    param_file_path,
                    param_saved_format,
                    compiler_config_context,
                    cache_dir,
                    _cleanup,
                )

                # Save artifacts before copying pipelines according to `data_parallelism_size`.
                if artifacts_export_path:
                    self._save_engine_artifacts(
                        artifacts_export_path,
                        comp_supertask_kind,
                        devices,
                    )
            finally:
                os.environ.pop("FURIOSA_COMPILE_DUMP_PATH", None)

        # If data parallelism is used, replicate pipelines for each entity data parallelism subgroup.
        if data_parallel_size > 1:
            self.pipelines_with_meta: List[PipelineWithMetadata] = [  # type: ignore[no-redef]
                PipelineWithMetadata(
                    pipeline_with_meta.pipeline.shallow_copy_with_replaced_devices(
                        dict(zip_equal(first_dp_subgroup_devices, flattened_pp_tp_group))  # type: ignore[arg-type]
                    ),
                    pipeline_with_meta.metadata,
                )
                for pipeline_with_meta, flattened_pp_tp_group in product(
                    self.pipelines_with_meta, normalized_dev_mesh
                )
            ]

        if speculative_model:
            if kv_cache_sharing_across_beams_config:
                raise NotImplementedError(
                    "Speculative decoding with beam search is not supported yet."
                )

            if artifacts_export_path:
                speculative_model_artifacts_export_path = os.path.join(
                    artifacts_export_path, "speculative_model"
                )
            else:
                speculative_model_artifacts_export_path = None

            if isinstance(speculative_model, LLM):
                draft_llm = speculative_model
                # TODO: do we need to check given arguments match?
            elif isinstance(speculative_model, str):
                draft_llm = LLM(
                    speculative_model,
                    task_type=self.model_metadata.task_type,
                    llm_config=speculative_model_llm_config,
                    qformat_path=speculative_model_qformat_path,
                    qparam_path=speculative_model_qparam_path,
                    quant_ckpt_file_path=speculative_model_quant_ckpt_file_path,
                    hf_overrides=speculative_model_config,
                    bucket_config=speculative_model_bucket_config,
                    max_seq_len_to_capture=max_seq_len_to_capture,
                    # TODO:Expose parallel config for specualtive model later?
                    tensor_parallel_size=speculative_draft_tensor_parallel_size
                    or tensor_parallel_size,
                    pipeline_parallel_size=speculative_draft_pipeline_parallel_size
                    or pipeline_parallel_size,
                    data_parallel_size=speculative_draft_data_parallel_size or data_parallel_size,
                    # NOTE: tokenizer is shared between main model and specualtive model.
                    seed=seed,
                    devices=devices,
                    # Use same configs of big model.
                    # TODO: do we need to expose param_file_path for the speculative model?
                    do_decompositions_for_model_rewrite=do_decompositions_for_model_rewrite,
                    comp_supertask_kind=comp_supertask_kind,
                    cache_dir=cache_dir,
                    backend=backend,
                    use_blockwise_compile=use_blockwise_compile,
                    num_blocks_per_supertask=num_blocks_per_supertask,
                    num_blocks_per_pp_stage=speculative_draft_num_blocks_per_pp_stage
                    or num_blocks_per_pp_stage,
                    embed_all_constants_into_graph=embed_all_constants_into_graph,
                    paged_attention_block_size=paged_attention_block_size,
                    kv_cache_sharing_across_beams_config=None,
                    scheduler_config=scheduler_config,
                    packing_type=packing_type,
                    # TODO: Should we expose this?
                    compiler_config_overrides=compiler_config_overrides,
                    # TODO: Should we expose this?
                    use_random_weight=use_random_weight,
                    num_pipeline_builder_workers=num_pipeline_builder_workers,
                    num_compile_workers=num_compile_workers,
                    skip_engine=True,
                    artifacts_export_path=speculative_model_artifacts_export_path,
                    _optimize_logit_shape=_optimize_logit_shape,
                )
            else:
                raise ValueError(
                    "`speculative_model` must be either a pretrained model id or an instance of LLM."
                )
            self.draft_pipelines_with_meta: Optional[List[PipelineWithMetadata]] = (
                draft_llm.pipelines_with_meta
            )
            self.draft_generator_config: Optional[GeneratorConfig] = draft_llm.generator_config
            self.speculative_model_config: Optional[PretrainedConfig] = draft_llm.model_config
        else:
            self.draft_pipelines_with_meta = None
            self.draft_generator_config = None
            self.speculative_model_config = None

        # for e2e testing purpose, it allows to skip to initialize the engine
        if not skip_engine:
            try:
                from furiosa.native_runtime.llm import NativeLLMEngine  # type: ignore
            except ImportError:
                logger.error(
                    "NativeLLMEngine is not available. Please make sure that the furiosa-native-runtime is installed.\n"
                    'You can install furiosa-native-runtime by running `pip install furiosa-llm`.\n'
                    "If you want to use the LLM without the native runtime, you can set `skip_engine=True` in the constructor."
                )
                raise

            # FIXME: remove this conversion after fixing generator to support non-slice model class with dynamic slice.
            if _optimize_logit_shape:
                if (
                    self.generator_config.model_qname
                    == "furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM"
                ):
                    self.generator_config.model_qname = (
                        "furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM"
                    )
                elif (
                    self.generator_config.model_qname
                    == "furiosa_llm_models.llama3.symbolic.mlperf_submission.LlamaForCausalLM"
                ):
                    self.generator_config.model_qname = "furiosa_llm_models.llama3.symbolic.mlperf_submission_slice.LlamaForCausalLM"
                elif (
                    self.generator_config.model_qname
                    == "furiosa_llm_models.llama.symbolic.mlperf_submission.LlamaForCausalLM"
                ):
                    self.generator_config.model_qname = (
                        "furiosa_llm_models.llama.symbolic.mlperf_submission_slice.LlamaForCausalLM"
                    )
                elif (
                    self.generator_config.model_qname
                    == "furiosa_llm_models.llama3.symbolic.aramco_specdec.LlamaForCausalLM"
                ):
                    self.generator_config.model_qname = "furiosa_llm_models.llama3.symbolic.aramco_specdec_slice_integrated.LlamaForCausalLM"

            self.engine = NativeLLMEngine(
                self.pipelines_with_meta,
                self.draft_pipelines_with_meta,
                self.generator_config,
                self.draft_generator_config,
                scheduler_config=self.scheduler_config,
                backend=backend.value,
                hf_config=self.model_config,
                draft_hf_config=self.speculative_model_config,
            )

    @classmethod
    def load_artifacts(
        cls,
        path: Union[str, os.PathLike],
        **kwargs,
    ) -> "LLM":
        """Instantiate LLM from saved artifacts without quantization and compilation.

        Please note that this method is being deprecated. Use `load_artifact` instead.

        Args:
            path: A path to artifacts to load.
            devices: The devices to run the model. It can be a single device or a list of devices.
                Each device can be either "npu:X" or "npu:X:\*" where X is a specific device index.
                If not given, all available devices will be used.
            data_parallel_size: The size of the data parallelism group. If not given, it will be inferred from
                total available PEs and other parallelism degrees.
            pipeline_parallel_size : The size of the pipeline parallelism. The argument is valid only for artifacts that use blockwise compilation.
            num_blocks_per_pp_stage: The number of transformer blocks per each pipeline parallelism stage.
                The argument is valid only for artifacts that use blockwise compilation. If only `pipeline_parallel_size` is provided, transformer blocks will be
                distributed equally.
            bucket_config: Config for bucket generating policy. If not given, all buckets in the artifacts will be used.
            scheduler_config: Configuration for the scheduler, allowing to maximum number of tasks which can be queued to HW, maximum number of samples
                that can be processed by the scheduler, and ratio of spare blocks that are reserved by scheduler. If this is not given, scheduler config
                saved in the artifacts will be used.
            speculative_model: Specualtive model for speculative decoding. Should be provided either as an artifact path or as an LLM instance.
            speculative_draft_data_parallel_size: The size of the data parallelism for running speculative model.
                If not given, it will following the value for the target model.
                This value will be ignored if `speculative_model` is given as `LLM` instance.
            speculative_draft_pipeline_parallel_size: The size of the pipeline parallelism for running speculative model.
                The argument is valid only for artifacts that use blockwise compilation.
                If not given, it will following the value for the target model.
                This value will be ignored if `speculative_model` is given as `LLM` instance.
            speculative_draft_num_blocks_per_pp_stage: The number of transformer blocks per each pipeline parallelism stage for running speculative model.
                The argument is valid only for artifacts that use blockwise compilation.
                If not given, it will following the value for the target model.
                In anyway if only `speculative_draft_pipeline_parallel_size` is provided, transformer blocks of speculative model will be distributed equally.
                This value will be ignored if `speculative_model` is given as `LLM` instance.
            speculative_model_paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store for speculative model.
                This argument must be given if speculative model uses paged attention.
                This value will be ignored if `speculative_model` is given as `LLM` instance.
            skip_speculative_model_load: If `True`, artifact will be loaded without speculative decoding.
            tokenizer: The name or path of a HuggingFace Transformers tokenizer.
            tokenizer_mode: The tokenizer mode. "auto" will use the fast tokenizer
                if available, and "slow" will always use the slow tokenizer.
            seed: The seed to initialize the random number generator for sampling.
            cache_dir: The cache directory for all generated files for this LLM instance.
                When its value is ``None``, caching is disabled. The default is "$HOME/.cache/furiosa/llm".
            skip_engine: If True, the native runtime engine will not be initialized. This is useful when you need
                the pipelines for other purposes than running them with the engine.
        """
        logger.warning(
            "`LLM.load_artifacts()` is being deprecated. Use `LLM.load_artifact()` instead."
        )
        return cls.load_artifact(path, **kwargs)

    @classmethod
    def _load_model_artifact(
        cls,
        model_artifact: ModelArtifact,
        pipelines: Sequence[Pipeline],
        # Runtime Configuration
        devices: Sequence[Device],
        scheduler_config: SchedulerConfig,
        prefill_chunk_size_from_artifact: Optional[int],
        data_parallel_size: Optional[int] = None,
        pipeline_parallel_size: Optional[int] = None,
        num_blocks_per_pp_stage: Optional[Sequence[int]] = None,
        bucket_config: Optional[BucketConfig] = None,
        # Other Configuration
        tokenizer: Optional[Union[PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
        tokenizer_mode: TokenizerModeType = "auto",
        seed: Optional[int] = None,
        cache_dir: os.PathLike = CACHE_DIR,
        skip_engine: bool = False,
        speculative_model: Optional["LLM"] = None,
        _artifact_id: str = "NO_ARTIFACT_ID",
        **kwargs,
    ) -> "LLM":

        assert not scheduler_config.prefill_chunk_size

        if pipeline_parallel_size and num_blocks_per_pp_stage:
            raise ValueError(
                "Only one of `pipeline_parallel_size` or `num_blocks_per_pp_stage` "
                "should be given as input, not both."
            )

        generator_config = model_artifact.generator_config
        model_metadata = ModelMetadataForArtifact.from_metadata(
            model_artifact.model_metadata, model_artifact.hf_config, generator_config.model_qname
        )
        model_metadata.trust_remote_code = False

        model_rewriting_config = model_artifact.model_rewriting_config
        parallel_config = model_artifact.parallel_config
        max_prompt_len = kwargs.pop("max_prompt_len", model_artifact.max_prompt_len)

        if not bucket_config:
            prefill_buckets = []
            decode_buckets = []

            for bucket in generator_config.buckets:
                if bucket.is_prefill:
                    prefill_buckets.append(bucket)
                elif bucket.is_decode and bucket.input_ids_size == 1:
                    decode_buckets.append(bucket)
                else:
                    # Bucket for speculative decoding.
                    # speculative_decoding_buckets.append(bucket)
                    pass

                bucket_config = ManualBucketConfig(
                    prefill_buckets=[
                        (bucket.batch_size, bucket.attention_size) for bucket in prefill_buckets
                    ],
                    decode_buckets=[
                        (bucket.batch_size, bucket.attention_size) for bucket in decode_buckets
                    ],
                )

        # Find the max attention_size from the pipelines' buckets
        if isinstance(bucket_config, ManualBucketConfig):
            if bucket_config.decode_buckets:
                assert model_metadata.is_generative_model
                max_seq_len_to_capture = max([bucket[1] for bucket in bucket_config.decode_buckets])
            else:
                max_seq_len_to_capture = max(
                    [bucket[1] for bucket in bucket_config.prefill_buckets]
                )
        elif isinstance(bucket_config, MinimalBucketConfig):
            max_seq_len_to_capture = bucket_config.max_seq_len
        else:
            raise ValueError("`bucket_config` must be an instance of BucketConfig.")

        if model_artifact.pipeline_metadata_list is None:
            # For B.C
            pipelines_with_metadata = [
                PipelineWithMetadata(
                    pipeline, get_default_pipeline_metadata(model_metadata, bucket)
                )
                for bucket, pipeline in zip_equal(generator_config.buckets, pipelines)
            ]
        else:
            pipelines_with_metadata = [
                PipelineWithMetadata(pipeline, pipeline_metadata)
                for pipeline, pipeline_metadata in zip_equal(
                    pipelines, model_artifact.pipeline_metadata_list
                )
            ]

        # Overriding in PP size
        overridden_pp_size, overridden_dp_size = None, None
        if num_blocks_per_pp_stage or pipeline_parallel_size:
            if not model_rewriting_config.use_blockwise_compile:
                raise ValueError(
                    "Pipeline parallelism overriding is supported only for blockwise-compiled artifacts."
                )
            # if `pipeline_parallel_size` is not None, `num_blocks_per_pp_stage` must be list of int
            overridden_pp_size = (
                pipeline_parallel_size
                if pipeline_parallel_size
                else len(num_blocks_per_pp_stage)  # type: ignore[arg-type]
            )
        else:
            # `devices` may refer to the currently available ones or those specified by the user.
            if len(devices) >= model_artifact.parallel_config.pipeline_parallel_size:
                overridden_pp_size = model_artifact.parallel_config.pipeline_parallel_size
            else:
                logger.info(
                    "The number of available devices is smaller than the artifact’s pipeline_parallel_size. Adjusting "
                    "pipeline_parallel_size to match the total available devices, which may lead to performance degradation."
                )
                overridden_pp_size = len(devices)

        dev_mesh = get_device_mesh(
            devices,
            parallel_config.tensor_parallel_size,
            overridden_pp_size,
            data_parallel_size,
        )
        overridden_dp_size = len(dev_mesh)

        assert overridden_pp_size
        assert overridden_dp_size

        if (
            overridden_pp_size != model_artifact.parallel_config.pipeline_parallel_size
            or num_blocks_per_pp_stage
        ):
            # Perform PP overriding if the specified PP size differs from the one used during build
            # or if num_blocks_per_pp_stage is provided.
            pipelines_with_metadata = [
                PipelineWithMetadata(
                    override_pp_size_on_pipeline(
                        pipeline,
                        devices=dev_mesh[0],
                        pipeline_parallel_size=(
                            overridden_pp_size if not num_blocks_per_pp_stage else None
                        ),
                        num_blocks_per_pp_stage=num_blocks_per_pp_stage,
                    ),
                    meta,
                )
                for pipeline, meta in pipelines_with_metadata
            ]

        assert devices

        return cls(
            model=model_metadata.pretrained_id,
            task_type=model_metadata.task_type,
            llm_config=model_metadata.llm_config,
            hf_overrides=model_metadata.hf_configs,
            bucket_config=bucket_config,
            num_speculative_tokens=generator_config.num_speculative_tokens,
            max_seq_len_to_capture=max_seq_len_to_capture,
            max_prompt_len=max_prompt_len,
            tensor_parallel_size=parallel_config.tensor_parallel_size,
            data_parallel_size=overridden_dp_size,
            pipeline_parallel_size=overridden_pp_size,
            tokenizer=tokenizer,
            tokenizer_mode=tokenizer_mode,
            seed=seed,
            devices=devices,
            do_decompositions_for_model_rewrite=model_rewriting_config.do_decompositions_for_model_rewrite,
            comp_supertask_kind="edf",
            cache_dir=cache_dir,
            backend=LLMBackend.FURIOSA_RT_V2,
            use_blockwise_compile=model_rewriting_config.use_blockwise_compile,
            num_blocks_per_pp_stage=num_blocks_per_pp_stage,
            num_blocks_per_supertask=model_rewriting_config.num_blocks_per_supertask,
            embed_all_constants_into_graph=model_rewriting_config.embed_all_constants_into_graph,
            kv_cache_sharing_across_beams_config=generator_config.kv_cache_sharing_across_beams_config,
            # The `prefill_chunk_size` is properly set in `scheduler_config`,
            # so `prefill_chunk_size` should not be passed to `LLM.__init__` as independent argument.
            scheduler_config=scheduler_config,
            packing_type=generator_config.packing_type,
            skip_engine=skip_engine,
            speculative_model=speculative_model,
            prefill_chunk_size=prefill_chunk_size_from_artifact,
            _pipelines_with_metadata=pipelines_with_metadata,
            _optimize_logit_shape=model_rewriting_config.optimize_logit_shape,
            _model_metadata=model_metadata,
            _unpadded_vocab_size=generator_config.unpadded_vocab_size,
            _artifact_id=_artifact_id,
            **kwargs,
        )

    @classmethod
    def load_artifact(
        cls,
        model_id_or_path: Union[str, os.PathLike],
        *,
        # Repo Configuration
        revision: Optional[str] = None,
        # Runtime Configuration
        devices: Optional[Union[str, Sequence[Device]]] = None,
        data_parallel_size: Optional[int] = None,
        pipeline_parallel_size: Optional[int] = None,
        num_blocks_per_pp_stage: Optional[Sequence[int]] = None,
        bucket_config: Optional[BucketConfig] = None,
        scheduler_config: Optional[SchedulerConfig] = None,
        # Speculative-decoding related Configuration
        speculative_model: Optional[Union[str, os.PathLike, "LLM"]] = None,
        speculative_draft_data_parallel_size: Optional[int] = None,
        speculative_draft_pipeline_parallel_size: Optional[int] = None,
        speculative_draft_num_blocks_per_pp_stage: Optional[Sequence[int]] = None,
        skip_speculative_model_load: bool = False,
        # Other Configuration
        tokenizer: Optional[Union[PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
        tokenizer_mode: TokenizerModeType = "auto",
        seed: Optional[int] = None,
        cache_dir: os.PathLike = CACHE_DIR,
        skip_engine: bool = False,
        **kwargs,
    ) -> "LLM":
        """Instantiate LLM from saved artifacts without quantization and compilation.

        Args:
            model_id_or_path: A path to furiosa llm engine artifact or a HuggingFace model id.
            revision: The revision of the model, if `model_id_or_path` is a HuggingFace model id.
            devices: The devices to run the model. It can be a single device or a list of devices.
                Each device can be either "npu:X" or "npu:X:\*" where X is a specific device index.
                If not given, all available devices will be used.
            data_parallel_size: The size of the data parallelism group. If not given, it will be inferred from
                total available PEs and other parallelism degrees.
            pipeline_parallel_size : The size of the pipeline parallelism. The argument is valid only for artifacts that use blockwise compilation.
            num_blocks_per_pp_stage: The number of transformer blocks per each pipeline parallelism stage.
                The argument is valid only for artifacts that use blockwise compilation. If only `pipeline_parallel_size` is provided, transformer blocks will be
                distributed equally.
            bucket_config: Config for bucket generating policy. If not given, all buckets in the artifacts will be used.
            scheduler_config: Configuration for the scheduler, allowing to maximum number of tasks which can be queued to HW, maximum number of samples
                that can be processed by the scheduler, and ratio of spare blocks that are reserved by scheduler. If this is not given, scheduler config
                saved in the artifacts will be used.
            speculative_model: Speculative model for speculative decoding. Should be provided either as an artifact path or as an LLM instance.
                Note that speculative decoding is an experimental feature and may lead to unstable behavior.
            speculative_draft_data_parallel_size: The size of the data parallelism for running speculative model.
                If not given, it will follow the value of the target model.
                This value will be ignored if `speculative_model` is given as `LLM` instance.
                Note that speculative decoding is an experimental feature and may lead to unstable behavior.
            speculative_draft_pipeline_parallel_size: The size of the pipeline parallelism for running speculative model.
                The argument is valid only for artifacts that use blockwise compilation.
                If not given, it will follow the value of the target model.
                This value will be ignored if `speculative_model` is given as `LLM` instance.
                Note that speculative decoding is an experimental feature and may lead to unstable behavior.
            speculative_draft_num_blocks_per_pp_stage: The number of transformer blocks per each pipeline parallelism stage for running speculative model.
                The argument is valid only for artifacts that use blockwise compilation.
                If not given, it will follow the value of the target model.
                In anyway if only `speculative_draft_pipeline_parallel_size` is provided, transformer blocks of speculative model will be distributed equally.
                This value will be ignored if `speculative_model` is given as `LLM` instance.
                Note that speculative decoding is an experimental feature and may lead to unstable behavior.
            skip_speculative_model_load: If `True`, artifact will be loaded without speculative decoding.
            tokenizer: The name or path of a HuggingFace Transformers tokenizer.
            tokenizer_mode: The tokenizer mode. "auto" will use the fast tokenizer
                if available, and "slow" will always use the slow tokenizer.
            seed: The seed to initialize the random number generator for sampling.
            cache_dir: The cache directory for all generated files for this LLM instance.
                When its value is ``None``, caching is disabled. The default is "$HOME/.cache/furiosa/llm".
            skip_engine: If True, the native runtime engine will not be initialized. This is useful when you need
                the pipelines for other purposes than running them with the engine.
        """

        try:
            revision = revision or _resolve_default_hf_revision(
                model_id_or_path, FURIOSA_LLM_VERSION
            )
            path = _get_path_or_hf_download(model_id_or_path, revision, ModelKind.ARTIFACT)
        except UnexpectedModelKind as e:
            raise ValueError(
                f"LLM.load_artifact() expects an artifact, "
                f"but {model_id_or_path} has {', '.join([kind.name for kind in e.actual_kinds])}."
            )

        artifact_path = f"{path}/artifact.json"

        # check path is valid
        if not os.path.exists(artifact_path):
            raise ValueError("This artifacts is not valid.")

        artifact = Artifact.load(artifact_path)
        # Load all saved pipelines
        pipelines = cls.__load_pipelines(
            path,
            try_from_lir=False,
            try_from_dfg=False,
            cache_dir=cache_dir,
            model_artifact=artifact.model,
        )

        if not devices:
            devices = _get_available_devices()

        if isinstance(devices, str):
            devices = parse_devices_str(devices)

        if scheduler_config and scheduler_config.prefill_chunk_size is not None:
            raise ValueError(
                "Specifying prefill_chunk_size in the scheduler configuration is not allowed."
            )

        if (not artifact.model.generator_config.num_speculative_tokens) and (
            artifact.speculative_model or speculative_model
        ):
            raise ValueError(
                "Speculative decoding can only be enabled only if "
                "`num_speculative_tokens` was given in artifact build via `ArtifactBuilder`"
            )

        if skip_speculative_model_load or (
            artifact.speculative_model is None and speculative_model is None
        ):
            # disabling speculative decoding or run the artifact as is
            speculative_model_llm = None
        elif isinstance(speculative_model, LLM):
            # replacing speculative model when given as `LLM` instance
            assert artifact.model.generator_config.num_speculative_tokens
            speculative_model_llm = speculative_model
        else:
            assert artifact.model.generator_config.num_speculative_tokens
            if isinstance(speculative_model, str | os.PathLike):
                # replacing speculative model when given as path to speculative model artifact
                speculative_model_artifact = Artifact.load(
                    f"{speculative_model}/artifact.json"
                ).model
                speculative_model_path = speculative_model
            else:
                assert artifact.speculative_model
                # Running the artifact as is since it already contains
                # the speculative model artifact within itself.
                speculative_model_artifact = artifact.speculative_model
                speculative_model_path = path

            speculative_model_pipelines = cls.__load_pipelines(
                speculative_model_path,
                try_from_lir=False,
                try_from_dfg=False,
                cache_dir=cache_dir,
                model_artifact=speculative_model_artifact,
            )
            # TODO : currently, artifact is loaded with default value of scheduler config
            # defined in `SchedulerConfig` (other than prefill_chunk_size) by default.
            # Later, this should be replaced by other `SchedulerConfig`
            # optimized to current device environment
            speculative_model_llm = LLM._load_model_artifact(
                model_artifact=speculative_model_artifact,
                pipelines=speculative_model_pipelines,
                devices=devices,
                scheduler_config=scheduler_config or SchedulerConfig(),
                prefill_chunk_size_from_artifact=None,
                data_parallel_size=speculative_draft_data_parallel_size or data_parallel_size,
                pipeline_parallel_size=speculative_draft_pipeline_parallel_size
                or pipeline_parallel_size,
                num_blocks_per_pp_stage=speculative_draft_num_blocks_per_pp_stage
                or num_blocks_per_pp_stage,
                tokenizer=tokenizer,
                tokenizer_mode=tokenizer_mode,
                seed=seed,
                cache_dir=cache_dir,
                skip_engine=skip_engine,
                **kwargs,
            )

        assert isinstance(speculative_model_llm, LLM) or speculative_model_llm is None

        # TODO : currently, artifact is loaded with default value of scheduler config
        # defined in `SchedulerConfig` (other than prefill_chunk_size) by default.
        # Later, this should be replaced by other `SchedulerConfig`
        # optimized to current device environment
        target_model_llm = LLM._load_model_artifact(
            artifact.model,
            pipelines,
            devices=devices,
            scheduler_config=scheduler_config or SchedulerConfig(),
            prefill_chunk_size_from_artifact=artifact.prefill_chunk_size,
            data_parallel_size=data_parallel_size,
            pipeline_parallel_size=pipeline_parallel_size,
            num_blocks_per_pp_stage=num_blocks_per_pp_stage,
            bucket_config=bucket_config,
            # Other Configuration
            tokenizer=tokenizer,
            tokenizer_mode=tokenizer_mode,
            seed=seed,
            cache_dir=cache_dir,
            skip_engine=skip_engine,
            speculative_model=speculative_model_llm,
            _artifact_id=artifact.metadata.artifact_id,
            **kwargs,
        )

        return target_model_llm

    @classmethod
    def from_artifacts(
        cls,
        path: Union[str, os.PathLike],
        bucket_config: Optional[BucketConfig] = None,
        speculative_model: Optional["LLM"] = None,
        num_speculative_tokens: Optional[int] = None,
        speculative_model_bucket_config: Optional[BucketConfig] = None,
        use_speculative_decoding_if_possible: bool = True,
        data_parallel_size: Optional[int] = None,
        pipeline_parallel_size: Optional[int] = None,
        num_blocks_per_pp_stage: Optional[Sequence[int]] = None,
        tokenizer: Optional[Union[PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
        tokenizer_mode: TokenizerModeType = "auto",
        seed: Optional[int] = None,
        devices: Optional[Union[str, Sequence[Device]]] = None,
        cache_dir: os.PathLike = CACHE_DIR,
        backend: Optional[LLMBackend] = None,
        paged_attention_num_blocks: Optional[int] = None,
        scheduler_config: Optional[SchedulerConfig] = None,
        packing_type: Literal["IDENTITY"] = "IDENTITY",
        skip_engine: bool = False,
        *,
        _cleanup=True,
        **kwargs,
    ) -> "LLM":
        """Instantiate LLM from saved artifacts without quantization and compilation.

        Args:
            path: A path to artifacts to load.
            bucket_config: Config for bucket generating policy. If not given, all buckets in the artifacts will be used.
            speculative_model: Draft model for speculative decoding.
            num_speculative_tokens: The number of tokens that speculative model will generate speculatively during each iteration of the decoding process.
            speculative_model_bucket_config: Bucket generating config for speculative_model. If not given,
                all speculative model buckets (if exists) in the artifacts will be used.
            use_speculative_decoding_if_possible: If True, speculative decoding will be used if possible
                (`speculative_model` is given or there's artifacts for speculative model in the artifacts.).
                Otherwise, speculative decoding will not be used.
            data_parallel_size: The size of the data parallelism group. If not given, it will be inferred from
                total available PEs and other parallelism degrees.
            pipeline_parallel_size : The size of the pipeline parallelism. The argument is valid only for artifacts that use blockwise compilation.
            num_blocks_per_pp_stage: The number of transformer blocks per each pipeline parallelism stage.
                The argument is valid only for artifacts that use blockwise compilation. If only `pipeline_parallel_size` is provided, transformer blocks will be
                distributed equally.
            tokenizer: The name or path of a HuggingFace Transformers tokenizer.
            tokenizer_mode: The tokenizer mode. "auto" will use the fast tokenizer
                if available, and "slow" will always use the slow tokenizer.
            seed: The seed to initialize the random number generator for sampling.
            devices: The devices to run the model. It can be a single device or a list of devices.
                Each device can be either "npu:X" or "npu:X:\*" where X is a specific device index.
                If not given, devices saved in the artifacts will be used.
            cache_dir: The cache directory for all generated files for this LLM instance.
                When its value is ``None``, caching is disabled. The default is "$HOME/.cache/furiosa/llm".
            backend: The backend implementation to run forward() of a model for the LLM.
                The default is LLMBackend.TORCH_PIPELINE_RUNNER.
            paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store. This argument must be given
                if model uses paged attention.
            scheduler_config: Configuration for the scheduler, allowing to maximum number of tasks which can be queued to HW, maximum number of samples
                that can be processed by the scheduler, and ratio of spare blocks that are reserved by scheduler. If this is not given, scheduler config
                saved in the artifacts will be used.
            speculative_model_paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store for the speculative model. This argument must be given
                if the speculative model uses paged attention.
            packing_type: Packing algorithm. Possible values are "IDENTITY" only for now
            skip_engine: If True, the native runtime engine will not be initialized. This is useful when you need
                the pipelines for other purposes than running them with the engine.
        """

        if not os.path.exists(f"{path}/ready"):
            raise ValueError("This artifacts is not valid.")

        if pipeline_parallel_size and num_blocks_per_pp_stage:
            raise ValueError(
                "Only one of `pipeline_parallel_size` or `num_blocks_per_pp_stage` should be given as input, not both."
            )
        # Load configs
        generator_config = GeneratorConfig.load(f"{path}/generator_config.json")
        scheduler_config_ = SchedulerConfig.load(f"{path}/scheduler_config.json")

        # Use saved scheduler config if not given.
        scheduler_config = scheduler_config or scheduler_config_

        with open(f"{path}/model_metadata.json", "r") as fp:
            model_metadata = ModelMetadata.model_validate_json(fp.read())
        with open(f"{path}/model_rewriting_config.json") as fp:
            model_rewriting_config = ModelRewritingConfig.model_validate_json(fp.read())
        with open(f"{path}/parallel_config.json") as fp:
            parallel_config = ParallelConfig.model_validate_json(fp.read())

        try:
            with open(f"{path}/pipelines_metadata.json", "r") as fp:
                pipelines_metadata = [
                    PipelineMetadata.model_validate(metadata) for metadata in json.load(fp)
                ]
        except FileNotFoundError:
            # PipelineMetadata doesn't exist. Get information from model metadata and bucket.
            pipelines_metadata = [
                get_default_pipeline_metadata(
                    model_metadata,
                    bucket,
                )
                for bucket in generator_config.buckets
            ]

        with open(f"{path}/other_config.json") as fp:
            other_configs = json.load(fp)

        try_from_lir = os.environ.get("LLM_ENGINE_ARTIFACTS_TRY_FROM_LIR", "0") == "1"
        try_from_dfg = os.environ.get("LLM_ENGINE_ARTIFACTS_TRY_FROM_DFG", "0") == "1"

        # Load all saved pipelines
        pipelines = cls.__load_pipelines(
            path,
            try_from_lir=try_from_lir,
            try_from_dfg=try_from_dfg,
            cache_dir=cache_dir,
        )

        if (
            get_list_with_no_dup_with_order_preserved(
                [_get_bucket_from_pipeline_name(pipeline.name) for pipeline in pipelines]
            )
            != generator_config.buckets
        ):
            raise ValueError(
                "Saved pipeline order does not comply with buckets in generator config."
            )

        pipelines_with_metadata = [
            PipelineWithMetadata(pipeline, metadata)
            for pipeline, metadata in zip_equal(pipelines, pipelines_metadata)
        ]

        paged_attention_num_blocks = paged_attention_num_blocks or getattr(
            generator_config.paged_attention_config, "num_blocks", None
        )
        paged_attention_block_size = getattr(
            generator_config.paged_attention_config, "block_size", 1
        )
        comp_supertask_kind = other_configs["comp_supertask_kind"]

        if devices is None:
            devices = other_configs.get("devices")
            if devices is None and not os.environ.get(
                "DISABLE_LLM_ENGINE_ARTIFACTS_STRICT_LOAD", False
            ):
                raise ValueError(
                    "Saved devices info is not found in the artifacts. Please provide devices explicitly or set `DISABLE_LLM_ENGINE_ARTIFACTS_STRICT_LOAD=1` to use all available devices."
                )
            if devices:
                devices = [Device(device) for device in devices]
            logger.info(
                f"Device is not given, fall back to devices specified in artifact: {devices}"
            )

        pp_size_to_convey = None
        if num_blocks_per_pp_stage or pipeline_parallel_size:
            if not model_rewriting_config.use_blockwise_compile:
                raise ValueError(
                    "Pipeline parallelism overriding is supported only for blockwise-compiled artifacts."
                )

            if isinstance(devices, str):
                devices = parse_devices_str(devices)
            # if `pipeline_parallel_size` is not None, `num_blocks_per_pp_stage` must be list of int
            pp_size_to_convey = (
                pipeline_parallel_size
                if pipeline_parallel_size
                else len(num_blocks_per_pp_stage)  # type: ignore[arg-type]
            )
            dev_mesh = get_device_mesh(
                devices,
                parallel_config.tensor_parallel_size,
                pp_size_to_convey,
                data_parallel_size,
            )

            pipelines_with_metadata = [
                PipelineWithMetadata(
                    override_pp_size_on_pipeline(
                        pipeline,
                        devices=dev_mesh[0],
                        pipeline_parallel_size=pipeline_parallel_size,
                        num_blocks_per_pp_stage=num_blocks_per_pp_stage,
                    ),
                    metadata,
                )
                for pipeline, metadata in pipelines_with_metadata
            ]

        if use_speculative_decoding_if_possible:
            if speculative_model:
                assert isinstance(speculative_model, LLM)

                if speculative_model_bucket_config:
                    raise NotImplementedError(
                        "`speculative_model_bucket_config` is not supported when "
                    )
            elif os.path.exists(f"{path}/speculative_model"):
                # speculative model exists.
                speculative_model = cls.from_artifacts(
                    f"{path}/speculative_model",
                    bucket_config=speculative_model_bucket_config,
                    seed=seed,
                    devices=devices,
                    cache_dir=cache_dir,
                    packing_type=packing_type,
                    skip_engine=True,
                )
            if num_speculative_tokens:
                if (
                    generator_config.num_speculative_tokens
                    and generator_config.num_speculative_tokens != num_speculative_tokens
                ):
                    raise ValueError(
                        f"`num_speculative_tokens` must be same as saved `num_speculative_tokens` value in artifacts: {num_speculative_tokens} != {generator_config.num_speculative_tokens}"
                    )
                if not speculative_model:
                    raise ValueError(
                        "Speculative model given, but original model artifacts is not for speculative decoding."
                    )
                generator_config.num_speculative_tokens = num_speculative_tokens

            if generator_config.num_speculative_tokens and not speculative_model:
                raise ValueError(
                    "You want to use speculative decoding but speculative model is not given and cannot be loaded."
                )
        else:
            # Don't use speculative decoding.
            if speculative_model:
                logger.warning(
                    "Ignore `speculative_model` because `use_speculative_decoding_if_possible` is False."
                )
            if num_speculative_tokens:
                logger.warning(
                    "Ignore `num_speculative_tokens` because `use_speculative_decoding_if_possible` is False."
                )
            num_speculative_tokens = None
            generator_config.num_speculative_tokens = None

        other_buckets_with_meta = []

        if not bucket_config:
            # If bucket config is not given, load available buckets from the artifacts.
            prefill_buckets_ = []
            decode_buckets_ = []

            for pipeline, meta in pipelines_with_metadata:
                other_buckets_with_meta.append(
                    BucketWithOutputLogitsSize(
                        _get_bucket_from_pipeline_name(pipeline.name),
                        meta.output_logits_size,
                    )
                )

            for bucket in generator_config.buckets:
                if bucket.is_prefill:
                    prefill_buckets_.append(bucket)
                elif bucket.is_decode and bucket.input_ids_size == 1:
                    decode_buckets_.append(bucket)
                else:
                    # Bucket for speculative decoding / chunked prefill.
                    pass

            if num_speculative_tokens:
                # Check all needed verification buckets exist.
                verification_buckets = set(
                    bucket_with_meta.bucket
                    for bucket_with_meta in other_buckets_with_meta
                    if bucket_with_meta.bucket.input_ids_size == num_speculative_tokens + 1
                )

                # There should be verification bucket with same attention size for each decode bucket.
                if any(
                    Bucket(
                        decode_bucket.batch_size,
                        decode_bucket.attention_size,
                        decode_bucket.attention_size - num_speculative_tokens - 1,
                    )
                    not in verification_buckets
                    for decode_bucket in decode_buckets_
                ):
                    raise ValueError(
                        f"There is missing verification buckets in the artifacts. Buckets with input_ids_length {num_speculative_tokens + 1} should exists."
                    )

            prefill_buckets = [
                (bucket.batch_size, bucket.attention_size) for bucket in prefill_buckets_
            ]
            decode_buckets = [
                (bucket.batch_size, bucket.attention_size) for bucket in decode_buckets_
            ]
            bucket_config = ManualBucketConfig(prefill_buckets, decode_buckets)

        # Find the max attention_size from the pipelines' buckets
        if isinstance(bucket_config, ManualBucketConfig):
            if bucket_config.decode_buckets:
                assert model_metadata.is_generative_model
                max_seq_len_to_capture = max([bucket[1] for bucket in bucket_config.decode_buckets])
            else:
                max_seq_len_to_capture = max(
                    [bucket[1] for bucket in bucket_config.prefill_buckets]
                )
        elif isinstance(bucket_config, MinimalBucketConfig):
            max_seq_len_to_capture = bucket_config.max_seq_len
        else:
            raise ValueError("`bucket_config` must be an instance of BucketConfig.")

        return cls(
            model_metadata.pretrained_id,
            task_type=model_metadata.task_type,
            llm_config=model_metadata.llm_config,
            hf_overrides=model_metadata.hf_configs,
            bucket_config=bucket_config,
            speculative_model=speculative_model,
            num_speculative_tokens=generator_config.num_speculative_tokens,
            max_seq_len_to_capture=max_seq_len_to_capture,
            tensor_parallel_size=parallel_config.tensor_parallel_size,
            pipeline_parallel_size=(
                pp_size_to_convey if pp_size_to_convey else parallel_config.pipeline_parallel_size
            ),
            data_parallel_size=data_parallel_size,
            tokenizer=tokenizer,
            tokenizer_mode=tokenizer_mode,
            seed=seed,
            devices=devices,
            do_decompositions_for_model_rewrite=model_rewriting_config.do_decompositions_for_model_rewrite,
            comp_supertask_kind=comp_supertask_kind,
            cache_dir=cache_dir,
            backend=backend,
            use_blockwise_compile=model_rewriting_config.use_blockwise_compile,
            num_blocks_per_pp_stage=num_blocks_per_pp_stage,
            num_blocks_per_supertask=model_rewriting_config.num_blocks_per_supertask,
            embed_all_constants_into_graph=model_rewriting_config.embed_all_constants_into_graph,
            paged_attention_num_blocks=paged_attention_num_blocks,
            paged_attention_block_size=paged_attention_block_size,
            kv_cache_sharing_across_beams_config=generator_config.kv_cache_sharing_across_beams_config,
            scheduler_config=scheduler_config,
            packing_type=packing_type,
            skip_engine=skip_engine,
            _pipelines_with_metadata=pipelines_with_metadata,
            _custom_buckets=other_buckets_with_meta,
            _optimize_logit_shape=model_rewriting_config.optimize_logit_shape,
            _cleanup=_cleanup,
            **kwargs,
        )

    @staticmethod
    def __load_pipelines(
        path: Union[str, os.PathLike],
        try_from_lir: bool,
        try_from_dfg: bool,
        cache_dir: Optional[os.PathLike] = CACHE_DIR,
        model_artifact: Optional[ModelArtifact] = None,
    ) -> List[Pipeline]:
        pipelines = []

        if model_artifact and model_artifact.pipelines:
            for pipeline_dict in model_artifact.pipelines:
                pipeline = Pipeline.from_dict(pipeline_dict)
                pipelines.append(pipeline)
        else:
            for idx in range(len(glob.glob(f"{path}/pipeline.*.json"))):
                pipeline = Pipeline.load(f"{path}/pipeline.{idx}.json")
                pipelines.append(pipeline)

        for pipeline in pipelines:
            blob_to_device: Dict[DataBlobId, Device] = {}
            for _, task in pipeline.supertasks.items():
                if isinstance(task, CompSuperTask) and task.kind == SuperTaskKind.EDF:
                    if task.data_blob is None:
                        continue
                    blob_to_device[task.data_blob] = pipeline.devices[task.device]

            blob_kind = pipeline.get_blob_kind()
            for id, _ in pipeline.blobs.items():
                kind = blob_kind.get(id)
                if kind == SuperTaskKind.FX:
                    with open(f"{path}/{id}.fx", "r") as fp:
                        pipeline.blobs[id] = fp.read()
                elif kind == SuperTaskKind.EDF:
                    try:
                        from furiosa.native_compiler import (  # type: ignore[import]
                            CompiledGraph,
                            compile_from_path,
                        )
                    except ImportError:
                        logger.error("furiosa-native-compiler is required to load EDF format")
                        raise

                    compiler_config_yaml = f"{path}/{id}.config.yaml"
                    device = blob_to_device[id]
                    target_npu = GraphModuleConverter.get_target_npu_from_device(device)
                    # check if:
                    #   - edf file does not exist,
                    #   - try_from_lir is enabled,
                    #   - and lir exists
                    # then, compile lir to edf
                    if (
                        not os.path.exists(f"{path}/{id}.edf")
                        and try_from_lir
                        and os.path.exists(f"{path}/{id}.lir")
                    ):
                        if try_from_dfg:
                            logger.warning(
                                "Both TRY_FROM_LIR and TRY_FROM_DFG are enabled. In this case, TRY_FROM_LIR is prioritized."
                            )
                        compiler_config = try_compiler_config_from_yaml(compiler_config_yaml)
                        logger.info(
                            f"Compiling LIR to EDF for {id} with compiler config {compiler_config}"
                        )
                        out = compile_from_path(
                            f"{path}/{id}.lir",
                            target_npu,
                            target_ir="edf",
                            config=compiler_config,
                            dump_tag=id,
                            dump_path=str(path),
                        )
                        contents = CompiledGraph.serialize(out)
                        with open(f"{path}/{id}.edf", "wb") as fp:  # type: ignore[assignment]
                            fp.write(contents)  # type: ignore[arg-type]

                    # check if:
                    #   - edf file does not exist,
                    #   - try_from_dfg is enabled,
                    #   - and dfg exists
                    # then, compile dfg to edf
                    if (
                        not os.path.exists(f"{path}/{id}.edf")
                        and try_from_dfg
                        and os.path.exists(f"{path}/{id}.dfg")
                    ):
                        compiler_config = try_compiler_config_from_yaml(compiler_config_yaml)
                        logger.info(
                            f"Compiling DFG to EDF for {id} with compiler config {compiler_config}"
                        )
                        out = compile_from_path(
                            f"{path}/{id}.dfg",
                            target_npu,
                            target_ir="edf",
                            config=compiler_config,
                            dump_tag=id,
                            dump_path=str(path),
                            dump_lir=True,
                        )
                        contents = CompiledGraph.serialize(out)
                        with open(f"{path}/{id}.edf", "wb") as fp:  # type: ignore[assignment]
                            fp.write(contents)  # type: ignore[arg-type]

                    with open(f"{path}/{id}.edf", "rb") as fp:
                        pipeline.blobs[id] = CompiledGraph.deserialize(fp.read(), tag=id)  # type: ignore[arg-type, assignment]
                else:
                    raise NotImplementedError(f"SuperTask [{kind}] is not supported to load")

            # Support both cases:
            # 1. param file is located in the artifacts directory
            # 2. param file is located in the global cache directory
            for param_idx, param_file in pipeline.param_files.items():
                # NOTE: param_file.path is already `os.path.basename`d
                path_candidates = (
                    os.path.abspath(f"{path}/{param_file.path}"),
                    os.path.abspath(f"{cache_dir}/param_files/{param_file.path}"),
                )
                for candidate in path_candidates:
                    if os.path.exists(candidate):
                        param_file.path = candidate
                        break
                else:
                    raise FileNotFoundError(
                        f"Param file {param_file.path} is not found in neither artifacts path nor cache directory."
                    )

        return pipelines

    @classmethod
    def compute_prefill_buckets(
        cls,
        preferred_batch_size: int,
        prefill_buckets_num: int,
        prefill_buckets: Optional[Sequence[Tuple[int, int]]],
        max_position_embeddings: int,
    ) -> List[Bucket]:
        if prefill_buckets is not None:
            return [
                Bucket.prefill(batch_size, attn_size) for batch_size, attn_size in prefill_buckets
            ]
        else:
            # Generate the buckets automatically
            percentage = 1.0 / prefill_buckets_num
            interval = max_position_embeddings * percentage
            atten_sizes = [int(interval * i) for i in range(1, prefill_buckets_num + 1)]
            return [Bucket.prefill(preferred_batch_size, attn_size) for attn_size in atten_sizes]

    @classmethod
    def compute_decode_buckets(
        cls,
        preferred_batch_size: int,
        decode_buckets_num: int,
        decode_buckets: Optional[Sequence[Tuple[int, int]]],
        max_position_embeddings: int,
    ) -> List[Bucket]:
        if decode_buckets is not None:
            return [
                Bucket.decode(batch_size, attn_size) for batch_size, attn_size in decode_buckets
            ]
        else:
            # Generate the buckets automatically
            percentage = 1.0 / decode_buckets_num
            interval = max_position_embeddings * percentage
            attn_sizes = [int(interval * i) for i in range(1, decode_buckets_num + 1)]
            return [Bucket.decode(preferred_batch_size, attn_size) for attn_size in attn_sizes]

    @classmethod
    def __verify_buckets(
        cls,
        prefills: Sequence[Bucket],
        decodes: Sequence[Bucket],
        kv_cache_beam_sharing: Optional[KvCacheSharingAcrossBeamsConfig],
    ):
        if kv_cache_beam_sharing is not None:
            for bucket in decodes:
                if bucket.batch_size % kv_cache_beam_sharing.beam_width != 0:
                    raise ValueError(
                        f"decode batch size must be a multiple of beam width, but got {bucket.batch_size} % {kv_cache_beam_sharing.beam_width} != 0"
                    )
                if bucket.attention_size <= kv_cache_beam_sharing.max_new_tokens:
                    raise ValueError(
                        f"decode bucket's attention size must be greater than max_new_tokens, but got {bucket.attention_size} < {kv_cache_beam_sharing.max_new_tokens}"
                    )

    @staticmethod
    def __verify_comp_supertask_kind(kind: str) -> None:
        if kind not in ("fx", "dfg", "edf"):
            raise ValueError(
                f"Unknown comp_supertask_kind: {kind}. Must be either 'fx', 'dfg', or 'edf'."
            )

    @staticmethod
    def __verify_tokenizer_mode(tokenizer_mode: TokenizerModeType) -> None:
        tokenizer_mode_lowered = tokenizer_mode.lower()
        if tokenizer_mode_lowered not in get_args(TokenizerModeType):
            valid_options = ",".join(get_args(TokenizerModeType))
            raise ValueError(
                f"Unknown tokenizer mode: {tokenizer_mode}. Must be one of '{valid_options}'."
            )

    @staticmethod
    def __verify_devices(devices: Sequence[Device]) -> None:
        if len(devices) == 0:
            raise ValueError("No devices are given")
        if not all(dev.kind == devices[0].kind for dev in devices):
            raise ValueError("All devices must be the same kind.")

    @staticmethod
    def __is_generative_model(model_type: Union[str, Type[PreTrainedModel]]) -> bool:
        """Check if the model is a generative model."""
        if isinstance(model_type, str):
            return model_type in _HF_CAUSAL_LM_CLASS_NAMES
        else:
            return model_type.__name__ in _HF_CAUSAL_LM_CLASS_NAMES

    def _get_default_opt_config_from_pretrained_id(
        self, pretrained_id: str, trust_remote_code: Optional[bool]
    ) -> OptimizationConfig:
        model_cls = get_model_cls_from_pretrained_id(pretrained_id, trust_remote_code)
        model_cls = get_mapped_class_for_optimization(model_cls)

        if model_cls is transformers.GPTJForCausalLM:
            return OptimizationConfig(
                attention_type=AttentionType.PAGED_ATTENTION,
                optimize_rope=True,
                optimize_packed=True,
                causal_mask_free_decoding=True,
            )
        elif model_cls is transformers.BertForQuestionAnswering:
            return OptimizationConfig(
                use_unsplit_packed=True,
                use_rngd_gelu=True,
            )
        elif model_cls is transformers.LlamaForCausalLM:
            # Llama MLPerf model
            return OptimizationConfig(
                attention_type=AttentionType.PAGED_ATTENTION,
                optimize_rope=True,
                optimize_packed=True,
                causal_mask_free_decoding=True,
            )
        else:
            raise NotImplementedError(f"Unsupported model architecture: {model_cls}")

    def build_all_pipelines(
        self,
        model: ModelCreationInfo,
        buckets_with_output_size: Sequence[BucketWithOutputLogitsSize],
        devices: Sequence[Device],
        backend: LLMBackend,
        comp_supertask_kind: str,
        one_supertask_per_device: bool,
        use_blockwise_compile: bool,
        embedding_layer_as_single_block: bool,
        do_decompositions_for_model_rewrite: bool,
        kv_cache_dtype: Optional[torch.dtype],
        sparse_select_version: str,
        num_pipeline_builder_workers: int,
        num_compile_workers: int,
        embed_all_constants_into_graph: bool,
        num_blocks_per_supertask: int,
        num_blocks_per_pp_stage: Optional[Sequence[int]],
        param_file_path: Optional[os.PathLike],
        param_saved_format: str,
        compiler_config_context: CompilerConfigContext,
        cache_dir: Optional[os.PathLike],
        cleanup: bool,
        **kwargs,
    ) -> None:
        # If backend using Pipeline is used, create directory for temporary files.
        tmp_dir_path = None
        if backend.is_parallelism_supported():
            if cleanup:
                self.tmp_dir = tempfile.TemporaryDirectory()
                tmp_dir_path = Path(self.tmp_dir.name)
            else:
                tmp_dir_path = Path(tempfile.mkdtemp())

        # Save model parameters when param file path is not given
        # and pipeline should be constructed.
        if param_file_path is None and backend.is_parallelism_supported():
            if cache_dir is not None and model.is_hashable():
                param_file_cache_dir = Path(cache_dir) / "param_files"
                param_file_path = get_param_file_with_cache(model, param_file_cache_dir)
            else:
                assert isinstance(tmp_dir_path, Path)
                param_file_path = get_param_file_with_cache(model, tmp_dir_path)

        cache_dir = None if cache_dir is None else Path(cache_dir)

        # For now, `PipelineParallelismMppp` supports all valid cases because only pipeline parallelism is needed to be expressed within one pipeline.
        if num_blocks_per_pp_stage and "mppp" in kwargs:
            logger.warning(
                "`num_blocks_per_pp_stage` and custom `mppp` is given at the same time.`num_blocks_per_pp_stage` is ignored."
            )
        mppp = kwargs.pop("mppp", None) or PipelineParallelismMppp(num_blocks_per_pp_stage)

        # Build Pipelines for first dp subgroup.
        self.pipelines_with_meta = build_pipelines(
            model,
            buckets_with_output_size,
            devices,
            param_file_path,
            cache_dir,
            backend,
            mppp,
            SuperTaskKind.from_str(comp_supertask_kind),
            one_supertask_per_device,
            use_blockwise_compile,
            embedding_layer_as_single_block,
            do_decompositions_for_model_rewrite,
            kv_cache_dtype,
            self.generator_config.paged_attention_config,
            sparse_select_version,
            self.generator_config.kv_cache_sharing_across_beams_config,
            tmp_dir_path,
            self.model_metadata,
            compiler_config_context,
            num_pipeline_builder_workers,
            num_compile_workers,
            embed_all_constants_into_graph,
            num_blocks_per_supertask,
            self.is_generative_model,
            param_saved_format,
            **kwargs,
        )

        if len(self.pipelines_with_meta) == 0:
            raise ValueError("No pipeline is generated")

    def _save_engine_artifacts(
        self,
        path: Union[str, os.PathLike],
        comp_supertask_kind: str,
        devices: Sequence[Device],
    ):
        import shutil

        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        for idx, pipeline_with_metadata in enumerate(self.pipelines_with_meta):
            pipeline = pipeline_with_metadata.pipeline
            blobs = {}
            param_files = copy.deepcopy(pipeline.param_files)

            blob_kind = pipeline.get_blob_kind()
            for id, blob in pipeline.blobs.items():
                blobs[id] = blob
                kind = blob_kind.get(id)
                if kind == SuperTaskKind.FX:
                    with open(f"{path}/{id}.fx", "w") as fp:
                        fp.write(blob)
                elif kind == SuperTaskKind.EDF:
                    with open(f"{path}/{id}.edf", "wb") as fp:
                        fp.write(blob.serialize())  # type: ignore[attr-defined]
                else:
                    raise NotImplementedError(f"SuperTask [{kind}] is not supported to save")
                pipeline.blobs[id] = None  # type: ignore[assignment]

            for param_idx, param_file in pipeline.param_files.items():
                filename = os.path.basename(param_file.path)
                new_path = Path(f"{path}/{filename}")
                if not new_path.exists():
                    shutil.copyfile(param_file.path, new_path)
                pipeline.param_files[param_idx].path = filename

            pipeline.export(f"{path}/pipeline.{idx}.json")
            pipeline.blobs = blobs
            pipeline.param_files = param_files

        # Save pipeline metadata
        serialized_pipelines_metadata_list = [
            pipeline_with_meta.metadata.model_dump()
            for pipeline_with_meta in self.pipelines_with_meta
        ]
        with open(f"{path}/pipelines_metadata.json", "w") as fp:
            fp.write(json.dumps(serialized_pipelines_metadata_list))

        self.generator_config.export(f"{path}/generator_config.json")
        self.scheduler_config.export(f"{path}/scheduler_config.json")
        with open(f"{path}/hf_config.json", "w") as fp:
            json.dump(self.model_config, fp)

        model_metadata_path = f"{path}/model_metadata.json"
        with open(model_metadata_path, "w") as fp:
            fp.write(self.model_metadata.model_dump_json())

        model_rewriting_config_path = f"{path}/model_rewriting_config.json"
        with open(model_rewriting_config_path, "w") as fp:
            fp.write(self.model_rewriting_config.model_dump_json())

        parallel_config_path = f"{path}/parallel_config.json"
        with open(parallel_config_path, "w") as fp:
            fp.write(self.parallel_config.model_dump_json())

        other_config_path = f"{path}/other_config.json"
        with open(other_config_path, "w") as fp:
            fp.write(
                json.dumps(
                    {
                        "comp_supertask_kind": comp_supertask_kind,
                        "devices": tuple(devices),
                    }
                )
            )

        open(f"{path}/ready", "w").close()

    @staticmethod
    def __verify_sampling_params_with_generator_config(
        sampling_params: SamplingParams,
        generator_config: GeneratorConfig,
    ):
        if sampling_params.max_tokens is None:
            raise ValueError("`sampling_params.max_tokens` must be specified at this point.")

        if generator_config.kv_cache_sharing_across_beams_config is not None:
            if not sampling_params.use_beam_search:
                raise ValueError(
                    "`sampling_params.use_beam_search` is not consistent with generator config. The model was configured to use beam search, but `sampling_params.use_beam_search` is False."
                )
            if (
                sampling_params.max_tokens
                > generator_config.kv_cache_sharing_across_beams_config.max_new_tokens
            ):
                raise ValueError(
                    "`sampling_params.max_tokens` is larger than `generator_config.kv_cache_sharing_across_beams_config.max_new_tokens`"
                )
            if (
                sampling_params.best_of
                != generator_config.kv_cache_sharing_across_beams_config.beam_width
            ):
                raise ValueError(
                    "`sampling_params.best_of` is different from beam width specified in `generator_config.kv_cache_sharing_across_beams_config.beam_width`."
                )

    def generate(
        self,
        prompts: Union[str, List[str]],
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[BatchEncoding] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Union[RequestOutput, List[RequestOutput]]:
        """Generate texts from given prompts and sampling parameters.

        Args:
            prompts: The prompts to generate texts.
            sampling_params: The sampling parameters for generating texts.
            prompt_token_ids: Pre-tokenized prompt input as a `BatchEncoding` object.
                If not provided, the prompt will be tokenized internally using the tokenizer.
            tokenizer_kwargs: Additional keyword arguments passed to the tokenizer's
                `encode` method, such as `{"use_special_tokens": True}`.

        Returns:
            A list of `RequestOutput` objects containing the generated
            completions in the same order as the input prompts.
        """

        if not self.is_generative_model:
            raise ValueError("generate API can only be used for generative models.")

        if prompt_token_ids is None:
            if tokenizer_kwargs is None:
                tokenizer_kwargs = {}
            prompt_token_ids = encode_auto(self.tokenizer, prompts, **tokenizer_kwargs)

        input_ids = prompt_token_ids.input_ids
        if input_ids and isinstance(input_ids[0], list):
            max_prompt_len = max(len(prompt) for prompt in input_ids)
        else:
            max_prompt_len = len(input_ids)
        assert (
            self.max_seq_len_to_capture is not None
        ), "Generative models must have max_seq_len_to_capture set."
        sampling_params.verify_and_finalize_max_tokens(
            max_prompt_len, self.prompt_max_seq_len, self.max_seq_len_to_capture
        )
        LLM.__verify_sampling_params_with_generator_config(sampling_params, self.generator_config)
        native_outputs = self.engine.generate(prompt_token_ids, sampling_params)
        return self._generate_postprocess(native_outputs, prompts, prompt_token_ids)

    def chat(
        self,
        messages: Union[List[ChatCompletionMessageParam], List[List[ChatCompletionMessageParam]]],
        sampling_params: SamplingParams = SamplingParams(),
        chat_template: Optional[str] = None,
        chat_template_content_format: ChatTemplateContentFormatOption = "string",
        add_generation_prompt: bool = True,
        continue_final_message: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> List[RequestOutput]:
        """
        Generate responses for a chat conversation.

        The chat conversation is converted into a text prompt using the
        tokenizer and calls the :meth:`generate` method to generate the
        responses.

        Args:
            messages: A list of conversations or a single conversation.

              - Each conversation is represented as a list of messages.
              - Each message is a dictionary with 'role' and 'content' keys.

            sampling_params: The sampling parameters for text generation.
            chat_template: The template to use for structuring the chat.
                If not provided, the model's default chat template will be used.
            chat_template_content_format: The format to render message content.
                Currently only "string" is supported.
            add_generation_prompt: If True, adds a generation template
                to each message.
            continue_final_message: If True, continues the final message in
                the conversation instead of starting a new one. Cannot be
                ``True`` if ``add_generation_prompt`` is also ``True``.

        Returns:
            A list of ``RequestOutput`` objects containing the generated
            responses in the same order as the input messages.
        """
        if continue_final_message and add_generation_prompt:
            raise ValueError(
                "continue_final_message cannot be True when add_generation_prompt is True."
            )
        messages_list: List[List[ChatCompletionMessageParam]]
        if is_list_of(messages, list):
            messages_list = messages
        else:
            messages_list = [messages]
        rendered_prompts = self.tokenizer.apply_chat_template(
            messages_list,
            tools=tools,
            chat_template=chat_template,
            add_generation_prompt=add_generation_prompt,
            tokenize=False,
            continue_final_message=continue_final_message,
        )
        # XXX(n0gu):
        # The `continue_final_message` parameter was introduced in transformers v4.45:
        #   https://github.com/huggingface/transformers/commit/52a02137557963e9dd58c9be65b6cef871d3bf32
        # But we are using v4.44.
        # Until we upgrade to a newer version of transformers, we must manually remove the last EOT token.
        if continue_final_message:
            try:
                # Remove last eos from prompt if exists
                eos_token = self.tokenizer.eos_token
                rendered_prompts = [
                    prompt[: -len(eos_token)] if prompt.endswith(eos_token) else prompt
                    for prompt in rendered_prompts
                ]
            except AttributeError:
                pass
        return self.generate(
            rendered_prompts, sampling_params, tokenizer_kwargs={"add_special_tokens": False}
        )  # type: ignore

    async def stream_generate(
        self,
        prompt: str,
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[BatchEncoding] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        is_demo: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Generate texts from given prompt and sampling parameters.

        Args:
            prompt: The prompt to generate texts. Note that unlike `generate`,
                this API supports only a single prompt.
            sampling_params: The sampling parameters for generating texts.
            prompt_token_ids: Pre-tokenized prompt input as a `BatchEncoding` object.
                If not provided, the prompt will be tokenized internally using the tokenizer.
            tokenizer_kwargs: Additional keyword arguments passed to the tokenizer's
                `encode` method, such as `{"use_special_tokens": True}`.

        Returns:
            A stream of generated output tokens.
        """
        if not self.is_generative_model:
            raise ValueError("generate API can only be used for generative models.")
        if not isinstance(prompt, str):
            raise ValueError("prompt must be a single string.")

        if prompt_token_ids is None:
            if tokenizer_kwargs is None:
                tokenizer_kwargs = {}
            prompt_token_ids = encode_auto(self.tokenizer, prompt, **tokenizer_kwargs)

        input_ids = prompt_token_ids.input_ids
        if input_ids and isinstance(input_ids[0], list):
            max_prompt_len = max(len(prompt) for prompt in input_ids)
        else:
            max_prompt_len = len(input_ids)
        assert (
            self.max_seq_len_to_capture is not None
        ), "Generative models must have max_seq_len_to_capture set."
        sampling_params.verify_and_finalize_max_tokens(
            max_prompt_len, self.prompt_max_seq_len, self.max_seq_len_to_capture
        )
        LLM.__verify_sampling_params_with_generator_config(sampling_params, self.generator_config)

        # FIXME: LLM.__init__() should take max_tokens to determine the maximum sequence length through bucket generations
        # and use the config value to raise an error.
        if is_demo and len(prompt_token_ids.input_ids) > 1024:  # type: ignore
            raise ValueError("The length of the prompt is larger than 1024 tokens")

        # NOTE: type of engine.stream_generate() is AsyncGenerator[RequestOutput, None]
        token_buffer = []
        request_output: RequestOutput
        async for request_output in self.engine.stream_generate(prompt_token_ids, sampling_params):
            num_decode_trials = STREAMING_MAX_DECODE_TRIAL
            for completion_output in request_output.outputs:
                token_buffer.extend(completion_output.token_ids)
                num_decode_trials = min(num_decode_trials, len(completion_output.token_ids))

            if num_decode_trials == 0:
                continue

            for tokens_to_discard in range(num_decode_trials):
                end_offset = len(token_buffer) - 1 - tokens_to_discard
                new_text = self.tokenizer.decode(
                    token_buffer[: end_offset + 1], skip_special_tokens=True
                )
                if not new_text.endswith("�"):
                    break
            else:
                continue

            token_buffer = token_buffer[end_offset + 1 :]
            yield new_text

        if token_buffer:
            yield self.tokenizer.decode(token_buffer, skip_special_tokens=True)

    def _generate_postprocess(
        self,
        native_outputs,
        prompts: Union[str, List[str]],
        prompt_token_ids: Union[List[int], List[List[int]]],
    ) -> Union[RequestOutput, List[RequestOutput]]:
        skip_special_tokens = isinstance(prompts, list)

        # Convert one prompt and multiple generated sequences into a RequestOutput
        def convert(prompt: str, prompt_token_ids: List[int], request_output):
            outputs = []
            for output in request_output.outputs:
                text = self.tokenizer.decode(
                    output.token_ids, skip_special_tokens, clean_up_tokenization_spaces=True
                )
                logprobs = None
                if output.logprobs is not None:
                    # output: NativeCompletionOutput (not CompletionOutput)
                    # output.logprobs: List[List[Tuple[int, float]]]
                    # token_id_to_logprob: List[Tuple[int, float]]
                    logprobs = [
                        {token_id: Logprob(logprob) for token_id, logprob in token_id_to_logprob}
                        for token_id_to_logprob in output.logprobs
                    ]
                outputs.append(
                    CompletionOutput(
                        output.index, text, output.token_ids, logprobs, output.finish_reason
                    )
                )
            return RequestOutput(
                request_id=uuid.uuid4().__str__(),
                prompt=prompt,
                prompt_token_ids=prompt_token_ids,
                outputs=outputs,
                finished=True,
            )

        if isinstance(native_outputs, list):
            assert isinstance(prompts, list)
            return [
                convert(req[0], req[1], req[2])
                for req in zip(prompts, prompt_token_ids.input_ids, native_outputs)  # type: ignore
            ]
        else:
            assert isinstance(prompts, str)
            return convert(prompts, prompt_token_ids.input_ids, native_outputs)  # type: ignore

    def bert_forward(
        self,
        prompts: Union[str, List[str]],
        contexts: Union[str, List[str]],
    ) -> Union[RequestOutput, List[RequestOutput]]:
        prompt_token_ids = encode_auto(self.tokenizer, prompts, text_pair=contexts)
        native_outputs = self.engine.bert_forward(prompt_token_ids)
        return self._generate_postprocess(native_outputs, prompts, prompt_token_ids)

    def __del__(self):
        # Remove tmp directory if exists.
        tmp_dir = getattr(self, "tmp_dir", None)
        if tmp_dir is not None:
            tmp_dir.cleanup()

    @staticmethod
    def __get_gms_for_pipeline(
        pipeline: Pipeline,
        get_input_constants: bool = False,
    ) -> Union[
        Tuple[GraphModule, ...], Tuple[Tuple[GraphModule, Tuple[Optional[torch.Tensor], ...]], ...]
    ]:
        ret: List = []
        gm_cache: Dict[Optional[DataBlobId], GraphModule] = {}

        # Sort supertasks by id to guarantee consistent order.
        sorted_supertasks = (
            supertask
            for _, supertask in sorted(pipeline.supertasks.items(), key=lambda x: int(x[0]))
        )

        for supertask in sorted_supertasks:
            if not isinstance(supertask, CompSuperTask):
                continue

            if supertask.kind != SuperTaskKind.FX:
                raise ValueError("Supertask is not FX graph supertask.")

            param_load_cache: Dict[Any, Any] = {}

            fake_mode = FakeTensorMode(allow_non_fake_inputs=True)

            with fake_mode:
                fake_example_inputs = tuple(
                    torch.zeros(
                        pipeline.tensors[input_].shape,
                        dtype=pipeline.tensors[input_].dtype.to_torch_dtype(),
                    )
                    for input_ in supertask.inputs
                )

            gm = gm_cache.get(supertask.data_blob, None)
            if gm is None:
                if supertask.data is not None:
                    data = supertask.data
                else:
                    assert supertask.data_blob is not None
                    data = pipeline.blobs[supertask.data_blob]

                gm = deserialize_gm(data)
                # NOTE: This Shape propagation is required because tensor meta information is lost during serialization. We need to regenerate this.
                ShapeProp(gm).propagate(*fake_example_inputs)
                # preprocess gms for it to be compiled immediately
                gm = preprocess(gm, fake_example_inputs)

                if supertask.data_blob is not None:
                    gm_cache[supertask.data_blob] = cast(GraphModule, gm)

            if get_input_constants:
                # TODO: change this to share same tensor among slices.
                def load_tensor(tensor_name) -> Optional[torch.Tensor]:
                    tensor_info = pipeline.tensors[tensor_name]
                    if isinstance(tensor_info, TensorInfo):
                        # If it's not an input constant tensor (i.e., input tensor not originated from constant tensor),
                        # just return None.
                        return None
                    else:
                        assert isinstance(tensor_info, ParamInfo)
                        param_value = tensor_info.value
                        param_file_info = pipeline.param_files[param_value.param_file]

                        return load_partial_param(
                            param_file_info.path,
                            param_value.name,
                            param_value.placements,
                            param_file_info.format,
                            cache=param_load_cache,
                        ).contiguous()

                example_input = tuple(load_tensor(input_name) for input_name in supertask.inputs)
                ret.append((gm, example_input))
            else:
                ret.append(gm)

        return tuple(ret)

    def _get_splitted_gms(self, get_input_constants: bool = False) -> Dict[
        str,
        Union[
            Tuple[GraphModule, ...],
            Tuple[Tuple[GraphModule, Tuple[Optional[torch.Tensor], ...]], ...],
        ],
    ]:
        """Get sub GraphModules for each pipeline.

        Returns:
            Dict[str, Union[Tuple[GraphModule, ...], Tuple[Tuple[GraphModule, Tuple[Optional[torch.Tensor], ...]], ...],],]:
                Dictionary whose key is the pipeline name and value is the tuple containing ``GraphModule``s (computation supertasks) and some additional information if necessary.
                if ``get_input_constants==False``, each value is just a tuple of ``GraphModule``s in the pipeline.
                Otherwise, each value is a tuple whose element is ``GraphModule`` in the pipeline  and list of input constant tensors,
                which were originally constant tensors, but converted to input. The list of input constant tensors has same length as corresponding ``GraphModule``'s number of inputs
                with each element exactly corresponding to the input of the ``GraphModule`` with same index, but elements with original input tensor indexes are ``None``.
        """
        if not (
            isinstance(self.pipelines_with_meta, Sequence)
            and isinstance(self.pipelines_with_meta[0], PipelineWithMetadata)
        ):
            raise ValueError("get_splitted_gms is only supported for parallel backends")

        return {
            pipeline_with_meta.pipeline.name: LLM.__get_gms_for_pipeline(
                pipeline_with_meta.pipeline, get_input_constants=get_input_constants
            )
            for pipeline_with_meta in self.pipelines_with_meta
        }

    @staticmethod
    def __verify_kv_cache_dtype_with_qformat(
        kv_cache_dtype: QDtype, qformat_path: os.PathLike, model_metadata: ModelMetadata
    ) -> None:
        kv_cache_dtype_from_qformat = get_kv_cache_dtype_from_qformat(qformat_path)
        if kv_cache_dtype != kv_cache_dtype_from_qformat:
            raise ValueError(
                f"kv_cache_dtype != qformat's kv_cache dtype: {kv_cache_dtype} != {kv_cache_dtype_from_qformat}"
            )

    @cached_property
    def model_max_seq_len(self) -> int:
        possible_keys = [
            # OPT, LLaMA, BERT
            "max_position_embeddings",
            # GPT-2, GPT-J
            "n_positions",
            # MPT
            "max_seq_len",
            # ChatGLM2
            "seq_length",
            # Command-R
            "model_max_length",
            # Others
            "max_sequence_length",
            "max_seq_length",
            "seq_len",
        ]

        for attr_name in possible_keys:
            if attr_name in self.model_config:
                model_max_seq_len = self.model_config[attr_name]
                break
        else:
            # If none of the keys were found in the config, use a default and
            # log a warning.
            default_max_len = 2048
            model_max_seq_len = default_max_len
            logger.warning(
                "The model's config.json does not contain any of the following "
                "keys to determine the original maximum length of the model: "
                "%s. Assuming the model's maximum length is %d.",
                possible_keys,
                default_max_len,
            )
        return model_max_seq_len


def try_compiler_config_from_yaml(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Compiler config must be given at: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_artifact(
    model_id_or_path: Union[str, os.PathLike],
    *,
    # Runtime Configuration
    devices: Optional[Union[str, Sequence[Device]]] = None,
    data_parallel_size: Optional[int] = None,
    pipeline_parallel_size: Optional[int] = None,
    num_blocks_per_pp_stage: Optional[Sequence[int]] = None,
    bucket_config: Optional[BucketConfig] = None,
    scheduler_config: Optional[SchedulerConfig] = None,
    paged_attention_num_blocks: Optional[int] = None,
    # Other Configuration
    tokenizer: Optional[Union[PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
    tokenizer_mode: TokenizerModeType = "auto",
    seed: Optional[int] = None,
    cache_dir: os.PathLike = CACHE_DIR,
    **kwargs,
) -> LLM:
    """Instantiate LLM from saved artifacts without quantization and compilation.

    Internally, this function calls :meth:`LLM.load_artifact`.
    """
    kwargs.pop("backend")

    return LLM.load_artifact(
        model_id_or_path,
        devices=devices,
        data_parallel_size=data_parallel_size,
        pipeline_parallel_size=pipeline_parallel_size,
        num_blocks_per_pp_stage=num_blocks_per_pp_stage,
        bucket_config=bucket_config,
        scheduler_config=scheduler_config,
        paged_attention_num_blocks=paged_attention_num_blocks,
        tokenizer=tokenizer,
        tokenizer_mode=tokenizer_mode,
        seed=seed,
        cache_dir=cache_dir,
        **kwargs,
    )
