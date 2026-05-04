"""Build JSON bodies for Metrics V2 POST .../metrics_v2/metrics (no HTTP dependencies)."""

import json
from typing import Any, Dict, Optional


def build_metrics_v2_post_body(
    config_or_envelope: str,
    get_count_only: bool = False,
    variables: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build the JSON body for POST .../metrics_v2/metrics.

    The API expects: {"config": {...}, "get_count_only": bool, "variables": dict}.
    Callers may pass either (1) a JSON string of the inner config object only, or
    (2) a JSON string of the full envelope with keys among config, get_count_only, variables.
    """
    try:
        parsed = (
            json.loads(config_or_envelope)
            if isinstance(config_or_envelope, str)
            else config_or_envelope
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e
    if not isinstance(parsed, dict):
        raise ValueError("config_or_envelope must decode to a JSON object")

    allowed_envelope_keys = {"config", "get_count_only", "variables"}
    if "config" in parsed and set(parsed.keys()) <= allowed_envelope_keys:
        body: Dict[str, Any] = {
            "get_count_only": bool(parsed.get("get_count_only", False))
            or get_count_only,
            "variables": parsed.get("variables")
            if isinstance(parsed.get("variables"), dict)
            else {},
            "config": parsed["config"],
        }
        if variables is not None:
            try:
                body["variables"] = (
                    json.loads(variables) if isinstance(variables, str) else variables
                )
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in variables: {e}") from e
        return body

    body = {
        "config": parsed,
        "get_count_only": get_count_only,
        "variables": {},
    }
    if variables is not None:
        try:
            body["variables"] = (
                json.loads(variables) if isinstance(variables, str) else variables
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in variables: {e}") from e
    return body
