"""Token-oriented object notation encoding for JSON-compatible payloads."""

import json
import re
from collections.abc import Mapping, Sequence
from typing import Any


_BARE_STRING = re.compile(r"^[A-Za-z0-9_./@+-]+(?: [A-Za-z0-9_./@+-]+)*$")
_AMBIGUOUS_STRINGS = {"true", "false", "null"}
_SCALAR_TYPES = (str, int, float, bool, type(None))


def encode_toon(payload: Any) -> str:
    """Encode a JSON-compatible value using a compact TOON-like notation."""
    return _encode_value(payload, key=None, indent=0).rstrip()


def _encode_value(value: Any, key: str | None, indent: int) -> str:
    if _is_tabular_list(value):
        return _encode_tabular_list(value, key=key, indent=indent)
    if isinstance(value, Mapping):
        return _encode_mapping(value, key=key, indent=indent)
    if _is_sequence(value):
        return _encode_sequence(value, key=key, indent=indent)
    return _encode_scalar_line(value, key=key, indent=indent)


def _encode_mapping(value: Mapping[str, Any], key: str | None, indent: int) -> str:
    prefix = " " * indent
    if not value:
        return _encode_scalar_line({}, key=key, indent=indent)

    lines = []
    child_indent = indent
    if key is not None:
        lines.append(f"{prefix}{key}:")
        child_indent += 2

    for child_key, child_value in value.items():
        lines.append(
            _encode_value(child_value, key=str(child_key), indent=child_indent)
        )
    return "\n".join(lines)


def _encode_sequence(value: Sequence[Any], key: str | None, indent: int) -> str:
    prefix = " " * indent
    header = f"{key}[{len(value)}]:" if key is not None else f"[{len(value)}]:"
    if not value:
        return f"{prefix}{header}"

    lines = [f"{prefix}{header}"]
    for item in value:
        item_prefix = " " * (indent + 2)
        if isinstance(item, Mapping):
            if not item:
                lines.append(f"{item_prefix}- {{}}")
            else:
                lines.append(f"{item_prefix}-")
                lines.append(_encode_mapping(item, key=None, indent=indent + 4))
        elif _is_sequence(item):
            lines.append(f"{item_prefix}-")
            lines.append(_encode_sequence(item, key=None, indent=indent + 4))
        else:
            lines.append(f"{item_prefix}- {_format_scalar(item)}")
    return "\n".join(lines)


def _encode_tabular_list(
    value: Sequence[Mapping[str, Any]], key: str | None, indent: int
) -> str:
    prefix = " " * indent
    headers = [str(header) for header in value[0].keys()]
    header_text = ",".join(headers)
    label = (
        f"{key}[{len(value)}]{{{header_text}}}:"
        if key is not None
        else f"[{len(value)}]{{{header_text}}}:"
    )

    lines = [f"{prefix}{label}"]
    for row in value:
        values = (_format_scalar(row[header]) for header in headers)
        lines.append(f"{prefix}{','.join(values)}")
    return "\n".join(lines)


def _encode_scalar_line(value: Any, key: str | None, indent: int) -> str:
    prefix = " " * indent
    scalar = _format_scalar(value)
    if key is None:
        return f"{prefix}{scalar}"
    return f"{prefix}{key}: {scalar}"


def _format_scalar(value: Any) -> str:
    if isinstance(value, str):
        if _can_emit_bare_string(value):
            return value
        return json.dumps(value, separators=(",", ":"))
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return json.dumps(value, allow_nan=False, separators=(",", ":"))
    return json.dumps(value, separators=(",", ":"))


def _can_emit_bare_string(value: str) -> bool:
    if value.strip() != value:
        return False
    if value.lower() in _AMBIGUOUS_STRINGS:
        return False
    return bool(_BARE_STRING.fullmatch(value))


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    )


def _is_tabular_list(value: Any) -> bool:
    if not _is_sequence(value) or not value:
        return False
    if not all(isinstance(item, Mapping) and item for item in value):
        return False

    headers = tuple(value[0].keys())
    return all(
        tuple(item.keys()) == headers
        and all(isinstance(item[header], _SCALAR_TYPES) for header in headers)
        for item in value
    )
