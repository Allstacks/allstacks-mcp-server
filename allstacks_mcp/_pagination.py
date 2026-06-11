"""Helpers for honoring MCP pagination params on list responses."""

from typing import Any


def cap_list_payload(payload: Any, *, limit: int, offset: int = 0) -> Any:
    """Slice list payloads when the API returns more rows than ``limit``."""
    if isinstance(payload, list) and len(payload) > limit:
        return payload[offset : offset + limit]

    if isinstance(payload, dict):
        results = payload.get("results")
        if isinstance(results, list) and len(results) > limit:
            capped = dict(payload)
            capped["results"] = results[offset : offset + limit]
            return capped

    return payload
