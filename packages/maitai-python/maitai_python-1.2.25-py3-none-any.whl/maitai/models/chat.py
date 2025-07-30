# codegen: frontend, sdk
import time
import uuid
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal

from maitai.models import application as application_types
from maitai.models import config, key, metric, sentinel


class EvaluationProvider(Enum):
    GROQ = 0
    OPENAI = 1
    CEREBRAS = 2
    MAITAI = 3
    SAMBANOVA = 4
    GEMINI = 5
    DEEPSEEK = 6
    ANTHROPIC = 7


class AzureParams(BaseModel):
    endpoint: Optional[str] = None
    deployment: Optional[str] = None
    api_version: Optional[str] = None


class ClientParams(BaseModel):
    base_url: Optional[str] = None
    default_headers: Optional[Dict[str, str]] = None
    default_query: Optional[Dict[str, str]] = None
    azure_params: Optional[AzureParams] = None


class ChatCompletionAuth(BaseModel):
    openai_api_key: Optional[str] = ""
    groq_api_key: Optional[str] = ""
    override_api_key: Optional[str] = ""
    anthropic_api_key: Optional[str] = ""
    cerebras_api_key: Optional[str] = ""
    azure_api_key: Optional[str] = ""
    sambanova_api_key: Optional[str] = ""
    gemini_api_key: Optional[str] = ""
    deepseek_api_key: Optional[str] = ""


