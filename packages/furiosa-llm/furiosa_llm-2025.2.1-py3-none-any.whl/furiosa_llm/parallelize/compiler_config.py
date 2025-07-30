from dataclasses import dataclass
from enum import Enum
import logging
from typing import Mapping, Optional

import yaml

from furiosa.native_compiler import create_default_compiler_config, create_llm_compiler_config
from furiosa_llm.models import ModelMetadata
from furiosa_llm.models.config_types import Bucket
from furiosa_llm.utils import get_logger_with_tz

logger = get_logger_with_tz(logging.getLogger(__name__))


class PipelineMode(Enum):
    UNKNOWN = "unknown"
    LLM_PREFILL = "prefill"
    LLM_DECODE = "decode"

    def __str__(self):
        return self.value

    @classmethod
    def _missing_(cls, value):
        if value is None:
            return cls.UNKNOWN


class BlockType(str, Enum):
    FIRST = "first"
    MID = "mid"
    LAST = "last"
    WHOLE = "all_merged"

    def __str__(self):
        return self.value


# FIXME: CompilerConfigContext must provide more generic way to match between target node and compiler config.
# the following implementation is MLPerf-specific (mostly targets gptj and bert) and should be fixed in the future.
@dataclass
class CompilerConfigContext:
    model_metadata: ModelMetadata
    num_pe: Optional[int] = None
    block_type: Optional[BlockType] = None
    bucket: Optional[Bucket] = None
    phase: Optional[PipelineMode] = None
    beam_size: Optional[int] = None
    compiler_config_overrides: Optional[Mapping] = None

    def load_config(self) -> Mapping:
        logger.info(f"Loading compiler config for {self}")
        config: Optional[Mapping] = None
        if self.bucket:
            config_yaml = create_llm_compiler_config(
                self.model_metadata.pretrained_id,
                self.num_pe or 8,
                self.bucket.batch_size,
                self.bucket.attention_size,
                self.bucket.input_ids_size,
                str(self.block_type),
            )
            logger.info(f"Generated compiler config yaml: {config_yaml}")
            if config_yaml:
                config = yaml.safe_load(config_yaml)

        if config is None:
            logger.info("Failed to create compiler config; using default compiler config")
            config_yaml = create_default_compiler_config()
            config = yaml.safe_load(config_yaml)

        if self.compiler_config_overrides is not None:
            config = {**config, **self.compiler_config_overrides}
        return config
