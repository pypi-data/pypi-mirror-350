from contextlib import AbstractContextManager, nullcontext
import copy
from copy import deepcopy
import functools
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any, ContextManager, Dict, Final, Iterable, Mapping, Optional, Tuple, Type, Union

import cachetools
from cachetools.keys import hashkey
import furiosa_llm_models
from pydantic import BaseModel, Field, model_validator
import torch
import transformers
from transformers import PretrainedConfig, PreTrainedModel, set_seed
from typing_extensions import Self

from furiosa_llm.optimum import AttentionType, OptimizationConfig, QDtype, QuantizationConfig
import furiosa_llm.optimum.modeling
from furiosa_llm.optimum.modeling import (
    LLAMA3_1_8B_ELICEAI_HELPY_EDU_B_PRETRAINED_ID,
    MODEL_CLS_TO_MLPERF_OPT_CONFIGS,
    SOLAR_10D7B_INSTRUCT_PRETRAINED_ID,
    AutoModel,
    AutoModelForCausalLM,
    AutoModelForQuestionAnswering,
    DecomposedLayerNorm,
    _FuriosaBaseAutoModelClass,
    _get_quant_causal_lm,
    convert_config_for_optimized_cls,
    get_mapped_class_for_optimization,
    get_optimized_cls,
    is_generative_model,
    is_llama3_based,
    is_mlperf_optimized,
    is_mlperf_optimized_with,
    replace_layernorm,
    requires_parameter_names_conversion,
    update_config_inplace,
)
from furiosa_llm.optimum.types import LLMConfig

from ..utils import get_logger_with_tz
from .config_types import Bucket, KvCacheSharingAcrossBeamsConfig
from .utils import generate_input_sample

DEFAULT_SEED_VALUE: Final = 42

# The maximum number of `Model.pretrained_models` kept.
# A custom pytest hook is used to group parametrized tests to work around this limit.
# Note that this should be at least 2 because quantized models recursively load base models!
PRETRAINED_MODEL_CACHE_SIZE: Final = 2
FURIOSA_LLM_PACKAGE_PATH: Final = Path(__file__).parent.parent
TINY_GPTJ_CONFIG: Final[Dict[str, Any]] = {
    "n_embd": 32,
    "rotary_dim": 2,
    "n_inner": 1,
}

MODEL_CONFIG_ROOT_DIR = Path(__file__).parent.with_name("model_configs")

with open(MODEL_CONFIG_ROOT_DIR / "LLaMA3.1-8B.json") as f:
    LLAMA3_1_8B_CONFIG = json.load(f)

with open(MODEL_CONFIG_ROOT_DIR / "LLaMA3.1-70B.json") as f:
    LLAMA3_1_70B_CONFIG = json.load(f)


logger = get_logger_with_tz(logging.getLogger(__name__))

TASK_TYPE_TO_AUTO_MODEL_CLASS: Final[Dict[str, Type[PreTrainedModel]]] = {
    "text-generation": AutoModelForCausalLM,
    "question-answering": AutoModelForQuestionAnswering,
}


# Cache based on `pretrained_id`` only.
@cachetools.cached(
    cache=cachetools.LRUCache(128), key=lambda pretrained_id, _: hashkey(pretrained_id)
)
def get_config_from_pretrained_id(
    pretrained_id: str, trust_remote_code: Optional[bool]
) -> PretrainedConfig:
    return transformers.AutoConfig.from_pretrained(
        pretrained_id, trust_remote_code=trust_remote_code
    )


class DummyModel(torch.nn.Module):
    def __init__(self, batch_size: int = 1):
        super(DummyModel, self).__init__()
        self.linear1 = torch.nn.Linear(16, batch_size)

    def forward(self, x):
        return self.linear1(x)


