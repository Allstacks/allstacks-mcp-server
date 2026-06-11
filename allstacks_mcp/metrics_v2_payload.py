"""Build JSON bodies for Metrics V2 POST .../metrics_v2/metrics (no HTTP dependencies)."""

from typing import Any, Dict, Optional

from ._json_input import JsonObjectInput, parse_json_input


def build_metrics_v2_post_body(
    config_or_envelope: JsonObjectInput,
    get_count_only: bool = False,
    variables: Optional[JsonObjectInput] = None,
) -> Dict[str, Any]:
    """
    Build the JSON body for POST .../metrics_v2/metrics.

    The API expects: {"config": {...}, "get_count_only": bool, "variables": dict}.
    Callers may pass either (1) the inner config object only, or (2) the full
    envelope with keys among config, get_count_only, variables. Either form may
    be supplied as a JSON string or as the already-parsed Python object.
    """
    parsed = parse_json_input(config_or_envelope, name="config")
    if not isinstance(parsed, dict):
        raise ValueError("config must decode to a JSON object")

    allowed_envelope_keys = {"config", "get_count_only", "variables"}
    if "config" in parsed and set(parsed.keys()) <= allowed_envelope_keys:
        if not isinstance(parsed.get("config"), dict):
            raise ValueError("config must decode to a JSON object")
        body: Dict[str, Any] = {
            "get_count_only": bool(parsed.get("get_count_only", False))
            or get_count_only,
            "variables": parsed.get("variables")
            if isinstance(parsed.get("variables"), dict)
            else {},
            "config": parsed["config"],
        }
        if variables is not None:
            parsed_variables = parse_json_input(variables, name="variables")
            if not isinstance(parsed_variables, dict):
                raise ValueError("variables must decode to a JSON object")
            body["variables"] = parsed_variables
        return body

    body = {
        "config": parsed,
        "get_count_only": get_count_only,
        "variables": {},
    }
    if variables is not None:
        parsed_variables = parse_json_input(variables, name="variables")
        if not isinstance(parsed_variables, dict):
            raise ValueError("variables must decode to a JSON object")
        body["variables"] = parsed_variables
    return body
