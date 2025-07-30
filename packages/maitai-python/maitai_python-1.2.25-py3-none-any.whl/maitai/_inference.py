import asyncio
import inspect
import json
import traceback
from typing import AsyncIterable, Iterable, Optional

import httpx

from maitai._config import config
from maitai._maitai_client import MaitaiClient
from maitai._types import AsyncChunkQueue, ChunkQueue, EvaluateCallback, QueueIterable
from maitai._utils import __version__ as version
from maitai._utils import chat_completion_chunk_to_response
from maitai.exceptions import BadRequestError, MaitaiConnectionError, NotFoundError
from maitai.models.chat import ChatCompletionChunk, ChatCompletionResponse
from maitai.models.inference import InferenceStreamResponse
from maitai.models.metric import RequestTimingMetric


class Inference(MaitaiClient):

    def __init__(self):
        super().__init__()

    def infer(
        self, request_dict: dict, evaluate_callback, timeout
    ) -> Iterable[InferenceStreamResponse]:
        if evaluate_callback:
            q = ChunkQueue()
            self.executor.submit(
                self.send_inference_request_with_callback,
                request_dict,
                timeout,
                q,
                evaluate_callback,
            )
            return QueueIterable(q, timeout=timeout)
        else:
            return self.send_inference_request(request_dict, timeout)

    async def infer_async(
        self, request_dict: dict, evaluate_callback, timeout
    ) -> AsyncIterable[InferenceStreamResponse]:
        if evaluate_callback:
            q = AsyncChunkQueue()
            asyncio.create_task(
                self.send_inference_request_with_callback_async(
                    request_dict,
                    timeout,
                    q,
                    evaluate_callback,
                )
            )
            return QueueIterable(q)
        else:
            return self.send_inference_request_async(request_dict, timeout)

    def send_inference_request_with_callback(
        self,
        request_dict: dict,
        timeout,
        chunk_queue: ChunkQueue,
        evaluation_callback: EvaluateCallback,
    ):
        try:
            for chunk in self.send_inference_request(request_dict, timeout):
                chunk_queue.put(chunk)
                if chunk.evaluate_response and evaluation_callback:
                    try:
                        evaluation_callback(chunk.evaluate_response)
                    except:
                        traceback.print_exc()
        except Exception as e:
            chunk_queue.put(e)

    def send_inference_request(
        self,
        request_dict: dict,
        timeout,
    ) -> Iterable[InferenceStreamResponse]:
        host = config.maitai_host
        url = f"{host}/chat/completions/serialized"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }

        client = self.get_client()

        try:
            with client.stream(
                "POST",
                url,
                headers=headers,
                content=json.dumps(request_dict),
                timeout=timeout,
            ) as response:
                for line in response.iter_lines():
                    if line:
                        build_exception(response, line)
                        inference_response: InferenceStreamResponse = (
                            InferenceStreamResponse.model_validate_json(line)
                        )
                        if inference_response.keep_alive:
                            continue
                        yield inference_response

        except TimeoutError as e:
            raise
        except BadRequestError as e:
            raise
        except NotFoundError as e:
            raise
        except MaitaiConnectionError as e:
            raise
        except Exception as e:
            exception = MaitaiConnectionError(
                f"Failed to send inference request. Error: {e}"
            )
            self.log_error(config.api_key, traceback.format_exc(), url)
            raise exception from None

    async def send_inference_request_with_callback_async(
        self,
        request_dict: dict,
        timeout,
        async_chunk_queue: AsyncChunkQueue,
        evaluation_callback: EvaluateCallback,
    ):
        try:
            async for chunk in self.send_inference_request_async(request_dict, timeout):
                await async_chunk_queue.put(chunk)
                if chunk.evaluate_response and evaluation_callback:
                    try:
                        if inspect.iscoroutinefunction(evaluation_callback):
                            asyncio.create_task(
                                evaluation_callback(chunk.evaluate_response)
                            )
                        else:
                            evaluation_callback(chunk.evaluate_response)
                    except:
                        traceback.print_exc()
        except Exception as e:
            await async_chunk_queue.put(e)

    async def send_inference_request_async(
        self,
        request_dict: dict,
        timeout,
    ):
        host = config.maitai_host
        url = f"{host}/chat/completions/serialized"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }

        try:
            client = await self.get_async_client()
            # Using a context manager here but properly handling exit even on exceptions
            async with client.stream(
                "POST", url, headers=headers, json=request_dict, timeout=timeout
            ) as response:
                try:
                    async for line in response.aiter_lines():
                        if line:
                            build_exception(response, line)
                            inference_response: InferenceStreamResponse = (
                                InferenceStreamResponse.model_validate_json(line)
                            )
                            if inference_response.keep_alive:
                                continue
                            yield inference_response
                except Exception as e:
                    # Let the context manager properly close the stream before re-raising
                    raise e
        except TimeoutError as e:
            raise
        except BadRequestError as e:
            raise
        except NotFoundError as e:
            raise
        except MaitaiConnectionError as e:
            raise
        except Exception as e:
            exception = MaitaiConnectionError(
                f"Failed to send inference request: {str(e)}"
            )
            await self.log_error_async(config.api_key, traceback.format_exc(), url)
            raise exception from None

    def store_chat_response(
        self,
        session_id,
        reference_id,
        intent,
        application_ref_name,
        completion_params: dict,
        chat_completion_response: Optional[ChatCompletionResponse],
        final_chunk: Optional[ChatCompletionChunk],
        content: str,
        timing: RequestTimingMetric,
        metadata: dict,
    ):
        inference_request = {
            "application_ref_name": application_ref_name,
            "session_id": session_id,
            "reference_id": reference_id,
            "action_type": intent,
            "apply_corrections": False,
            "evaluation_enabled": False,
            "params": completion_params,
            "auth_keys": config.auth_keys.model_dump(),
            "metadata": metadata,
        }

        if final_chunk:
            chat_completion_response = chat_completion_chunk_to_response(
                final_chunk, content
            )

        chat_storage_request = {
            "chat_completion_request": inference_request,
            "chat_completion_response": (
                chat_completion_response.model_dump()
                if chat_completion_response
                else None
            ),
            "timing_metrics": timing.model_dump(),
        }

        self.executor.submit(self.send_storage_request, chat_storage_request)

    async def store_chat_response_async(
        self,
        session_id,
        reference_id,
        intent,
        application_ref_name,
        completion_params: dict,
        chat_completion_response: Optional[ChatCompletionResponse],
        final_chunk: Optional[ChatCompletionChunk],
        content: str,
        timing: RequestTimingMetric,
        metadata: dict,
    ):
        inference_request = {
            "application_ref_name": application_ref_name,
            "session_id": session_id,
            "reference_id": reference_id,
            "action_type": intent,
            "apply_corrections": False,
            "evaluation_enabled": False,
            "params": completion_params,
            "auth_keys": config.auth_keys.model_dump(),
            "metadata": metadata,
        }

        if final_chunk:
            chat_completion_response = chat_completion_chunk_to_response(
                final_chunk, content
            )

        chat_storage_request = {
            "chat_completion_request": inference_request,
            "chat_completion_response": (
                chat_completion_response.model_dump()
                if chat_completion_response
                else None
            ),
            "timing_metrics": timing.model_dump(),
        }

        asyncio.create_task(self.send_storage_request_async(chat_storage_request))

    def send_storage_request(self, storage_request: dict):
        host = config.maitai_host
        url = f"{host}/chat/completions/response"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }
        try:
            client = self.get_client()
            return client.put(url, headers=headers, json=storage_request)
        except:
            self.log_error(config.api_key, traceback.format_exc(), url)

    async def send_storage_request_async(self, storage_request: dict):
        host = config.maitai_host
        url = f"{host}/chat/completions/response"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }
        try:
            client = await self.get_async_client()
            return await client.put(
                url,
                headers=headers,
                json=storage_request,
            )
        except Exception as e:
            await self.log_error_async(config.api_key, traceback.format_exc(), url)

    def store_request_timing_data(self, metric: RequestTimingMetric):
        self.executor.submit(self._store_request_timing_data, metric)

    def _store_request_timing_data(self, metric: RequestTimingMetric):
        host = config.maitai_host
        if "/batch" in host:
            host = host.replace("/batch", "")
        url = f"{host}/metrics/timing"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }
        try:
            client = self.get_client()
            return client.put(
                url, headers=headers, timeout=10, json=metric.model_dump()
            )
        except:
            pass

    async def send_request_timing_data_async(self, metric: RequestTimingMetric):
        host = config.maitai_host
        if "/batch" in host:
            host = host.replace("/batch", "")
        url = f"{host}/metrics/timing"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "User-Agent": version,
        }
        try:
            client = await self.get_async_client()
            return await client.put(
                url, headers=headers, timeout=10, json=metric.model_dump()
            )
        except:
            pass


def build_exception(response: httpx.Response, line: str):
    if response.status_code >= 400 and response.status_code < 500:
        if response.status_code == 400:
            raise BadRequestError(
                f"Error code: {response.status_code} - {line}"
            ) from None
        elif response.status_code == 404:
            raise NotFoundError(
                f"Error code: {response.status_code} - {line}"
            ) from None
        else:
            raise MaitaiConnectionError(
                f"Error code: {response.status_code} - {line}"
            ) from None
    elif response.status_code >= 500:
        raise MaitaiConnectionError(
            f"Error code: {response.status_code} - {line}"
        ) from None