def get_model_cls_from_pretrained_id(
    pretrained_id: str, trust_remote_code: Optional[bool], task_type: Optional[str] = None
) -> Type[PreTrainedModel]:
    model_config = get_config_from_pretrained_id(pretrained_id, trust_remote_code)
    supported_architectures = getattr(model_config, "architectures", [])

    if task_type:
        if auto_model_cls := TASK_TYPE_TO_AUTO_MODEL_CLASS.get(task_type):
            return auto_model_cls.find_model_class(
                pretrained_id,
                model_config,
                trust_remote_code=trust_remote_code,
            )
        else:
            raise NotImplementedError(f"Unsupported task_type: {task_type}")
    else:
        if len(supported_architectures) != 1:
            raise ValueError(
                f"Task type not given, but multiple architectures found: {supported_architectures}"
            )

        if model_cls := getattr(transformers, supported_architectures[0], None):
            return model_cls

        # Model should be loaded with remote code.
        if not hasattr(model_config, "auto_map"):
            raise ValueError(
                f"Model {pretrained_id} is not a local model, but does not have an auto map in config."
            )
        auto_class_names = [
            auto_class_name
            for auto_class_name, class_ref in model_config.auto_map.items()
            if class_ref.rsplit('.', maxsplit=1)[-1] == supported_architectures[0]
        ]
        assert len(auto_class_names) == 1
        auto_class_name = auto_class_names[0]
        if not (module_finder := getattr(furiosa_llm.optimum.modeling, auto_class_name)):
            raise ValueError(f"Unsupported auto model class type: {auto_class_name}")
        assert issubclass(module_finder, _FuriosaBaseAutoModelClass)
        return module_finder.find_model_class(
            pretrained_id,
            model_config,
            trust_remote_code=trust_remote_code,
        )


def get_default_task_type_from_pretrained_id(
    pretrained_id: str, trust_remote_code: Optional[bool]
) -> str:
    model_cls = get_model_cls_from_pretrained_id(pretrained_id, trust_remote_code)
    if model_cls in transformers.MODEL_FOR_CAUSAL_LM_MAPPING.values():
        return "text-generation"
    elif model_cls in transformers.MODEL_FOR_QUESTION_ANSWERING_MAPPING.values():
        return "question-answering"
    else:
        raise ValueError(f"cannot set task_type automatically for {model_cls}")


