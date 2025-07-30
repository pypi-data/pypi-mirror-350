import asyncio
import json
import logging
import queue
from typing import Any, Callable, Mapping, Optional, Protocol, TypedDict, Union

import openai.types.chat as openai_chat_types
from pydantic import BaseModel
from typing_extensions import Literal, runtime_checkable

import maitai.models.chat as chat_types
from maitai.models.chat import *
from maitai.models.chat import ChatCompletionResponse, Tool

logger = logging.getLogger("maitai")

try:
    from typing import override
except ImportError:
    from typing_extensions import override


class Omit:
    def __bool__(self) -> Literal[False]:
        return False


Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object


class MaitaiChunk(ChatCompletionChunk):

    def openai_dump_json(self):
        for choice in self.choices:
            if choice.delta and not choice.delta.role:
                choice.delta.role = "assistant"
        data = self.model_dump()
        return openai_chat_types.ChatCompletionChunk.model_validate(
            data
        ).model_dump_json()


class MaitaiCompletion(ChatCompletionResponse):

    def set_response_format(
        self,
        response_format: Optional[BaseModel] = None,
    ):
        for choice in self.choices:
            choice.message = MaitaiMessage.model_validate(choice.message.model_dump())
            choice.message.response_format = response_format

    def openai_dump_json(self):
        data = self.model_dump()
        return openai_chat_types.ChatCompletion.model_validate(data).model_dump_json()


class MaitaiMessage(ChatCompletionMessage):
    response_format: Optional[BaseModel] = None

    @property
    def parsed(self) -> Any:
        content = json.loads(self.content)
        if self.response_format:
            return self.response_format.model_validate(content)
        return content


@runtime_checkable
class ToolFunction(Protocol):
    __name__: str
    __doc__: str
    __tool__: Tool

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


ChunkQueue = queue.Queue[
    Union[chat_types.ChatCompletionChunk, StopIteration, Exception]
]
AsyncChunkQueue = asyncio.Queue[
    Union[chat_types.ChatCompletionChunk, StopIteration, Exception]
]


class QueueIterable:
    def __init__(
        self, chunk_queue: Union[ChunkQueue, AsyncChunkQueue], timeout=None
    ) -> None:
        self.queue = chunk_queue
        self.done = False
        self.timeout = timeout
        # Keep track of whether we're in async or sync mode
        self._async_mode = None

    def __aiter__(self):
        """Returns the asynchronous iterator object itself."""
        # Set mode to async to prevent mixing with sync iteration
        if self._async_mode is None:
            self._async_mode = True
        elif self._async_mode is False:
            # Reset state if switching from sync to async
            self.done = False
            self._async_mode = True
        return self

    def __iter__(self):
        """Returns the iterator object itself."""
        # Set mode to sync to prevent mixing with async iteration
        if self._async_mode is None:
            self._async_mode = False
        elif self._async_mode is True:
            # Reset state if switching from async to sync
            self.done = False
            self._async_mode = False
        return self

    def __next__(self) -> chat_types.ChatCompletionChunk:
        if self.done:
            raise StopIteration

        while not self.done:
            try:
                # Wait for an item from the queue, block if necessary
                item = self.queue.get(timeout=self.timeout)
                if item is None or isinstance(item, StopIteration):
                    self.done = True  # Set done to True to prevent further blocking
                    raise StopIteration
                elif isinstance(item, Exception):
                    raise item
                return item
            except queue.Empty:
                logger.warning("Maitai issue, queue timed out")
                self.done = True
                raise TimeoutError
        raise StopIteration

    async def __anext__(self) -> chat_types.ChatCompletionChunk:
        if self.done:
            raise StopAsyncIteration

        try:
            # Wait for an item from the queue with a timeout if specified
            if self.timeout:
                item = await asyncio.wait_for(self.queue.get(), timeout=self.timeout)
            else:
                item = await self.queue.get()

            if item is None or isinstance(item, StopIteration):
                self.done = True  # Set done to True to prevent further blocking
                raise StopAsyncIteration
            elif isinstance(item, Exception):
                raise item
            return item

        except asyncio.TimeoutError:
            logger.warning("Maitai issue, queue timed out")
            self.done = True
            raise StopAsyncIteration


EvaluateCallback = Callable[[EvaluateResponse], None]


class FallbackConfig(TypedDict):
    model: Optional[str]
    strategy: Literal["reactive", "first_response", "timeout"]
    timeout: Optional[float]


# Sentinel class used until PEP 0661 is accepted
class NotGiven:
    """
    A sentinel singleton class used to distinguish omitted keyword arguments
    from those passed in with the value None (which may have different behavior).

    For example:

    ```py
    def get(timeout: Union[int, NotGiven, None] = NotGiven()) -> Response: ...


    get(timeout=1)  # 1s timeout
    get(timeout=None)  # No timeout
    get()  # Default timeout behavior, which may not be statically known at the method definition.
    ```
    """

    def __bool__(self) -> Literal[False]:
        return False

    @override
    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()
