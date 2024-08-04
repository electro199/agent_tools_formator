import inspect
import json
from typing import Any, Callable, get_type_hints

import chromadb
from chromadb.config import Settings

__all__ = [
    "tools",
    "tool_func",
    "get_relevant_tools",
]

tools: dict[str, Callable] = dict()
_chroma_client = None


def _get_type_name(t) -> str:
    name = str(t)
    if "list" in name or "dict" in name:
        return name
    else:
        return t.__name__


def _get_required_parameters(func):
    """
    Returns a list of required parameters for a given function.

    Parameters:
    func (function): The function to inspect.

    Returns:
    list: A list of names of required parameters.
    """
    sig: inspect.Signature = inspect.signature(func)
    required_params = []

    for name, param in sig.parameters.items():
        if param.default is inspect.Parameter.empty:
            required_params.append(name)

    return required_params


def _function_to_json(func: Callable):
    type_hints: dict[str, Any] = get_type_hints(func)
    try:
        function_info = {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__.replace("\n", " ")
                .replace("  ", " ")
                .replace("   ", " ")
                .strip(),
                "parameters": {"type": "object", "properties": {}},
                "returns": type_hints.get("return", "void").__name__,
                "required": _get_required_parameters(func),
            },
        }
    except AttributeError as e:
        print("Error converting function metadata to json in", func.__name__, e)
        raise e

    for name, _ in inspect.signature(func).parameters.items():
        param_type = _get_type_name(type_hints.get(name, type(None)))
        function_info["function"]["parameters"]["properties"][name] = {
            "type": param_type,
            "description": "",
        }

    return json.dumps(function_info)


def tool_func(func: Callable):  # -> Callable[..., Any]:
    """
    parse and save function metadata in db to later be retrived by get_relevant_tools

    """
    tools.update(
        {
            func.__name__: func,
        }
    )
    data = _function_to_json(func)
    _add_tools_db(func, data)

    return func


def convert_functions_to_json(*tool_func) -> list[str]:
    return [_function_to_json(tool_data) for tool_data in tool_func]


def _get_or_mk_db() -> chromadb.ClientAPI:
    global _chroma_client
    if not _chroma_client:
        return (_chroma_client := chromadb.Client(Settings(anonymized_telemetry=False)))

    return _chroma_client


def _add_tools_db(func: Callable, data: str) -> None:
    _get_or_mk_db().get_or_create_collection(name="tools").add(
        func.__name__, documents=data
    )


def get_relevant_tools(prompt, n_results=2, *args, **kwargs) -> list:
    """

    Retrive relevant tools relative to prompt 

    """
    return [
        json.loads(tool)
        for tool in _get_or_mk_db()
        .get_or_create_collection(name="tools")
        .query(query_texts=[prompt], n_results=n_results, *args, **kwargs)["documents"][
            0
        ]
    ]


def call_tool(tool_call: dict) -> str:
    """
    Takes a function call dictionary from llm reponse run the function and return the tool returned object as string
    """
    function_to_call = tools.get(tool_call["function"]["name"])
    if function_to_call is None:
        raise NotImplemented(
            "Tool " + tool_call["function"]["name"] + " not found in registered tool"
        )
    return str(
        function_to_call(
            **tool_call["function"]["arguments"],
        )
    )

def call_tools(tool_calls:list[dict]) -> list[str]:
    return [call_tool(call) for call in tool_calls]