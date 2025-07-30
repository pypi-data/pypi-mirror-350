# codegen: sdk
from typing import Optional

from pydantic import BaseModel

from maitai.models.chat import (
    ChatCompletionChunk,
    ChatCompletionResponse,
    EvaluateResponse,
)


class InferenceStreamResponse(BaseModel):
    chat_completion_chunk: Optional[ChatCompletionChunk] = None
    chat_completion_response: Optional[ChatCompletionResponse] = None
    evaluate_response: Optional[EvaluateResponse] = None
    error: Optional[str] = None
    warning: Optional[str] = None
    keep_alive: bool = False