@functools.total_ordering
class ModelMetadata(BaseModel):
    pretrained_id: str
    task_type: Optional[str] = None
    llm_config: LLMConfig = Field(default_factory=LLMConfig)
    hf_configs: Dict[str, Any] = Field(default_factory=dict)
    # path to load pre-trained model weights (optional)
    model_weight_path: Optional[os.PathLike] = None
    trust_remote_code: Optional[bool] = None
    allow_bfloat16_cast_with_mcp: bool = True

    # This field exists only for artifact backward compatibility.
    auto_bfloat16_cast: Optional[bool] = True

    @model_validator(mode='after')
    def validate_model_metadata(self):
        if self.task_type is None:
            self.task_type = get_default_task_type_from_pretrained_id(
                self.pretrained_id, self.trust_remote_code
            )
        assert self.task_type in transformers.pipelines.SUPPORTED_TASKS, "unsupported task_type"
        return self

    @property
    @functools.lru_cache
    def model_cls(self) -> Type[PreTrainedModel]:
        return get_model_cls_from_pretrained_id(
            self.pretrained_id, self.trust_remote_code, self.task_type
        )

    @property
    def _is_tiny_gptj(self) -> bool:
        config_without_num_hidden_layers = {
            k: v for k, v in self.hf_configs.items() if k != "num_hidden_layers"
        }

        return (
            self.model_cls == transformers.GPTJForCausalLM
            and config_without_num_hidden_layers == TINY_GPTJ_CONFIG
        )

    @property
    def num_hidden_layers(self) -> int:
        return (
            self.config_dict.get("num_hidden_layers")
            or self.config_dict.get("num_layers")
            or self.config_dict["n_layer"]
        )

    @property
    def attention_type(self) -> AttentionType:
        return self.llm_config.optimization_config.attention_type

    @property
    def optimize_options(self) -> OptimizationConfig:
        return self.llm_config.optimization_config

    @property
    def quantization_config(self) -> Optional[QuantizationConfig]:
        return self.llm_config.quantization_config

    def __init__(
        self,
        pretrained_id: str,
        task_type: Optional[str] = None,
        llm_config: LLMConfig = LLMConfig(),
        hf_configs: Dict = {},
        model_weight_path: Optional[os.PathLike] = None,
        trust_remote_code: Optional[bool] = None,
        allow_bfloat16_cast_with_mcp: bool = True,
        # This arg exists for artifact backward compatibility.
        auto_bfloat16_cast: Optional[bool] = None,
    ):
        super(ModelMetadata, self).__init__(
            pretrained_id=pretrained_id,
            task_type=task_type,
            llm_config=llm_config,
            hf_configs=hf_configs,
            model_weight_path=model_weight_path,
            trust_remote_code=trust_remote_code,
            allow_bfloat16_cast_with_mcp=allow_bfloat16_cast_with_mcp,
            auto_bfloat16_cast=auto_bfloat16_cast,
        )

        # If the model is not quantized and can be casted to bfloat16, enable auto bf16 cast.
        if not self.quantization_config and (
            (self.config_dict.get("torch_dtype") == "bfloat16" and allow_bfloat16_cast_with_mcp)
            or auto_bfloat16_cast
        ):
            self._enable_auto_bfloat16_cast()

    @classmethod
    def init_with_mlperf_optim_options(
        cls,
        pretrained_id: str,
        quantization_config: Optional[QuantizationConfig] = None,
        hf_configs: Dict = {},
        model_weight_path: Optional[os.PathLike] = None,
        trust_remote_code: Optional[bool] = None,
        allow_bfloat16_cast_with_mcp: bool = True,
    ) -> Self:
        return cls(
            pretrained_id=pretrained_id,
            llm_config=LLMConfig(
                optimization_config=ModelMetadata.get_mlperf_options(
                    get_model_cls_from_pretrained_id(pretrained_id, trust_remote_code)
                ),
                quantization_config=quantization_config,
            ),
            hf_configs=hf_configs,
            model_weight_path=model_weight_path,
            trust_remote_code=trust_remote_code,
            allow_bfloat16_cast_with_mcp=allow_bfloat16_cast_with_mcp,
        )

    def with_num_layers(self, num_hidden_layers: int) -> Self:
        return self.model_copy(
            update={
                "hf_configs": {**self.hf_configs, "num_hidden_layers": num_hidden_layers},
            },
            deep=True,
        )

    def with_hf_configs(self, hf_configs: Mapping[str, Any]) -> Self:
        new_hf_configs = deepcopy(self.hf_configs)
        new_hf_configs.update(hf_configs)
        return self.model_copy(
            update={
                "hf_configs": new_hf_configs,
            },
            deep=True,
        )

    def with_quantization_config(self, quantization_config: QuantizationConfig) -> Self:
        return self.model_copy(
            update={
                "llm_config": self.llm_config.with_quantization_config(quantization_config),
            },
            deep=True,
        )

    def with_optimizations(self, opts: Union[Dict[str, Any], str]) -> Self:
        if isinstance(opts, str):
            opts = {opts: True}
        return self.model_copy(
            update={
                "llm_config": self.llm_config.with_optimizations(opts),
            },
            deep=True,
        )

    @property
    def is_beam_search_kv_cache_sharing_model(self) -> bool:
        return (
            self.model_cls is transformers.GPTJForCausalLM
            and self.optimize_options.kv_cache_sharing_across_beams
        )

    def is_compact_causal_mask_for_bert(self) -> bool:
        return (
            self.model_cls is transformers.BertForQuestionAnswering
            and self.optimize_options.compact_causal_mask
        )

    @staticmethod
    def get_mlperf_options(model_cls: Type[PreTrainedModel]) -> OptimizationConfig:
        model_cls = get_mapped_class_for_optimization(model_cls)

        if optim_options := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(model_cls):
            return optim_options
        raise NotImplementedError(f"Unsupported mlperf model variant: {model_cls}")

    @staticmethod
    def mlperf_option_exists(model_cls: Type[PreTrainedModel]) -> bool:
        return model_cls in MODEL_CLS_TO_MLPERF_OPT_CONFIGS

    @property
    def contains_mlperf_opts(self) -> bool:
        return ModelMetadata.mlperf_option_exists(  # fmt: off
            self.model_cls
        ) and self.optimize_options.contains(self.get_mlperf_options(self.model_cls))

    @property
    def use_paged_attention(self) -> bool:
        return self.attention_type == AttentionType.PAGED_ATTENTION

    def __str__(self):
        name = self.pretrained_id.rsplit("/", maxsplit=1)[-1]

        return "{}{}_{}L{}{}".format(
            "TINY_" if self._is_tiny_gptj else "",
            name,
            self.get_num_hidden_layers(),
            f"_{self.get_optimized_cls().__module__}",
            f"_{self.quantization_config}" if self.is_quantized else "",
        )

    @property
    def name(self):
        return self.__str__()

    @property
    def __hash_key(self):
        """A hashable key to uniquely identify the model metadata."""

        # Convert the nested values to hashable types in a recursively way
        def hashable_dict(d):
            return frozenset(
                (
                    k,
                    (
                        hashable_dict(v)
                        if isinstance(v, dict)
                        else tuple(v) if isinstance(v, list) else v
                    ),
                )
                for k, v in d.items()
            )

        hashable_hf_configs = {
            k: (hashable_dict(v) if isinstance(v, dict) else tuple(v) if isinstance(v, list) else v)
            for k, v in self.hf_configs.items()
        }

        return (
            self.pretrained_id,
            self.task_type,
            not self.optimize_options.optimize_furiosa,
            self.hf_configs.get("num_hidden_layers"),
            self.attention_type,
            self.optimize_options,
            self.quantization_config,
            frozenset(hashable_hf_configs.items()),
        )

    def __eq__(self, other):
        if not isinstance(other, ModelMetadata):
            return False
        return self.__hash_key == other.__hash_key

    def __lt__(self, other):
        if not isinstance(other, ModelMetadata):
            return NotImplemented
        return self.__hash_key < other.__hash_key

    def __hash__(self):
        return hash(self.__hash_key)

    def get_num_hidden_layers(self) -> int:
        """Retrieve the number of hidden layers in the model.

        If the number of hidden layers was specified during initialization, it returns that value.
        Otherwise, it returns the total number of layers in the model variant.

        Returns:
            int: The number of hidden layers.

        Raises:
            ValueError: If the number of layers in the model variant is unknown.
        """
        return self.hf_configs.get("num_hidden_layers", self.full_layer_count)

    @property
    def pretrained_name(self) -> str:
        return self.pretrained_id

    @property
    def is_generative_model(self) -> bool:
        return self.task_type == "text-generation" or is_generative_model(self.model_cls)

    @property
    def kv_cache_torch_dtype(self) -> Optional[torch.dtype]:
        return self.kv_cache_dtype.to_torch_dtype() if self.kv_cache_dtype else None

    @property
    def kv_cache_dtype(self) -> Optional[QDtype]:
        if not self.is_generative_model:
            return None
        if self.quantization_config:
            return self.quantization_config.kv_cache
        return QDtype.FP32

    @property
    def is_quantized(self) -> bool:
        return self.quantization_config is not None

    @property
    def need_quant_artifacts(self) -> bool:
        # BF16 model doesn't need qparam, qformat files.
        return (
            self.quantization_config is not None
            and self.quantization_config.use_mcp
            and not (self.allow_bfloat16_cast_with_mcp and self.quantization_config.is_bf16)
        )

    def with_allowing_bf16_cast_with_mcp(self) -> Self:
        return self.model_copy(
            update={
                "allow_bfloat16_cast_with_mcp": True,
            },
            deep=True,
        )

    def with_auto_bfloat16_cast(self) -> Self:
        if self.is_generative_model:
            quant_config = QuantizationConfig.w_16_a_16_kv_16()
        else:
            quant_config = QuantizationConfig.w_16_a_16()
        return self.with_quantization_config(quant_config).with_allowing_bf16_cast_with_mcp()

    def _enable_auto_bfloat16_cast(self) -> None:
        if self.is_generative_model:
            quant_config = QuantizationConfig.w_16_a_16_kv_16()
        else:
            quant_config = QuantizationConfig.w_16_a_16()
        self.llm_config = self.llm_config.with_quantization_config(quant_config)
        self.allow_bfloat16_cast_with_mcp = True

    @property
    def full_layer_count(self) -> int:
        config = get_config_from_pretrained_id(self.pretrained_name, self.trust_remote_code)

        if full_layer_cnt := getattr(
            config, "num_hidden_layers", getattr(config, "n_layers", None)
        ):
            return full_layer_cnt
        raise ValueError(f"Unknown number of hidden layers for {self}")

    @property
    def config(self) -> PretrainedConfig:
        config_original: PretrainedConfig = get_config_from_pretrained_id(
            self.pretrained_name, self.trust_remote_code
        )
        config = copy.deepcopy(config_original)

        # Some `PretrainedConfig` types may have non-standard attribute names,
        # so we use the config's `attribute_map` to validate key names.
        attribute_map_of_config = getattr(config, "attribute_map", {})
        valid_config_attributes = {*config.__dict__.keys(), *attribute_map_of_config.keys()}
        for key, val in self.hf_configs.items():
            if key not in valid_config_attributes:
                logger.warning(
                    f"{key} in hf_configs is not valid attribute of {type(config_original)}, and it will be ignored."
                )
            setattr(config, key, val)

        update_config_inplace(self.pretrained_id, config, self.optimize_options)
        return config

    @property
    def config_dict(self) -> Dict[str, Any]:
        return self.config.to_dict()

    @property
    def is_mlperf_optimized(self) -> bool:
        return is_mlperf_optimized(self.model_cls, self.optimize_options)

    def is_mlperf_optimized_with(self, **kwargs) -> bool:
        return is_mlperf_optimized_with(self.model_cls, self.optimize_options)

    def get_optimized_cls(self) -> Type[PreTrainedModel]:
        return get_optimized_cls(self.pretrained_id, self.model_cls, self.optimize_options)

    @property
    def model_qname(self) -> str:
        cls_type = self.get_optimized_cls()
        return f"{cls_type.__module__}.{cls_type.__name__}"

    @functools.lru_cache(maxsize=1)
    def _random_weight_model(
        self,
        seed: int,
        qformat_path: Optional[os.PathLike],
        qparam_path: Optional[os.PathLike],
        run_gc: bool,
    ) -> PreTrainedModel:
        # FIXME: This is a workaround to reduce memory usage
        self._pretrained_model.cache_clear()
        if run_gc:
            import gc

            gc.collect()
        set_seed(seed)
        print(f"\x1b[1;36m(Creating {self} with random weights)\x1b[0m", end="", file=sys.stderr)
        sys.stderr.flush()

        ctx_mgr: Union[AbstractContextManager[Any], ContextManager[Any]]
        if self.optimize_options.decompose_layernorm:
            ctx_mgr = replace_layernorm(DecomposedLayerNorm)
        else:
            ctx_mgr = nullcontext()
        with ctx_mgr:
            if requires_parameter_names_conversion(self.pretrained_id, self.model_cls):
                config = convert_config_for_optimized_cls(self.config, self.get_optimized_cls())
            else:
                config = self.config
            model = self.get_optimized_cls()(config=config)

        model.eval()
        model.requires_grad_(False)

        if self.optimize_options.decompose_layernorm:
            model.config.decompose_layernorm = True

        if self.is_quantized and self.need_quant_artifacts:
            if not (qformat_path and qparam_path):
                raise ValueError(
                    "Both `qparam_path` and `qformat_path` should be given for quantization."
                )
            return _get_quant_causal_lm(
                model,
                self.optimize_options,
                qformat_path=qformat_path,
                qparam_path=qparam_path,
            )
        else:
            return model

    # FIXME: This wraps internal function to properly cache the model(because of default args)
    def random_weight_model(
        self,
        seed: int = DEFAULT_SEED_VALUE,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        run_gc: bool = True,
    ) -> PreTrainedModel:
        return self._random_weight_model(seed, qformat_path, qparam_path, run_gc)  # type: ignore[arg-type]

    @functools.lru_cache(maxsize=PRETRAINED_MODEL_CACHE_SIZE)
    def _pretrained_model(
        self,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        quant_ckpt_file_path: Optional[os.PathLike] = None,
        run_gc: bool = True,
    ) -> PreTrainedModel:
        # FIXME: This is a workaround to reduce memory usage
        self._random_weight_model.cache_clear()
        if run_gc:
            import gc

            gc.collect()
        print(f"\x1b[1;36m(Loading {self})\x1b[0m", end="", file=sys.stderr)
        sys.stderr.flush()

        # Make sure qformat_path and qparam_path are given together or not given at all.
        if qformat_path and os.path.isfile(qformat_path):
            assert qparam_path and os.path.isfile(qparam_path), "qparam_path should be given."
        if qparam_path and os.path.isfile(qparam_path):
            assert qformat_path and os.path.isfile(qformat_path), "qformat_path should be given."

        # Make sure qparam_path, qformat_path, and quant_ckpt_file_path (optional) are
        # under the same directory and set quantization_checkpt_path to the directory.
        # It's necessary because AutoModel.from_pretrained uses a specific directory
        # to load quantization artifacts (qparam.npy, qformat.yaml, and exported_model.qckpt).
        quantization_checkpt_path = None
        if qparam_path and qformat_path:
            # Make sure qparam_path and qformat_path are belong to the same parent directory
            assert os.path.dirname(qparam_path) == os.path.dirname(
                qformat_path
            ), "qparam_path and qformat_path should be in the same directory."
            if (
                quant_ckpt_file_path
            ):  # if quant_ckpt_file_path is given, make sure it is in the same directory
                assert os.path.dirname(quant_ckpt_file_path) == os.path.dirname(
                    qparam_path
                ), "quant_ckpt_file_path should be in the same directory."

            # Set quantization_checkpt_path to the parent directory of qformat.yaml, qparam.npy,
            #   and exported_model.qckpt (optional)
            quantization_checkpt_path = os.path.dirname(qformat_path)

        auto_model_cls: Optional[Type[_FuriosaBaseAutoModelClass]]
        if self.task_type is None:
            auto_model_cls = AutoModel
        else:
            auto_model_cls = TASK_TYPE_TO_AUTO_MODEL_CLASS.get(self.task_type)
            if auto_model_cls is None:
                raise ValueError(f"Unsupported task_type: {self.task_type}")

        return auto_model_cls.from_pretrained(
            model_id=self.pretrained_id,
            config=self.config,
            optimization_config=self.optimize_options,
            quantization_checkpt_path=quantization_checkpt_path,
            trust_remote_code=self.trust_remote_code,
            auto_bfloat16_cast=self.quantization_config
            and self.quantization_config.is_bf16
            and self.allow_bfloat16_cast_with_mcp,
            _disable_bfloat16_cast=not self.allow_bfloat16_cast_with_mcp,
        )

    # FIXME: This wraps internal function to properly cache the model
    def pretrained_model(
        self,
        qformat_path: Optional[os.PathLike] = None,
        qparam_path: Optional[os.PathLike] = None,
        quant_ckpt_file_path: Optional[os.PathLike] = None,
        run_gc: bool = True,
    ) -> PreTrainedModel:
        return self._pretrained_model(qformat_path, qparam_path, quant_ckpt_file_path, run_gc)  # type: ignore[arg-type]

    def has_side_effect(self) -> bool:
        return self.attention_type == AttentionType.PAGED_ATTENTION

    def is_model_available(self) -> bool:
        if not self.is_quantized:
            return True

        if self.get_optimized_cls() in (
            furiosa_llm_models.gptj.symbolic.huggingface.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.preallocated_concat_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.huggingface_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.paged_attention_rope.GPTJForCausalLM,
            furiosa_llm_models.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
        ):
            return False

        # These models are temporarily available.
        UNAVAILABLE_PAIRS = {
            (SOLAR_10D7B_INSTRUCT_PRETRAINED_ID, QuantizationConfig.w_16_a_16_kv_16()),
            (
                LLAMA3_1_8B_ELICEAI_HELPY_EDU_B_PRETRAINED_ID,
                QuantizationConfig.w_f8_a_f8_kv_f8(),
            ),
            (
                LLAMA3_1_8B_ELICEAI_HELPY_EDU_B_PRETRAINED_ID,
                QuantizationConfig.w_16_a_16_kv_16(),
            ),
            (
                SOLAR_10D7B_INSTRUCT_PRETRAINED_ID,
                QuantizationConfig.w_f8_a_f8_kv_f8(),
            ),
        }
        if (self.pretrained_id, self.quantization_config) in UNAVAILABLE_PAIRS:
            return False

        # All w4a16 models are temporarily unavailable.
        if self.quantization_config in (QuantizationConfig.w_4_a_16_kv_f8(),):
            return False

        return True

    def test_uses_models(self) -> Iterable[str]:
        return [self.name]

    # FIXME: make this robust
    def is_random_weight_only_model(self) -> bool:
        return "n_embd" in self.hf_configs

    def is_llama3_based(self) -> bool:
        return is_llama3_based(self.pretrained_id, type(self.config))

    @property
    def supports_speculative_decoding(self) -> bool:
        return self.get_optimized_cls() in (
            furiosa_llm_models.llama3.symbolic.aramco_specdec.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.aramco_specdec_slice_integrated.LlamaForCausalLM,
        )

    @property
    def seq_dim_in_logits(self) -> int:
        """Returns which dimension is sequence dimension in output logits tensor."""
        # This function is used for prefill last block slicing.
        if get_mapped_class_for_optimization(self.model_cls) in {
            transformers.GPTJForCausalLM,
            transformers.BertForQuestionAnswering,
            transformers.LlamaForCausalLM,
        }:
            return 1
        else:
            raise NotImplementedError(f"Sequence dimension in logits for model {self} is unknown")

    def get_output_logits_size(self, bucket: Bucket) -> Optional[int]:
        if not self.is_generative_model:
            return None
        if self.optimize_options.calculate_logit_only_for_last_token and bucket.is_prefill:
            return 1
        return bucket.input_ids_size

    def get_example_input(
        self,
        bucket: Bucket,
        paged_attention_num_blocks: Optional[int] = None,
        paged_attention_block_size: Optional[int] = None,
        kv_cache_sharing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig] = None,
        random_value: bool = False,
    ) -> Tuple[Tuple, Dict]:
        if self.attention_type is AttentionType.PAGED_ATTENTION:
            if not paged_attention_num_blocks:
                raise ValueError(
                    "`paged_attention_num_blocks` should be given for paged attention models."
                )
            if not paged_attention_block_size:
                raise ValueError(
                    "`paged_attention_block_size` should be given for paged attention models."
                )
        else:
            if paged_attention_num_blocks is not None:
                raise ValueError(
                    "`paged_attention_num_blocks` should be given if and only if the model is paged attention model."
                )
            if paged_attention_block_size is not None:
                raise ValueError(
                    "`paged_attention_block_size` should be given if and only if the model is paged attention model."
                )

        if self.is_beam_search_kv_cache_sharing_model:
            if not kv_cache_sharing_across_beams_config:
                raise ValueError(
                    "`kv_cache_sharing_across_beams_config` should be given if the model is optimized for kv cache sharing across beams."
                )
        else:
            if kv_cache_sharing_across_beams_config is not None:
                raise ValueError(
                    "`kv_cache_sharing_across_beams_config` should be given if and only if the model is optimized for kv cache sharing across beams."
                )

        if not self.is_generative_model and not bucket.is_prefill:
            raise ValueError("encoder-only model supports prefill mode only")

        use_causal_mask = self.optimize_options.causal_mask_free_decoding

        return (), generate_input_sample(
            self.config,
            bucket,
            self.kv_cache_torch_dtype,
            paged_attention_num_blocks,
            paged_attention_block_size,
            kv_cache_sharing_across_beams_config,
            self.optimize_options.optimize_packed,
            self.is_compact_causal_mask_for_bert(),
            use_causal_mask,
            self.supports_speculative_decoding,
            self.need_quant_artifacts,
            self.optimize_options.calculate_logit_only_for_last_token,
            random_value=random_value,
        )
