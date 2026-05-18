"""Shared JSON-input handling for MCP tool parameters.

Several MCP clients (Claude Desktop and others) automatically parse JSON-shaped
strings into the corresponding object/list before the value reaches FastMCP's
parameter validator. When a tool annotates the parameter as ``str``, validation
then rejects the call because the runtime type is now ``dict`` (or ``list``).

To make these parameters usable across clients, tools should annotate them with
``JsonInput`` and parse them through ``parse_json_input`` so that callers may
pass either a JSON string or the already-parsed Python value.
"""

import json
from typing import Any, Dict, List, Union

JsonInput = Union[str, Dict[str, Any], List[Any]]


def parse_json_input(value: JsonInput, *, name: str = "value") -> Any:
    """Return ``value`` decoded to a Python object.

    Accepts a JSON string, dict, or list. Raises ``ValueError`` with a stable,
    machine-readable message when a string fails to decode or the input is an
    unsupported type.
    """
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {name} parameter: {e}") from e
    raise ValueError(
        f"{name} must be a JSON string, object, or array (got {type(value).__name__})"
    )
