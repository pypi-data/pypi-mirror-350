from dataclasses import dataclass, field
from itertools import chain, product
import logging
import os
from pathlib import Path
from typing import ClassVar, Dict, Final, Iterable, List, Mapping, Optional, Tuple, Union

try:
    import pytest
except ImportError:
    pass
from transformers import set_seed

from furiosa_llm import LLM, SamplingParams
from furiosa_llm.api import KvCacheSharingAcrossBeamsConfig, ManualBucketConfig, SchedulerConfig
from furiosa_llm.artifact import ArtifactBuilder
from furiosa_llm.models.config_types import BucketWithOutputLogitsSize
from furiosa_llm.models.metadata import ModelMetadata
from furiosa_llm.parallelize.mppp.config import Device
from furiosa_llm.tokenizer import get_tokenizer

logger = logging.getLogger(__name__)

TEST_SEED_VALUE = 42
FURIOSA_LLM_PACKAGE_PATH: Final = Path(__file__).parent.parent

_LLAMA3_OPT_CLASS_COMPATIBLE_LISTS = [
    {
        "llama3.symbolic.mlperf_submission",
        "llama3.symbolic.aramco_specdec",
    },
]
_LLAMA3_VARIANT_COMPATIBLE_MAP: Final[Dict[str, Tuple[str, ...]]] = {
    opt_class: tuple(compatible_set.difference({opt_class}))
    for compatible_set in _LLAMA3_OPT_CLASS_COMPATIBLE_LISTS
    for opt_class in compatible_set
}

# calibration dataset names
BASE_CALIB_DATASET = "base"
ARAMCO_CALIB_DATASET = "aramco"


# Make this struct and furiosa-rt-python/tests/e2e_base.rs consistent
@dataclass
class LLMTestCase:
    name: str
    model_metadata: ModelMetadata
    prompts: List[str]
    sampling_params: SamplingParams
    seed: int = TEST_SEED_VALUE
    devices: str = "cpu:0"
    prefill_buckets: List[Tuple[int, int]] = field(default_factory=list)
    decode_buckets: List[Tuple[int, int]] = field(default_factory=list)
    custom_buckets: List[BucketWithOutputLogitsSize] = field(default_factory=list)
    speculative_model_metadata: Optional[ModelMetadata] = None
    speculative_model_prefill_buckets: Optional[List[Tuple[int, int]]] = None
    speculative_model_decode_buckets: Optional[List[Tuple[int, int]]] = None
    speculative_model_paged_attention_num_blocks: Optional[int] = None
    num_speculative_tokens: Optional[int] = None
    tensor_parallel_size: int = 4
    pipeline_parallel_size: int = 1
    data_parallel_size: Optional[int] = None
    validation_model: Optional[ModelMetadata] = (
        None  # For some model, you may need to use a different model for validation.
    )
    num_blocks_per_supertask: int = 1
    num_blocks_per_pp_stage: Optional[List[int]] = None
    paged_attention_num_blocks: Optional[int] = None
    kv_cache_sharing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig] = None
    qa_context: Optional[List[str]] = None
    scheduler_config: SchedulerConfig = SchedulerConfig(spare_blocks_ratio=0.0)
    compiler_config_overrides: Optional[Mapping] = None
    use_random_weight: bool = False
    device_sets_for_actual_use: Optional[List[Union[str, List[Device]]]] = None
    embed_all_constants_into_graph: bool = False
    optimize_logit_shape: bool = True
    num_pipeline_builder_workers: int = int(os.environ.get("NUM_PIPELINE_BUILDER_WORKERS", 1))
    num_compile_workers: int = int(os.environ.get("NUM_COMPILE_WORKERS", 1))
    skip_validation: bool = False

    _BY_NAME: ClassVar[Dict[str, "LLMTestCase"]] = {}

    @classmethod
    def xxfail(cls, reason: str, *args, **kwargs):
        """Marks this test case to be known to fail (xfail) and shouldn't be run by default.
        Use `--runxfail` to run such test cases."""
        return pytest.param(cls(*args, **kwargs), marks=pytest.mark.xfail(reason=reason, run=False))

    def __class_getitem__(cls, name: str) -> "LLMTestCase":
        return cls._BY_NAME[name]

    def __post_init__(self):
        try:
            old = self._BY_NAME[self.name]
        except KeyError:
            self._BY_NAME[self.name] = self
            return

        if self != old:
            raise ValueError(
                f"LLMTestCase {self.name} has an inconsistent value:\n{old!r}\n{self!r}"
            )

    def __str__(self):
        # Use all attributes to generate string representation
        return str(self.__dict__)

    @property
    def test_param_id(self):
        return self.name

    def test_uses_models(self) -> Iterable[str]:
        if self.validation_model is not None:
            return [self.model_metadata.name, self.validation_model.name]
        return [self.model_metadata.name]

    def is_model_available(self) -> bool:
        return self.model_metadata.is_model_available()