class Property(BaseModel):
    type: Union[str, List[str]] = ""
    description: Optional[str] = None
    items: Optional["FunctionParameters"] = None
    anyOf: Optional[List["Property"]] = None
    enum: List[str] = Field(default_factory=list)

    def model_dump(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().model_dump_json(**kwargs)


class FunctionParameters(BaseModel):
    type: Optional[str] = ""
    description: Optional[str] = ""
    properties: Optional[Dict[str, Property]] = {}
    required: List[str] = Field(default_factory=list)
    additionalProperties: Optional[bool] = False
    enum: List[str] = Field(default_factory=list)


class Function(BaseModel):
    name: str
    description: Optional[str] = ""
    parameters: Optional[FunctionParameters] = None
    strict: Optional[bool] = False


class Tool(BaseModel):
    type: str
    function: Function


class JSONSchema(BaseModel):
    name: str = "output_schema"
    strict: Optional[bool] = False
    json_schema: FunctionParameters = Field(alias="schema")


class ResponseFormat(BaseModel):
    type: str
    json_schema: Optional[JSONSchema] = None


class StreamOptions(BaseModel):
    include_usage: bool = False


class ToolCallFunction(BaseModel):
    name: Optional[str] = None
    arguments: str = ""


class ToolCall(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    function: Optional[ToolCallFunction] = None
    index: Optional[int] = None


class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = ""
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


class ToolChoice(BaseModel):
    type: str
    function: Optional[Function] = None


class ChatCompletionParams(BaseModel):
    messages: List[ChatMessage]
    model: str
    max_tokens: Optional[int] = None
    response_format: Optional[ResponseFormat] = ResponseFormat(type="text")
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    logprobs: Optional[bool] = False
    top_logprobs: Optional[int] = None
    n: Optional[int] = 1
    seed: Optional[int] = None
    stream: Optional[bool] = False
    stream_options: Optional[StreamOptions] = None
    logit_bias: Optional[Dict[str, float]] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    user: Optional[str] = None
    tools: Optional[List[Tool]] = []
    tool_choice: Optional[Union[ToolChoice, str]] = None
    parallel_tool_calls: Optional[bool] = False
    extra_headers: Optional[Dict[str, str]] = None
    reasoning_effort: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    params: ChatCompletionParams = None
    application_ref_name: str = None
    session_id: str = None
    action_type: str = None

    application_id: Optional[int] = None
    reference_id: Optional[Union[str, int]] = None
    application_action_id: Optional[int] = None
    company_id: Optional[int] = None
    apply_corrections: Optional[bool] = False
    id: Optional[int] = None
    date_created: Optional[float] = None
    request_id: Optional[str] = None
    evaluation_enabled: Optional[bool] = True
    auth_info: Optional[ChatCompletionAuth] = ChatCompletionAuth()
    return_evaluation: Optional[bool] = False
    error: Optional[str] = None
    auth_keys: Optional[key.KeyMap] = key.KeyMap()
    inference_location: Optional[str] = "SERVER"
    context_retrieval_enabled: Optional[bool] = False
    context_query: Optional[str] = None
    context: Optional[str] = None
    return_request: Optional[bool] = Field(default=False)
    fallback_model: Optional[str] = None
    user_id: Optional[str] = None
    assistant: Optional[bool] = False
    client_params: Optional[ClientParams] = None
    metadata: Optional[Dict[str, Any]] = None
    safe_mode: Optional[bool] = Field(default=False)
    preserve_model_alias: Optional[bool] = False
    fallback_config: Optional[config.FallbackConfig] = None
    request_type: Literal["PROD", "RERUN", "SYNTHETIC"] = "PROD"


class FunctionCall(BaseModel):
    arguments: Optional[str] = ""
    name: Optional[str] = None


class ChatCompletionMessage(BaseModel):
    role: str
    content: Optional[str] = ""
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[List[ToolCall]] = None
    refusal: Optional[str] = None


class TopLogProbs(BaseModel):
    token: str
    logprob: float
    bytes: List[int] = Field(default_factory=list)


class LogPropsContent(BaseModel):
    token: str
    logprob: float
    bytes: List[int] = Field(default_factory=list)
    top_logprobs: List[TopLogProbs] = Field(default_factory=list)


class LogProbs(BaseModel):
    content: List[LogPropsContent] = Field(default_factory=list)
    refusal: List[LogPropsContent] = Field(default_factory=list)


class ChatCompletionChoice(BaseModel):
    index: Optional[int] = 0
    message: Optional[ChatCompletionMessage] = None
    logprobs: Optional[LogProbs] = None
    finish_reason: Optional[str] = ""
    is_correction: bool = False


class CompletionTokensDetails(BaseModel):
    reasoning_tokens: Optional[int] = 0


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0
    model: str = ""
    completion_tokens_details: Optional[CompletionTokensDetails] = None


class EvaluateResult(BaseModel):
    id: Optional[int] = -1
    status: Optional[str] = None
    description: Optional[str] = None
    confidence: Optional[float] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
    sentinel_id: Optional[int] = None
    eval_time: Optional[float] = 0
    date_created: Optional[float] = 0
    usage: Optional[ChatCompletionUsage] = None
    sentinel_name: Optional[str] = None
    severity: Optional[int] = None
    correction: Optional[str] = None
    sentinel_directive_id: Optional[int] = None
    evaluation_request_id: Optional[str] = None
    request_id: Optional[str] = None
    application_id: Optional[int] = None
    session_id: Optional[str] = None


class EvaluateResponse(BaseModel):
    application_id: Optional[int] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    evaluation_results: List[EvaluateResult] = Field(default_factory=list)
    evaluation_request_id: Optional[str] = None
    evaluate_summary: Optional[str] = None
    evaluation_time: Optional[float] = None
    reference_id: Optional[Union[str, int]] = None
    id: Optional[int] = -1
    date_created: Optional[float] = 0
    correction: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


class ChatCompletionResponse(BaseModel):
    id: Optional[Union[int, str]] = None
    object: str = "chat.completion"
    created: Union[int, float] = Field(default_factory=lambda: int(time.time()))
    model: str = None
    system_fingerprint: Optional[str] = None
    choices: List[ChatCompletionChoice] = Field(default_factory=list)
    usage: Optional[ChatCompletionUsage] = None
    request_id: Optional[str] = None
    evaluate_response: Optional[EvaluateResponse] = None
    correction_applied: bool = False
    first_token_time: float = 0
    response_time: float = 0
    chat_completion_request: Optional[ChatCompletionRequest] = None
    service_tier: Optional[str] = None
    input_safety_score: Optional[float] = 0
    fallback_reason: Optional[str] = None


class ChatStorageRequest(BaseModel):
    chat_completion_request: ChatCompletionRequest
    chat_completion_response: ChatCompletionResponse
    evaluate_request: Optional["EvaluateRequest"] = None
    timing_metrics: Optional[metric.RequestTimingMetric] = None


class Turn(BaseModel):
    application: Optional[application_types.Application] = None
    request: Optional[ChatCompletionRequest] = None
    response: Optional[ChatCompletionResponse] = None
    eval_request: Optional["EvaluateRequest"] = None
    first: bool = False
    last: bool = False


class ChoiceDelta(BaseModel):
    content: Optional[str] = ""
    role: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    function_call: Optional[FunctionCall] = None
    refusal: Optional[str] = None


class ChunkChoice(BaseModel):
    delta: ChoiceDelta
    finish_reason: Optional[str] = None
    index: int = 0
    logprobs: Optional[LogProbs] = None
    is_correction: bool = False


class ChatCompletionChunk(BaseModel):
    id: str = ""
    choices: List[ChunkChoice] = Field(default_factory=list)
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    object: str = ""
    system_fingerprint: Optional[str] = ""
    usage: Optional[ChatCompletionUsage] = None
    evaluate_response: Optional[EvaluateResponse] = None
    correction_applied: bool = False
    service_tier: Optional[str] = None
    input_safety_score: float = 0
    request_id: str = ""
    fallback_reason: Optional[str] = None


class InferenceStreamResponse(BaseModel):
    chat_completion_chunk: Optional[ChatCompletionChunk] = None
    chat_completion_response: Optional[ChatCompletionResponse] = None
    evaluate_response: Optional[EvaluateResponse] = None
    error: Optional[str] = None
    warning: Optional[str] = None
    keep_alive: Optional[bool] = False


class EvaluationContentType(IntEnum):
    MESSAGE = 0
    TEXT = 1
    PARTIAL = 2


class EvaluateRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = None
    date_created: Optional[float] = None
    application_id: Optional[int] = None
    application_ref_name: str = None
    session_id: str = None
    reference_id: Optional[Union[str, int]] = None
    action_type: str = None
    evaluation_content_type: Union[EvaluationContentType, str] = (
        EvaluationContentType.MESSAGE
    )
    eval_results_set: Optional[EvaluateResponse] = None
    company_id: Optional[int] = None
    evaluation_context: Optional[str] = None
    text_content: Optional[str] = None
    message_content: List[Union[ChatMessage, ChatCompletionMessage]] = Field(
        default_factory=list
    )
    request_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    sentinel_id: Optional[int] = None
    fault_description: Optional[str] = None
    chat_completion_request: Optional[ChatCompletionRequest] = None
    chat_completion_response: Optional[ChatCompletionResponse] = None
    timeout: float = 0
    partial: Optional[str] = None
    stream: Optional[bool] = False
    apply_corrections: bool = False
    timing_metrics: Optional[metric.RequestTimingMetric] = None
    tools: List[Tool] = Field(default_factory=list)
    sentinels: List[sentinel.Sentinel] = Field(default_factory=list)
    evaluation_request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    json_schema: Optional[JSONSchema] = None
    evaluation_run_id: Optional[int] = None


class SessionMessage(BaseModel):
    id: Optional[int] = -1
    application_id: int
    company_id: Optional[int] = -1
    application_action_id: int
    session_id: str
    request_id: str
    role: str
    message: ChatMessage
    instructions: str
    date_created: Optional[float] = 0


# This is needed because of the forward reference in Property
FunctionParameters.model_rebuild()

# Add this alongside the other model_rebuild() call
ChatMessage.model_rebuild()  # Because ChatMessage has a forward reference to

ChatStorageRequest.model_rebuild()

Turn.model_rebuild()
