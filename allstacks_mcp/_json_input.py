"""Shared JSON-input handling for MCP tool parameters.

MCP clients (Claude Desktop and others) often pre-parse JSON-shaped strings into
dicts or lists before FastMCP validates tool arguments. Plain ``str`` annotations
then fail validation and the call never reaches the handler.

Use ``JsonObjectInput``, ``JsonArrayInput``, or ``JsonValueInput`` on tool
parameters instead of ``str``. They accept already-parsed JSON from the client
and still coerce a JSON string when one arrives intact.
"""

import json
from typing import Annotated, Any, Dict, List, Union

from pydantic import BeforeValidator


def _parse_json_string(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string: {e}") from e


def _coerce_json_value(value: Any) -> Union[Dict[str, Any], List[Any]]:
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        parsed = _parse_json_string(value)
        if not isinstance(parsed, (dict, list)):
            raise ValueError("Expected a JSON object or array")
        return parsed
    raise ValueError(
        f"Expected JSON string, object, or array (got {type(value).__name__})"
    )


def _coerce_json_object(value: Any) -> Dict[str, Any]:
    parsed = _coerce_json_value(value)
    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object")
    return parsed


def _coerce_json_array(value: Any) -> List[Any]:
    parsed = _coerce_json_value(value)
    if not isinstance(parsed, list):
        raise ValueError("Expected a JSON array")
    return parsed


JsonValueInput = Annotated[
    Union[Dict[str, Any], List[Any]],
    BeforeValidator(_coerce_json_value),
]
JsonObjectInput = Annotated[Dict[str, Any], BeforeValidator(_coerce_json_object)]
JsonArrayInput = Annotated[List[Any], BeforeValidator(_coerce_json_array)]

# Back-compat alias for parameters that accept either JSON objects or arrays.
JsonInput = JsonValueInput


def parse_json_input(value: Any, *, name: str = "value") -> Any:
    """Normalize a JSON parameter after MCP validation or from legacy callers."""
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {name} parameter") from e
    raise ValueError(
        f"{name} must be a JSON string, object, or array (got {type(value).__name__})"
    )