def run_furiosa_llm(
    test_case: LLMTestCase,
    **kwargs,
) -> Union[List[str], List[List[str]]]:
    set_seed(test_case.seed)
    llm = prestep_furiosa_llm(test_case, **kwargs)
    request_output = llm.generate(test_case.prompts, test_case.sampling_params)
    return poststep_furiosa_llm(request_output, llm.tokenizer)


@dataclass
class QuantArtifacts:
    qparam_path: os.PathLike
    qformat_path: os.PathLike
    qckpt_file_path: Optional[os.PathLike]


def _get_quant_subpath(model: ModelMetadata) -> str:
    return model.get_optimized_cls().__module__.split(".", maxsplit=1)[-1]


def _get_valid_quant_ckpt_file_paths(
    model: ModelMetadata, variant_sub_path: str
) -> Tuple[Path, Path, Optional[Path]]:
    root_dir = FURIOSA_LLM_PACKAGE_PATH.parent / "furiosa-llm-models-artifacts" / "quantized"

    if not root_dir.is_dir():
        raise FileNotFoundError(f"Directory not found: {root_dir}")

    tiny_model_suffix = "-tiny" if model._is_tiny_gptj else ""

    # TODO: get filename from quantization target types. (now it's hardcoded to W8A8KV8)
    assert model.quantization_config is not None

    quant_type_path = str(model.quantization_config)
    curr_model_num_layer = model.get_num_hidden_layers()
    # FIXME: Using "" as one of the candidate calibration dataset directory is a temporary workaround
    # for addressing several quantization artifact directory patterns presented currently.
    # It should be removed later after `furiosa-llm-models-artifacts` is updated.
    calib_dataset = getattr(model, "calib_dataset", BASE_CALIB_DATASET)
    full_model_num_layer = model.full_layer_count

    # If there's no specific quantization files for specific number of hidden layers,
    # try to use "one for all" quantization files.
    cases_for_num_layer_and_calib_data = product(
        [
            f"{model.get_num_hidden_layers()}L{tiny_model_suffix}",
            f"{full_model_num_layer}L{tiny_model_suffix}",
        ],
        ([calib_dataset] if calib_dataset != BASE_CALIB_DATASET else ["", BASE_CALIB_DATASET, "_"]),
    )

    for num_layer, calib_dataset in cases_for_num_layer_and_calib_data:
        q_path = (
            root_dir
            / model.pretrained_id
            / variant_sub_path
            / quant_type_path
            / num_layer
            / calib_dataset
        )
        logger.info(f"trying quant artifact path: {q_path}")
        if os.path.isfile(q_path / "qformat.yaml"):
            if num_layer != f"{curr_model_num_layer}L":
                logging.info(
                    "\x1b[1;35mFull model qparam/qformat is used for model with smaller number of layers. "
                    "The model might not be quantized properly.\x1b[0m",
                )
            qformat_path = q_path / "qformat.yaml"
            qparam_path = q_path / "qparam.npy"
            if os.path.isfile(q_path / "exported_model.qckpt"):
                qckpt_file_path = q_path / "exported_model.qckpt"
            else:
                qckpt_file_path = None
            return qformat_path, qparam_path, qckpt_file_path
    raise FileNotFoundError(f"Failed to find qparam, qformat artifacts: for model metadata {model}")


