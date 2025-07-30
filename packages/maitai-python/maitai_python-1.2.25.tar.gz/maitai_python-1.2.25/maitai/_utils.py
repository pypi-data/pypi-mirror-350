import functools
import inspect
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

import openai
import openai.types.chat as openai_types
import pydantic
from openai.types import ChatModel

import maitai.models.chat as chat_types
from maitai._pydantic import (
    is_basemodel_type,
    is_dataclass_like_type,
    to_strict_json_schema,
)
from maitai._types import ToolFunction
from maitai.tools import Tools
from maitai_common.version import version

__version__ = f"Maitai/Python{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} {version}"

CallableT = TypeVar("CallableT", bound=Callable[..., Any])


def type_to_response_format_param(response_format):
    json_schema_type: type[pydantic.BaseModel] | pydantic.TypeAdapter[Any] | None = None

    if is_basemodel_type(response_format):
        name = response_format.__name__
        json_schema_type = response_format
    elif is_dataclass_like_type(response_format):
        name = response_format.__name__
        json_schema_type = pydantic.TypeAdapter(response_format)
    else:
        raise TypeError(f"Unsupported response_format type - {response_format}")

    return {
        "schema": to_strict_json_schema(json_schema_type),
        "name": name,
        "strict": True,
    }


def required_args(*variants: Sequence[str]) -> Callable[[CallableT], CallableT]:
    def inner(func: CallableT) -> CallableT:
        params = inspect.signature(func).parameters
        positional = [
            name
            for name, param in params.items()
            if param.kind
            in {
                param.POSITIONAL_ONLY,
                param.POSITIONAL_OR_KEYWORD,
            }
        ]

        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            given_params: set[str] = set()
            for i, _ in enumerate(args):
                try:
                    given_params.add(positional[i])
                except IndexError:
                    raise TypeError(
                        f"{func.__name__}() takes {len(positional)} argument(s) but {len(args)} were given"
                    ) from None

            for key in kwargs.keys():
                given_params.add(key)

            for variant in variants:
                matches = all((param in given_params for param in variant))
                if matches:
                    break
            else:  # no break
                if len(variants) > 1:
                    variations = human_join(
                        [
                            "("
                            + human_join([quote(arg) for arg in variant], final="and")
                            + ")"
                            for variant in variants
                        ]
                    )
                    msg = f"Missing required arguments; Expected either {variations} arguments to be given"
                else:
                    assert len(variants) > 0

                    # TODO: this error message is not deterministic
                    missing = list(set(variants[0]) - given_params)
                    if len(missing) > 1:
                        msg = f"Missing required arguments: {human_join([quote(arg) for arg in missing])}"
                    else:
                        msg = f"Missing required argument: {quote(missing[0])}"
                raise TypeError(msg)
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return inner


# copied from https://github.com/Rapptz/RoboDanny
def human_join(seq: Sequence[str], *, delim: str = ", ", final: str = "or") -> str:
    size = len(seq)
    if size == 0:
        return ""

    if size == 1:
        return seq[0]

    if size == 2:
        return f"{seq[0]} {final} {seq[1]}"

    return delim.join(seq[:-1]) + f" {final} {seq[-1]}"


def quote(string: str) -> str:
    """Add single quotation marks around the given string. Does *not* do any escaping."""
    return f"'{string}'"


def convert_openai_chat_completion(
    chat: openai_types.ChatCompletion,
) -> chat_types.ChatCompletionResponse:
    return chat_types.ChatCompletionResponse.model_validate(chat.model_dump())


def convert_open_ai_chat_completion_chunk(
    chunk: openai_types.ChatCompletionChunk,
) -> chat_types.ChatCompletionChunk:
    return chat_types.ChatCompletionChunk.model_validate(chunk.model_dump())


