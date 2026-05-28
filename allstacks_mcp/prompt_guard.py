"""Response scanning for indirect prompt injection.

Allstacks data originates from Jira, GitHub, PR descriptions, commit messages,
and similar user-authored text — classic indirect injection surfaces.  This
module scans API responses before they reach the model and blocks content that
looks like an injection attempt.

Behaviour defaults:
  - ENABLED  via ``--prompt-guard`` CLI flag or ``ALLSTACKS_PROMPT_GUARD=1``
  - FAIL-CLOSED when the scanner itself errors (safe default)
  - Optional FAIL-OPEN with ``--prompt-guard-fail-open`` for availability-first
    deployments

Two scanning layers (either/both may be active):
  1. Built-in heuristic patterns (always available, zero dependencies)
  2. Optional external scanner service (HTTP POST, e.g. Llama PromptGuard 2)
"""

import logging
import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Heuristic patterns — each targets a known indirect-injection vector that
# could appear in Jira tickets, PR descriptions, commit messages, etc.
# ---------------------------------------------------------------------------

_HEURISTIC_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (
        re.compile(r"(?:^|\n)\s*(?:system|assistant)\s*:", re.IGNORECASE),
        "role-prefix injection (system:/assistant:)",
    ),
    (
        re.compile(
            r"(?:ignore|disregard|forget)\s+(?:all\s+)?(?:previous|prior|above|earlier)"
            r"\s+(?:instructions|prompts|context|directives|rules)",
            re.IGNORECASE,
        ),
        "instruction-override attempt",
    ),
    (
        re.compile(r"you\s+are\s+now\s+(?:a|an|in)\b", re.IGNORECASE),
        "persona-hijack attempt",
    ),
    (
        re.compile(
            r"\bdo\s+not\s+(?:follow|obey|listen\s+to)\s+(?:your|the|any)\s+"
            r"(?:instructions|rules|guidelines|system\s+prompt)",
            re.IGNORECASE,
        ),
        "instruction-suppression attempt",
    ),
    (
        re.compile(
            r"<\s*(?:system|instruction|prompt|context)\s*>",
            re.IGNORECASE,
        ),
        "XML tag injection (<system>, <instruction>, etc.)",
    ),
    (
        re.compile(
            r"\[\s*(?:SYSTEM|INST|INSTRUCTION)\s*\]",
        ),
        "bracket tag injection ([SYSTEM], [INST], etc.)",
    ),
    (
        re.compile(
            r"(?:^|\n)\s*#{1,3}\s*(?:system\s+prompt|instructions|new\s+instructions)",
            re.IGNORECASE,
        ),
        "markdown heading injection (## System Prompt, etc.)",
    ),
    (
        re.compile(
            r"(?:reveal|output|print|show|repeat|echo)\s+(?:your\s+)?"
            r"(?:system\s+prompt|instructions|secret|api\s*key|token|password)",
            re.IGNORECASE,
        ),
        "exfiltration attempt (reveal system prompt / secrets)",
    ),
]


class ScanVerdict(str, Enum):
    ALLOWED = "allowed"
    BLOCKED_HEURISTIC = "blocked_heuristic"
    BLOCKED_EXTERNAL = "blocked_external"
    BLOCKED_SCANNER_ERROR = "blocked_scanner_error"


@dataclass
class ScanResult:
    verdict: ScanVerdict
    reason: str = ""
    matched_text: str = ""


@dataclass
class PromptGuardConfig:
    enabled: bool = False
    fail_open: bool = False
    external_url: Optional[str] = None
    external_timeout: float = 5.0
    external_token: Optional[str] = None
    heuristics_enabled: bool = True