# NOTE: assumes that the furiosa-llm package is located in furiosa-runtime
# TODO: move this to tests.utils.
def get_quant_artifacts_for_test(model: ModelMetadata) -> QuantArtifacts:
    """Get qformat / qparam path in furiosa-llm-models-artifacts fot the given model."""
    variant_sub_path = _get_quant_subpath(model)

    # NOTE: spec dec models share same qparam / qformat with ones without spec dec optimization.
    # FIXME: make this matching more robust.
    list_to_try = (variant_sub_path,) + _LLAMA3_VARIANT_COMPATIBLE_MAP.get(variant_sub_path, ())
    for variant_sub_path in list_to_try:
        try:
            qformat_path, qparam_path, qckpt_file_path = _get_valid_quant_ckpt_file_paths(
                model, variant_sub_path
            )
            break
        except FileNotFoundError:
            pass
    else:
        raise

    return QuantArtifacts(
        qparam_path,
        qformat_path,
        qckpt_file_path,
    )


def prestep_furiosa_llm(
    test_case: LLMTestCase,
    *,
    artifacts_path: Optional[Union[str, os.PathLike]] = None,
    **kwargs,
) -> LLM:
    # Analyze the LLM parameters from prompts and sampling params
    tokenizer = kwargs.pop("tokenizer", None)
    if not tokenizer:
        tokenizer = get_tokenizer(test_case.model_metadata.pretrained_name, **kwargs)

    if test_case.speculative_model_metadata:
        speculative_model: Optional[str] = test_case.speculative_model_metadata.pretrained_id
        speculative_model_llm_config = test_case.speculative_model_metadata.llm_config
        speculative_model_config = test_case.speculative_model_metadata.hf_configs

        assert test_case.speculative_model_prefill_buckets is not None
        assert test_case.speculative_model_decode_buckets is not None

        speculative_model_bucket_config = ManualBucketConfig(
            prefill_buckets=test_case.speculative_model_prefill_buckets,
            decode_buckets=test_case.speculative_model_decode_buckets,
        )
    else:
        speculative_model = speculative_model_llm_config = None
        speculative_model_config = {}
        assert test_case.speculative_model_prefill_buckets is None
        assert test_case.speculative_model_decode_buckets is None
        speculative_model_bucket_config = None

    # FIXME: Remove this after fixing all rust tests and furiosa-mlperf to call
    # `LLM.from_artifacts` directly when artifacts is presence.
    if artifacts_path:
        try:
            llm = LLM.load_artifact(
                artifacts_path,
                **kwargs,
            )
        except Exception as e:
            logger.warning(f"load_artifact failed ({e}), retry with legacy loader")
            llm = LLM.from_artifacts(
                artifacts_path,
                bucket_config=ManualBucketConfig(
                    prefill_buckets=test_case.prefill_buckets,
                    decode_buckets=test_case.decode_buckets,
                ),
                speculative_model_bucket_config=speculative_model_bucket_config,
                data_parallel_size=test_case.data_parallel_size,
                tokenizer=tokenizer,
                seed=test_case.seed,
                devices=test_case.devices,
                paged_attention_num_blocks=test_case.paged_attention_num_blocks,
                scheduler_config=test_case.scheduler_config,
                device_sets_for_actual_use=test_case.device_sets_for_actual_use,
                **kwargs,
            )
    elif artifacts_path := os.environ.get("LLM_ENGINE_ARTIFACTS_PATH"):
        try:
            llm = LLM.load_artifact(
                artifacts_path,
                num_speculative_tokens=test_case.num_speculative_tokens,
                speculative_model_bucket_config=speculative_model_bucket_config,
                data_parallel_size=test_case.data_parallel_size,
                tokenizer=tokenizer,
                seed=test_case.seed,
                devices=test_case.devices,
                paged_attention_num_blocks=test_case.paged_attention_num_blocks,
                scheduler_config=test_case.scheduler_config,
                device_sets_for_actual_use=test_case.device_sets_for_actual_use,
                **kwargs,
            )
        except Exception as e:
            logger.warning(f"load_artifact failed ({e}), retry with legacy loader")
            llm = LLM.from_artifacts(
                artifacts_path,
                speculative_model_bucket_config=speculative_model_bucket_config,
                data_parallel_size=test_case.data_parallel_size,
                tokenizer=tokenizer,
                seed=test_case.seed,
                devices=test_case.devices,
                paged_attention_num_blocks=test_case.paged_attention_num_blocks,
                scheduler_config=test_case.scheduler_config,
                device_sets_for_actual_use=test_case.device_sets_for_actual_use,
                **kwargs,
            )
    else:
        max_bucket_size = max(
            attention_size
            for _, attention_size in chain(test_case.prefill_buckets, test_case.decode_buckets)
        )

        if test_case.model_metadata.need_quant_artifacts:
            quant_artifacts = get_quant_artifacts_for_test(test_case.model_metadata)
            qformat_path: Optional[os.PathLike] = quant_artifacts.qformat_path
            qparam_path: Optional[os.PathLike] = quant_artifacts.qparam_path
            quant_ckpt_file_path = quant_artifacts.qckpt_file_path
        else:
            qformat_path = qparam_path = quant_ckpt_file_path = None
        if (
            test_case.speculative_model_metadata
            and test_case.speculative_model_metadata.need_quant_artifacts
        ):
            speculative_model_quant_artifacts = get_quant_artifacts_for_test(
                test_case.speculative_model_metadata
            )
            speculative_model_qformat_path: Optional[os.PathLike] = (
                speculative_model_quant_artifacts.qformat_path
            )
            speculative_model_qparam_path: Optional[os.PathLike] = (
                speculative_model_quant_artifacts.qparam_path
            )
            speculative_model_quant_ckpt_file_path = (
                speculative_model_quant_artifacts.qckpt_file_path
            )
        else:
            speculative_model_qformat_path = speculative_model_qparam_path = None
            speculative_model_quant_ckpt_file_path = None

        llm = LLM(
            model=test_case.model_metadata.pretrained_id,
            task_type=test_case.model_metadata.task_type,
            llm_config=test_case.model_metadata.llm_config,
            qformat_path=qformat_path,
            qparam_path=qparam_path,
            quant_ckpt_file_path=quant_ckpt_file_path,
            hf_overrides=test_case.model_metadata.hf_configs,
            bucket_config=ManualBucketConfig(
                prefill_buckets=test_case.prefill_buckets, decode_buckets=test_case.decode_buckets
            ),
            _custom_buckets=test_case.custom_buckets,
            speculative_model=speculative_model,
            speculative_model_llm_config=speculative_model_llm_config,
            speculative_model_config=speculative_model_config,
            speculative_model_bucket_config=speculative_model_bucket_config,
            speculative_model_paged_attention_num_blocks=test_case.speculative_model_paged_attention_num_blocks,
            num_speculative_tokens=test_case.num_speculative_tokens,
            tensor_parallel_size=test_case.tensor_parallel_size,
            pipeline_parallel_size=test_case.pipeline_parallel_size,
            data_parallel_size=test_case.data_parallel_size,
            tokenizer=tokenizer,
            seed=test_case.seed,
            max_seq_len_to_capture=max_bucket_size,
            devices=test_case.devices,
            num_blocks_per_supertask=test_case.num_blocks_per_supertask,
            num_blocks_per_pp_stage=test_case.num_blocks_per_pp_stage,
            embed_all_constants_into_graph=test_case.embed_all_constants_into_graph,
            _optimize_logit_shape=test_case.optimize_logit_shape,
            paged_attention_num_blocks=test_case.paged_attention_num_blocks,
            kv_cache_sharing_across_beams_config=test_case.kv_cache_sharing_across_beams_config,
            scheduler_config=test_case.scheduler_config,
            compiler_config_overrides=test_case.compiler_config_overrides,
            device_sets_for_actual_use=test_case.device_sets_for_actual_use,
            use_random_weight=test_case.use_random_weight,
            num_pipeline_builder_workers=test_case.num_pipeline_builder_workers,
            num_compile_workers=test_case.num_compile_workers,
            speculative_model_qformat_path=speculative_model_qformat_path,
            speculative_model_qparam_path=speculative_model_qparam_path,
            speculative_model_quant_ckpt_file_path=speculative_model_quant_ckpt_file_path,
            **kwargs,
        )

    return llm


