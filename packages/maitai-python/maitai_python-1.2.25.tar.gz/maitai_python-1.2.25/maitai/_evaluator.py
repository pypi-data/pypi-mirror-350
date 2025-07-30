import asyncio
import logging
import traceback
from typing import Iterable, Optional

from maitai._config import config
from maitai._maitai_client import MaitaiClient
from maitai._types import EvaluateCallback
from maitai._utils import __version__ as version
from maitai._utils import chat_completion_chunk_to_response
from maitai.models.chat import (
    ChatCompletionChunk,
    ChatCompletionParams,
    ChatCompletionResponse,
    EvaluateRequest,
    EvaluateResponse,
    EvaluationContentType,
)
from maitai.models.metric import RequestTimingMetric

logger = logging.getLogger("maitai")


def _get_content_type(content, partial=None):
    if partial is not None:
        return EvaluationContentType.PARTIAL
    if isinstance(content, str):
        return EvaluationContentType.TEXT
    elif isinstance(content, list):
        return EvaluationContentType.MESSAGE


class Evaluator(MaitaiClient):

    def __init__(self):
        super().__init__()

    async def evaluate_async(
        self,
        session_id,
        reference_id,
        intent,
        content,
        content_type=None,
        application_id=None,
        application_ref_name=None,
        callback=None,
        completion_params: dict = None,
        chat_completion_response: ChatCompletionResponse = None,
        chat_completion_chunk: ChatCompletionChunk = None,
        timing: RequestTimingMetric = None,
        metadata: dict = {},
    ):
        if content_type is None:
            content_type = _get_content_type(content)
        if content_type is None:
            raise Exception("Unable to automatically determine content_type")
        if application_id is None and application_ref_name is None:
            raise Exception("application_id or application_ref_name must be provided")
        eval_request = self.create_eval_request(
            application_id,
            application_ref_name,
            session_id,
            reference_id,
            intent,
            content_type,
            content,
        )
        if completion_params is not None:
            eval_request["chat_completion_request"] = {
                "application_ref_name": application_ref_name,
                "session_id": session_id,
                "reference_id": reference_id,
                "action_type": intent,
                "apply_corrections": False,
                "evaluation_enabled": True,
                "params": completion_params,
                "return_evaluation": True if callback else False,
                "auth_keys": config.auth_keys.model_dump(),
                "metadata": metadata,
            }
            if chat_completion_chunk is not None:
                chat_completion_response = chat_completion_chunk_to_response(
                    chat_completion_chunk, content
                )
            eval_request["chat_completion_response"] = (
                chat_completion_response.model_dump()
                if chat_completion_response
                else None
            )
        eval_request["timing_metrics"] = timing.model_dump() if timing else None
        if callback is not None:
            asyncio.create_task(
                self.send_evaluation_request_async(eval_request, callback)
            )
        else:
            return self.send_evaluation_request(eval_request)

    def evaluate(
        self,
        session_id,
        reference_id,
        intent,
        content,
        content_type=None,
        application_id=None,
        application_ref_name=None,
        callback=None,
        partial=None,
        completion_params: ChatCompletionParams = None,
        chat_completion_response: ChatCompletionResponse = None,
        chat_completion_chunk: ChatCompletionChunk = None,
        timing: RequestTimingMetric = None,
        metadata: dict = {},
    ):
        if content_type is None:
            content_type = _get_content_type(content, partial)
        if content_type is None:
            raise Exception("Unable to automatically determine content_type")
        if application_id is None and application_ref_name is None:
            raise Exception("application_id or application_ref_name must be provided")
        eval_request: EvaluateRequest = self.create_eval_request(
            application_id,
            application_ref_name,
            session_id,
            reference_id,
            intent,
            content_type,
            content,
            partial=partial,
        )
        if completion_params is not None:
            eval_request["chat_completion_request"] = {
                "application_ref_name": application_ref_name,
                "session_id": session_id,
                "reference_id": reference_id,
                "action_type": intent,
                "apply_corrections": False,
                "evaluation_enabled": True,
                "params": completion_params,
                "return_evaluation": True if callback else False,
                "auth_keys": config.auth_keys.model_dump(),
                "metadata": metadata,
            }
            if chat_completion_chunk is not None:
                chat_completion_response = chat_completion_chunk_to_response(
                    chat_completion_chunk, content
                )
            eval_request["chat_completion_response"] = (
                chat_completion_response.model_dump()
            )
        eval_request["timing_metrics"] = timing.model_dump() if timing else None
        if callback is not None:
            self.executor.submit(self.send_evaluation_request, eval_request, callback)
        else:
            return self.send_evaluation_request(eval_request)

    def stream_correction(
        self,
        session_id,
        reference_id,
        intent,
        content_type,
        content,
        application_ref_name,
        partial,
        fault_description,
        sentinel_id,
    ):
        eval_request: EvaluateRequest = self.create_eval_request(
            None,
            application_ref_name,
            session_id,
            reference_id,
            intent,
            content_type,
            content,
            partial=partial,
            fault_description=fault_description,
        )
        eval_request["sentinel_id"] = sentinel_id
        return self.send_stream_correction_request(eval_request)

    def create_eval_request(
        self,
        application_id,
        application_ref_name,
        session_id,
        reference_id,
        intent,
        content_type,
        content,
        partial=None,
        fault_description=None,
        chat_completion_response=None,
    ):
        eval_request = {
            "evaluation_content_type": content_type.value,
            "application_id": application_id,
            "application_ref_name": application_ref_name,
            "session_id": session_id,
            "reference_id": reference_id,
            "action_type": intent,
        }
        if content_type == EvaluationContentType.TEXT:
            if not isinstance(content, str):
                raise Exception("Content must be a string")
            eval_request["text_content"] = content
        elif content_type == EvaluationContentType.MESSAGE:
            eval_request["message_content"] = content
        elif content_type == EvaluationContentType.PARTIAL:
            eval_request["message_content"] = content
            eval_request["text_content"] = partial

        if fault_description:
            eval_request["fault_description"] = fault_description

        return eval_request

    def send_evaluation_request(
        self, eval_request: dict, callback: Optional[EvaluateCallback] = None
    ):
        path = "request" if callback else "submit"
        host = config.maitai_host
        url = f"{host}/evaluation/{path}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }
        try:
            client = self.get_client()
            response = client.post(url, headers=headers, json=eval_request)
            if response.status_code != 200:
                error_text = response.text
                self.log_error(config.api_key, error_text, url)
            result = response.content
        except Exception as e:
            self.log_error(config.api_key, traceback.format_exc(), url)
            return None
        if result is not None:
            eval_result = EvaluateResponse.model_validate_json(result)
            if callback is not None:
                try:
                    callback(eval_result)
                except:
                    traceback.print_exc()
            else:
                return eval_result

    async def send_evaluation_request_async(
        self, eval_request: dict, callback: Optional[EvaluateCallback] = None
    ):
        path = "request" if callback else "submit"
        host = config.maitai_host
        url = f"{host}/evaluation/{path}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }

        try:
            client = await self.get_async_client()
            response = await client.post(url, headers=headers, json=eval_request)
            if response.status_code != 200:
                error_text = response.text
                await self.log_error_async(config.api_key, error_text, url)
                return None
            result = response.content
        except Exception as e:
            await self.log_error_async(config.api_key, traceback.format_exc(), url)
            return None

        if result is not None:
            eval_result = EvaluateResponse.model_validate_json(result)
            if callback is not None:
                try:
                    callback(eval_result)
                except:
                    traceback.print_exc()
            else:
                return eval_result

    def send_stream_correction_request(
        self, eval_request: dict
    ) -> Iterable[ChatCompletionChunk]:
        def consume_stream():
            host = config.maitai_host
            url = f"{host}/evaluation/stream_correction"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": config.api_key,
                "User-Agent": version,
            }

            client = self.get_client()
            with client.stream(
                "POST", url, headers=headers, json=eval_request
            ) as response:
                if response.status_code != 200:
                    logger.error(
                        f"Failed to send stream correction request. Status code: {response.status_code}. Error: {response.text}"
                    )
                    self.log_error(config.api_key, response.text, url)
                    return
                try:
                    for line in response.iter_lines():
                        if line:
                            yield line
                finally:
                    pass  # No need to close response as context manager handles it

        for resp in consume_stream():
            inference_response: ChatCompletionChunk = (
                ChatCompletionChunk.model_validate_json(resp)
            )
            yield inference_response
