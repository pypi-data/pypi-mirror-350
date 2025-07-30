# Adapted from
# https://github.com/vllm-project/vllm/blob/4ef41b84766670c1bd8079f58d35bf32b5bcb3ab/vllm/entrypoints/openai/protocol.py
import time
from typing import Any, Dict, List, Literal, Optional, Union

from openai.types.chat import ChatCompletionMessageParam
from openai.types.model import Model as OpenAIModel
from pydantic import BaseModel, ConfigDict, Field

from furiosa_llm.api import LLM, SamplingParams
from furiosa_llm.outputs import Logprob
from furiosa_llm.server.utils import random_uuid


class OpenAIBaseModel(BaseModel):
    # OpenAI API does not allow extra fields
    model_config = ConfigDict(extra="forbid")


class CompletionTokenUsageInfo(OpenAIBaseModel):
    accepted_prediction_tokens: int = 0
    audio_tokens: int = 0
    reasoning_tokens: int = 0
    rejected_prediction_tokens: int = 0


class UsageInfo(OpenAIBaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0
    completion_tokens_details: Optional[CompletionTokenUsageInfo] = None


class StreamOptions(OpenAIBaseModel):
    include_usage: Optional[bool] = True


class FunctionDefinition(OpenAIBaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class ChatCompletionToolsParam(OpenAIBaseModel):
    type: Literal["function"] = "function"
    function: FunctionDefinition


class ChatCompletionNamedFunction(OpenAIBaseModel):
    name: str


class ChatCompletionNamedToolChoiceParam(OpenAIBaseModel):
    function: ChatCompletionNamedFunction
    type: Literal["function"] = "function"


class ChatCompletionRequest(OpenAIBaseModel):
    messages: List[ChatCompletionMessageParam]
    model: str
    logprobs: Optional[bool] = False
    top_logprobs: Optional[int] = None
    n: Optional[int] = 1
    temperature: Optional[float] = 1.0
    stream: Optional[bool] = False
    stream_options: Optional[StreamOptions] = None
    top_p: Optional[float] = 1.0
    best_of: Optional[int] = 1
    use_beam_search: bool = False
    top_k: int = -1
    min_p: float = 0.0
    length_penalty: float = 1.0
    early_stopping: bool = False
    min_tokens: int = 0

    # TODO: completely remove max_tokens when OpenAI removes it
    max_tokens: Optional[int] = Field(
        default=None,
        deprecated='max_tokens is deprecated in favor of the max_completion_tokens field',
    )
    max_completion_tokens: Optional[int] = None

    tools: Optional[List[ChatCompletionToolsParam]] = None
    tool_choice: Optional[
        Union[Literal["none"], Literal["auto"], ChatCompletionNamedToolChoiceParam]
    ] = None
    # NOTE this will be ignored -- the model determines the behavior
    parallel_tool_calls: Optional[bool] = True

    add_generation_prompt: bool = True

    return_tokens_as_token_ids: Optional[bool] = Field(
        default=None,
        description="If specified with 'logprobs', tokens are represented as strings of the form 'token_id:{token_id}' so that tokens that are not JSON-encodable can be identified.",
    )

    # Parameters that is supported by OpenAI but not by Furiosa.
    # All of them are no-op, but declared to prevent errors caused by extra="forbid"
    audio: Optional[Dict[str, Any]] = None
    frequency_penalty: Optional[float] = 0.0
    function_call: Optional[Union[str, Dict[str, Any]]] = None  # Deprecated
    functions: Optional[List[Any]] = None  # Deprecated
    logit_bias: Optional[Dict[int, float]] = None
    metadata: Optional[Dict[str, Any]] = None
    modalities: Optional[List[str]] = None
    prediction: Optional[Dict[str, Any]] = None
    presence_penalty: Optional[float] = 0.0
    reasoning_effort: Optional[str] = "medium"
    response_format: Optional[Dict[str, Any]] = None
    seed: Optional[int] = None
    service_tier: Optional[str] = "auto"
    stop: Optional[Union[str, List[str]]] = None
    store: Optional[bool] = False
    user: Optional[str] = None
    web_search_options: Optional[Dict[str, Any]] = None

    def to_sampling_params(self) -> SamplingParams:
        max_tokens = self.max_completion_tokens or self.max_tokens
        return SamplingParams.from_optional(
            n=self.n,
            best_of=self.best_of,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            use_beam_search=self.use_beam_search,
            length_penalty=self.length_penalty,
            early_stopping=self.early_stopping,
            logprobs=self.top_logprobs if self.logprobs else None,
            max_tokens=max_tokens,
            min_tokens=self.min_tokens,
        )


class CompletionRequest(OpenAIBaseModel):
    model: str
    prompt: Union[str, List[str], List[int], List[List[int]]]
    best_of: Optional[int] = 1
    logprobs: Optional[int] = None
    max_tokens: Optional[int] = 16
    n: int = 1
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0

    stream: Optional[bool] = False
    # XXX: stream_options has no effect in the current implementation
    stream_options: Optional[StreamOptions] = None
    use_beam_search: bool = False
    top_k: int = -1
    min_p: float = 0.0
    length_penalty: float = 1.0
    early_stopping: bool = False
    min_tokens: int = 0

    return_tokens_as_token_ids: Optional[bool] = Field(
        default=None,
        description=(
            "If specified with 'logprobs', tokens are represented as strings of the form 'token_id:{token_id}' so that tokens that are not JSON-encodable can be identified."
        ),
    )

    # Parameters that is supported by OpenAI but not by Furiosa.
    # All of them are no-op, but declared to prevent errors caused by extra="forbid"
    echo: Optional[bool] = False
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[int, float]] = None
    presence_penalty: Optional[float] = 0.0
    seed: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    suffix: Optional[str] = None
    user: Optional[str] = None

    def to_sampling_params(self) -> SamplingParams:
        return SamplingParams.from_optional(
            n=self.n,
            best_of=self.best_of,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            use_beam_search=self.use_beam_search,
            length_penalty=self.length_penalty,
            early_stopping=self.early_stopping,
            logprobs=self.logprobs,
            max_tokens=self.max_tokens,
            min_tokens=self.min_tokens,
        )


class CompletionLogProbs(OpenAIBaseModel):
    text_offset: List[int] = Field(default_factory=list)
    token_logprobs: List[Optional[float]] = Field(default_factory=list)
    tokens: List[str] = Field(default_factory=list)
    top_logprobs: List[Optional[Dict[str, float]]] = Field(default_factory=list)


class CompletionResponseChoice(OpenAIBaseModel):
    index: int
    text: str
    logprobs: Optional[CompletionLogProbs] = None
    finish_reason: Optional[str] = None
    prompt_logprobs: Optional[List[Optional[Dict[int, Logprob]]]] = None


class CompletionResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"cmpl-{random_uuid()}")
    object: str = "text_completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[CompletionResponseChoice]
    usage: UsageInfo