def config_from_env() -> PromptGuardConfig:
    """Build a PromptGuardConfig from environment variables only.

    CLI args override these in server.py — this provides a baseline for
    environments that inject config exclusively via env vars (containers,
    MCP client stanzas, etc.).
    """
    enabled = os.environ.get("ALLSTACKS_PROMPT_GUARD", "").strip()
    fail_open = os.environ.get("ALLSTACKS_PROMPT_GUARD_FAIL_OPEN", "").strip()
    external_url = os.environ.get("ALLSTACKS_PROMPT_GUARD_URL", "").strip() or None
    external_token = os.environ.get("ALLSTACKS_PROMPT_GUARD_TOKEN", "").strip() or None
    external_timeout = os.environ.get("ALLSTACKS_PROMPT_GUARD_TIMEOUT", "").strip()
    heuristics = os.environ.get("ALLSTACKS_PROMPT_GUARD_HEURISTICS", "").strip()

    return PromptGuardConfig(
        enabled=enabled in ("1", "true", "yes"),
        fail_open=fail_open in ("1", "true", "yes"),
        external_url=external_url,
        external_timeout=float(external_timeout) if external_timeout else 5.0,
        external_token=external_token,
        heuristics_enabled=heuristics not in ("0", "false", "no"),
    )


def _flatten_to_strings(obj: Any, max_depth: int = 10) -> List[str]:
    """Recursively extract all string values from a nested dict/list."""
    if max_depth <= 0:
        return []
    results: List[str] = []
    if isinstance(obj, str):
        results.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            results.extend(_flatten_to_strings(v, max_depth - 1))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(_flatten_to_strings(item, max_depth - 1))
    return results


def _scan_heuristics(text: str) -> Optional[ScanResult]:
    for pattern, reason in _HEURISTIC_PATTERNS:
        match = pattern.search(text)
        if match:
            return ScanResult(
                verdict=ScanVerdict.BLOCKED_HEURISTIC,
                reason=reason,
                matched_text=match.group(0)[:200],
            )
    return None


async def _scan_external(text: str, config: PromptGuardConfig) -> Optional[ScanResult]:
    """Call an external scanner service (e.g. Llama PromptGuard 2 wrapper).

    Expected request:  POST { "text": "..." }
    Expected response: { "safe": true/false, "reason": "..." }
    """
    if not config.external_url:
        return None

    headers: Dict[str, str] = {"Content-Type": "application/json"}
    if config.external_token:
        headers["Authorization"] = f"Bearer {config.external_token}"

    try:
        async with httpx.AsyncClient(timeout=config.external_timeout) as client:
            resp = await client.post(
                config.external_url,
                json={"text": text},
                headers=headers,
            )
            resp.raise_for_status()
            body = resp.json()

            if not body.get("safe", True):
                return ScanResult(
                    verdict=ScanVerdict.BLOCKED_EXTERNAL,
                    reason=body.get("reason", "external scanner flagged content"),
                )
            return None
    except Exception as exc:
        logger.warning("PromptGuard external scanner error: %s", exc)
        if config.fail_open:
            return None
        return ScanResult(
            verdict=ScanVerdict.BLOCKED_SCANNER_ERROR,
            reason=f"external scanner unavailable: {exc}",
        )


async def scan_response(response_data: Any, config: PromptGuardConfig) -> ScanResult:
    """Scan an API response payload for indirect prompt injection.

    Returns ALLOWED when content is safe, or a BLOCKED_* verdict with details.
    """
    if not config.enabled:
        return ScanResult(verdict=ScanVerdict.ALLOWED)

    if isinstance(response_data, dict) and response_data.get("error"):
        return ScanResult(verdict=ScanVerdict.ALLOWED, reason="error response skipped")

    strings = _flatten_to_strings(response_data)
    combined = "\n".join(strings)

    if not combined.strip():
        return ScanResult(verdict=ScanVerdict.ALLOWED, reason="empty content")

    if config.heuristics_enabled:
        heuristic_result = _scan_heuristics(combined)
        if heuristic_result is not None:
            return heuristic_result

    if config.external_url:
        external_result = await _scan_external(combined, config)
        if external_result is not None:
            return external_result

    return ScanResult(verdict=ScanVerdict.ALLOWED)


def blocked_response(scan_result: ScanResult) -> Dict:
    """Build the structured response returned to the model when content is blocked."""
    return {
        "prompt_guard": {
            "blocked": True,
            "verdict": scan_result.verdict.value,
            "reason": scan_result.reason,
        },
        "error": True,
        "message": (
            "Response blocked by PromptGuard: content flagged as potential "
            "indirect prompt injection. The original API data has been withheld. "
            "This is a safety measure — the upstream data source (Jira, GitHub, etc.) "
            "may contain adversarial text."
        ),
    }
