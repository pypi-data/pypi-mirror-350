import inspect
import json
import re
from typing import get_type_hints

from maitai.models.chat import Function, FunctionParameters, Property, Tool, ToolCall


class Tools:
    def __init__(self, *tools):
        self.available_functions = {}
        self.definitions = []
        for func in tools:
            if not hasattr(func, "__tool__"):
                raise TypeError(f"Method passed into tools missing @tool decorator")
            tool_call = func.__tool__
            self.available_functions[tool_call.function.name] = func
            self.definitions.append(tool_call)

    def get_tool_definitions(self):
        return self.definitions

    def invoke(self, tool_call: ToolCall, **override_args):
        if tool_call.function.name not in self.available_functions:
            raise TypeError(f"Function {tool_call.function.name} is not defined")
        function_to_call = self.available_functions[tool_call.function.name]
        try:
            function_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            function_args = {}
        function_args.update(override_args)
        function_response = function_to_call(**function_args)
        return function_response


def tool(func=None, strict=False):
    if func is None:
        return lambda f: tool(f, strict=strict)

    function_description = func.__doc__
    if not function_description:
        raise ValueError("Missing docstring for tool")
    function_description = (
        function_description.split(":param")[0].split("Args:")[0].strip()
    )

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    sig = inspect.signature(func)
    params = sig.parameters

    properties = {}
    required = []
    type_hints = get_type_hints(func)

    param_descriptions = _extract_param_details(func.__doc__)
    for param_name, param in params.items():
        if param_name in ["self", "cls"]:
            continue
        if param_name in type_hints:
            param_type = type_hints[param_name].__name__
        elif param.default is not param.empty and param.default is not None:
            param_type = type(param.default).__name__
        else:
            param_type = "string"
        properties[param_name] = Property(
            type=_parse_type(param_type),
            description=param_descriptions.get(param_name, ""),
        )
        required.append(param_name)

    wrapper.__tool__ = Tool(
        type="function",
        function=Function(
            name=func.__name__,
            strict=strict,
            description=function_description,
            parameters=FunctionParameters(
                type="object",
                properties=properties,
                required=required,
            ),
        ),
    )
    return wrapper


def _extract_param_details(docstring):
    param_descriptions = {}
    param_pattern = re.compile(r":param (\w+): (.+)")
    args_pattern = re.compile(r"Args:\s*(.*?)(?=\n\S|$)", re.DOTALL)
    arg_param_pattern = re.compile(r"(\w+): (.+)")

    args_match = args_pattern.search(docstring)
    if args_match:
        args_section = args_match.group(1)
        arg_lines = args_section.split("\n")
        for line in arg_lines:
            if line.strip():
                param_match = arg_param_pattern.match(line.strip())
                if param_match:
                    param_name, param_description = param_match.groups()
                    param_descriptions[param_name] = param_description.strip()
    param_matches = param_pattern.findall(docstring)
    for param, description in param_matches:
        param_descriptions[param] = description.strip()
    return param_descriptions


def _parse_type(type_string):
    if type_string == "str" or type_string == "string":
        return "string"
    if type_string == "int" or type_string == "integer":
        return "integer"
    if type_string == "bool" or type_string == "boolean":
        return "boolean"
    if type_string == "float" or type_string == "number":
        return "number"
    return "string"