class CompletionResponseStreamChoice(OpenAIBaseModel):
    index: int
    text: str
    logprobs: Optional[CompletionLogProbs] = None
    finish_reason: Optional[str] = None


class CompletionStreamResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"cmpl-{random_uuid()}")
    object: str = "text_completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[CompletionResponseStreamChoice]
    usage: Optional[UsageInfo] = Field(default=None)


class EmbeddingResponseData(OpenAIBaseModel):
    index: int
    object: str = "embedding"
    embedding: Union[List[float], str]


class EmbeddingResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"cmpl-{random_uuid()}")
    object: str = "list"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    data: List[EmbeddingResponseData]
    usage: UsageInfo


class FunctionCall(OpenAIBaseModel):
    name: str
    arguments: str


class ToolCall(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-tool-{random_uuid()}")
    type: Literal["function"] = "function"
    function: FunctionCall


class ChatMessage(OpenAIBaseModel):
    role: str
    content: Optional[str] = None
    reasoning_content: Optional[str] = None
    tool_calls: List[ToolCall] = Field(default_factory=list)


class ChatCompletionLogProb(OpenAIBaseModel):
    token: str
    logprob: float = -9999.0
    bytes: Optional[List[int]] = None


class ChatCompletionLogProbsContent(ChatCompletionLogProb):
    top_logprobs: List[ChatCompletionLogProb] = Field(default_factory=list)


class ChatCompletionLogProbs(OpenAIBaseModel):
    content: Optional[List[ChatCompletionLogProbsContent]] = None


class ChatCompletionResponseChoice(OpenAIBaseModel):
    index: int
    message: ChatMessage
    logprobs: Optional[ChatCompletionLogProbs] = None
    finish_reason: Optional[str] = None


class ChatCompletionResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{random_uuid()}")
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo
    prompt_logprobs: Optional[List[Optional[Dict[int, Logprob]]]] = None


class DeltaFunctionCall(BaseModel):
    name: Optional[str] = None
    arguments: Optional[str] = None


# a tool call delta where everything is optional
class DeltaToolCall(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-tool-{random_uuid()}")
    type: Literal["function"] = "function"
    function: Optional[DeltaFunctionCall] = None


class DeltaMessage(OpenAIBaseModel):
    role: Optional[str] = None
    content: Optional[str] = None
    reasoning_content: Optional[str] = None
    tool_calls: List[DeltaToolCall] = Field(default_factory=list)


class ChatCompletionResponseStreamChoice(OpenAIBaseModel):
    index: int
    delta: DeltaMessage
    logprobs: Optional[ChatCompletionLogProbs] = None
    finish_reason: Optional[str] = None


class ChatCompletionStreamResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{random_uuid()}")
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseStreamChoice]
    usage: Optional[UsageInfo] = Field(default=None)


class ExtractedToolCallInformation(BaseModel):
    # indicate if tools were called
    tools_called: bool

    # extracted tool calls
    tool_calls: List[ToolCall]

    # content - per OpenAI spec, content AND tool calls can be returned rarely
    # But some models will do this intentionally
    content: Optional[str] = None


class Model(OpenAIModel):
    artifact_id: str
    max_prompt_len: int
    max_context_len: int

    # TODO: Add runtime-related configuration data.
    @classmethod
    def from_llm(cls, llm: LLM) -> "Model":
        assert llm.max_seq_len_to_capture is not None
        return cls(
            id=llm.model_metadata.pretrained_id,
            created=int(time.time()),
            object="model",
            owned_by="furiosa-ai",
            artifact_id=llm.artifact_id,
            max_prompt_len=llm.prompt_max_seq_len,
            max_context_len=llm.max_seq_len_to_capture,
        )


class ModelsResponse(OpenAIBaseModel):
    object: Literal["list"] = "list"
    data: List[Model]

    @classmethod
    def from_llm(cls, llm: LLM) -> "ModelsResponse":
        return cls(data=[Model.from_llm(llm)])


class ErrorResponse(OpenAIBaseModel):
    object: str = "error"
    message: str
    type: str
    param: Optional[str] = None
    code: int