def poststep_furiosa_llm(
    request_output,
    tokenizer,
) -> Union[List[str], List[List[str]]]:
    if not isinstance(request_output, list):
        request_output = [request_output]

    # FIXME: workaround for BPE-based tokenizer that LLaMA uses.
    #  See: https://github.com/furiosa-ai/furiosa-sdk-private/pull/759#issuecomment-1899648400
    return [
        [
            tokenizer.decode(
                req.prompt_token_ids + output.token_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )
            for output in req.outputs
        ]
        for req in request_output
    ]


def build_artifact_from_llm_testcase(
    test_case: LLMTestCase,
    artifacts_export_path: Union[str, os.PathLike],
    *,
    num_pipeline_builder_workers: int = 1,
    num_compile_workers: int = 1,
    _cleanup: bool = False,
):
    """Builds and saves artifacts based on the given LLMTestCase object.

    The LLMTestCase object is designed for testing purposes in the furiosa-llm,
    ensuring that each configuration value is directly applicable for artifact building.

    Args:
        test_case (LLMTestCase): The test case containing configuration values
            to be used for artifact building.
        artifacts_export_path: The path to export the artifacts.
            With artifacts, you can create ``LLM`` without quantizing or compiling the model again.
            num_pipeline_builder_workers: The number of workers used for building pipelines (except for compilation). The default is 1 (no parallelism).
                Setting this value larger than 1 reduces pipeline building time, especially for large models, but requires much more memory.
            num_compile_workers: The number of workers used for compilation. The default is 1 (no parallelism).

    Returns:
        None: The artifact is built and saved as specified.
    """
    qformat_path = get_quant_artifacts_for_test(test_case.model_metadata).qformat_path
    quantize_artifact_path = Path(qformat_path).parent

    builder = ArtifactBuilder(
        test_case.model_metadata.pretrained_id,
        test_case.name,
        tensor_parallel_size=test_case.tensor_parallel_size,
        pipeline_parallel_size=test_case.pipeline_parallel_size,
        prefill_buckets=test_case.prefill_buckets,
        decode_buckets=test_case.decode_buckets,
        prefill_chunk_size=test_case.scheduler_config.prefill_chunk_size,
        num_hidden_layers=test_case.model_metadata.get_num_hidden_layers(),
        seed_for_random_weight=test_case.seed if test_case.use_random_weight else None,
        quantize_artifact_path=quantize_artifact_path,
        compiler_config_overrides=test_case.compiler_config_overrides,
        num_blocks_per_supertask=test_case.num_blocks_per_supertask,
        embed_all_constants_into_graph=test_case.embed_all_constants_into_graph,
        kv_cache_sharing_across_beams_config=test_case.kv_cache_sharing_across_beams_config,
        paged_attention_num_blocks=test_case.paged_attention_num_blocks,
    )

    builder.build(
        artifacts_export_path,
        num_pipeline_builder_workers=num_pipeline_builder_workers,
        num_compile_workers=num_compile_workers,
        _cleanup=_cleanup,
    )