def get_chat_completion_params(
    *,
    messages: Iterable[openai_types.ChatCompletionMessageParam],
    model: Union[str, ChatModel],
    frequency_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    logit_bias: Union[Optional[Dict[str, int]], openai.NotGiven] = openai.NOT_GIVEN,
    logprobs: Union[Optional[bool], openai.NotGiven] = openai.NOT_GIVEN,
    max_tokens: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    n: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    presence_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    response_format: Union[
        openai_types.completion_create_params.ResponseFormat,
        chat_types.ResponseFormat,
        openai.NotGiven,
    ] = openai.NOT_GIVEN,
    seed: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    stop: Union[Union[Optional[str], List[str]], openai.NotGiven] = openai.NOT_GIVEN,
    stream: Optional[bool] = False,
    stream_options: Union[
        Optional[openai_types.ChatCompletionStreamOptionsParam], openai.NotGiven
    ] = openai.NOT_GIVEN,
    temperature: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    tool_choice: Union[
        openai_types.ChatCompletionToolChoiceOptionParam, openai.NotGiven
    ] = openai.NOT_GIVEN,
    tools: Union[
        Iterable[Union[openai_types.ChatCompletionToolParam, ToolFunction]],
        openai.NotGiven,
    ] = openai.NOT_GIVEN,
    top_logprobs: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    top_p: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    user: Union[str, openai.NotGiven] = openai.NOT_GIVEN,
    parallel_tool_calls: Union[bool, openai.NotGiven] = openai.NOT_GIVEN,
    reasoning_effort: Optional[str] = openai.NOT_GIVEN,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    params = {
        "messages": [msg for msg in messages],
        "model": model,
        "stream": stream,
    }

    if not extra_headers:
        extra_headers = {}

    # Define all optional parameters in a dictionary
    optional_params = {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stop": stop,
        "logprobs": logprobs,
        "top_logprobs": top_logprobs,
        "n": n,
        "seed": seed,
        "logit_bias": logit_bias,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "user": user,
        "tool_choice": tool_choice,
        "parallel_tool_calls": parallel_tool_calls,
        "reasoning_effort": reasoning_effort,
        "extra_headers": extra_headers,
    }

    # Add non-NOT_GIVEN params to the dict
    for param_name, value in optional_params.items():
        if value != openai.NOT_GIVEN:
            params[param_name] = value

    if stream_options != openai.NOT_GIVEN and stream_options:
        params["stream_options"] = {
            "include_usage": stream_options.get("include_usage")
        }

    if response_format != openai.NOT_GIVEN and response_format is not None:
        if hasattr(response_format, "model_json_schema"):
            response_format = {
                "type": "json_schema",
                "json_schema": type_to_response_format_param(response_format),
            }
        params["response_format"] = {"type": response_format["type"]}
        if response_format.get("json_schema"):
            params["response_format"]["json_schema"] = response_format["json_schema"]

    if tools != openai.NOT_GIVEN:
        params["tools"] = []
        if isinstance(tools, Tools):
            params["tools"] = [
                tool.model_dump() for tool in tools.get_tool_definitions()
            ]
        elif tools:
            for tool in tools:
                if hasattr(tool, "__tool__"):
                    params["tools"].append(tool.__tool__.model_dump())
                    continue

                tool_dict = {"type": tool["type"]}
                function = tool.get("function", {})

                properties = {}
                for prop_name, prop_value in (
                    function.get("parameters", {}).get("properties", {}).items()
                ):
                    if isinstance(prop_value, dict):
                        prop_dict = {
                            "type": prop_value.get("type"),
                            "description": prop_value.get("description"),
                        }
                        if prop_value.get("items"):
                            prop_dict["items"] = prop_value["items"]
                        properties[prop_name] = prop_dict
                    else:
                        properties[prop_name] = prop_value

                parameters = {}
                if function.get("parameters"):
                    parameters = {
                        "type": function["parameters"].get("type", ""),
                        "properties": properties,
                        "required": function["parameters"].get("required", []),
                        "additionalProperties": function["parameters"].get(
                            "additionalProperties", False
                        ),
                        "enum": function["parameters"].get("enum", []),
                    }

                tool_dict["function"] = {
                    "name": function.get("name"),
                    "description": function.get("description"),
                    "parameters": parameters,
                    "strict": function.get("strict", False),
                }
                params["tools"].append(tool_dict)

    return params


def chat_completion_chunk_to_response(
    final_chunk: chat_types.ChatCompletionChunk,
    content: Union[str, List[chat_types.ChatMessage]],
):
    chat_completion_response = chat_types.ChatCompletionResponse.model_validate(
        final_chunk.model_dump()
    )
    if isinstance(content, str):
        chat_completion_response.choices[0].message = chat_types.ChatMessage(
            role="assistant", content=content
        )
    if isinstance(content, List):
        chat_completion_response.choices[0].message = content[-1]
    if isinstance(chat_completion_response.choices[0].message, dict):
        chat_completion_response.choices[0].message = (
            chat_types.ChatMessage.model_validate(
                chat_completion_response.choices[0].message
            )
        )
    return chat_completion_response


def convert_params_to_groq(params: Dict[str, Any]) -> Dict[str, Any]:
    if "reasoning_effort" in params:
        del params["reasoning_effort"]
    if "stream_options" in params:
        del params["stream_options"]
    if params.get("max_tokens", openai.NOT_GIVEN) == openai.NOT_GIVEN or params.get("max_tokens", 0) <= 0:
        ## max_tokens must be positive
        params["max_tokens"] = 1000
    to_del = []
    for key, item in params.items():
        if item == openai.NOT_GIVEN:
            to_del.append(key)
    for key in to_del:
        del params[key]
    return params
