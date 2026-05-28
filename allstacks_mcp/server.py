#!/usr/bin/env python3
"""
Allstacks MCP Server - AI-ready interface to Allstacks API

This modular MCP server provides 194+ tools across 12 categories for interacting
with the Allstacks API using HTTP Basic Authentication.
"""

import argparse
import sys

from mcp.server.fastmcp import FastMCP

from .client import AllstacksAPIClient
from .prompt_guard import PromptGuardConfig, config_from_env
from .tools import (
    metrics,
    service_items,
    users_teams,
    org_projects,
    ai_analytics,
    dashboards,
    employee,
    forecasting,
    labels,
    alerts,
    work_bundles,
    risk_management,
)

# Shown in initialize.instructions for connected clients (token cost per turn).
MCP_SERVER_INSTRUCTIONS = (
    "This server wraps the Allstacks REST API (HTTP Basic auth at startup). "
    "Tools return JSON strings; parse them before reasoning. Prefer narrow reads: "
    "pagination (limit/offset), filters, and IDs from list endpoints. "
    "Data is scoped by organization and project: most routes are under "
    "organization/{org_id}/ or project/{project_id}/. A given login usually has one "
    "org; projects are many per org and often align with team or department splits; "
    "service user tags are another common way to segment people—get_metrics_v2_user_tags "
    "for tag values used in Metrics V2 filters. "
    "Happy paths: (1) Org/project context — list_organizations, list_projects, then "
    "scoped calls. (2) Engineering work — list_service_items / get_service_item_* "
    "with item_type (e.g. PULL_REQUEST, COMMIT, CARD); use get_service_item_property_keys "
    "before complex filters. (3) Metrics — list_metrics or get_project_metrics_list, "
    "get_metric_info / get_generated_metric, then get_project_metrics_v2_data or "
    "get_org_metrics_v2_data for time series. AI-built Metrics V2 example: call "
    "ai_metric_builder(project_id, prompt, stream=false), parse the JSON string, "
    "take inner = obj['config'] if isinstance(obj.get('config'), dict) else obj, "
    "then get_project_metrics_v2_data(project_id, json.dumps(inner)); use "
    "previous_config as a JSON string to refine the builder across turns. "
    "Org-scoped charts use get_org_metrics_v2_data(org_id, config) with the same "
    "inner config shape. (4) Dashboards — list_org_dashboards, "
    "get_org_dashboard, list_dashboard_widgets. (5) AI insights — list_ai_reports "
    "as appropriate. "
    "Errors may appear as JSON with error/status_code instead of exceptions."
)

# Initialize FastMCP server
mcp = FastMCP("Allstacks-MCP", instructions=MCP_SERVER_INSTRUCTIONS)

# Global API client
api_client = None


def register_all_tools():
    """Register all tool modules with the MCP server"""
    metrics.register_tools(mcp, api_client)
    service_items.register_tools(mcp, api_client)
    users_teams.register_tools(mcp, api_client)
    org_projects.register_tools(mcp, api_client)
    ai_analytics.register_tools(mcp, api_client)
    dashboards.register_tools(mcp, api_client)
    employee.register_tools(mcp, api_client)
    forecasting.register_tools(mcp, api_client)
    labels.register_tools(mcp, api_client)
    alerts.register_tools(mcp, api_client)
    work_bundles.register_tools(mcp, api_client)
    risk_management.register_tools(mcp, api_client)


def _build_prompt_guard_config(args: argparse.Namespace) -> PromptGuardConfig:
    """Merge CLI flags with env-var defaults (CLI wins)."""
    env = config_from_env()
    return PromptGuardConfig(
        enabled=args.prompt_guard if args.prompt_guard is not None else env.enabled,
        fail_open=(
            args.prompt_guard_fail_open
            if args.prompt_guard_fail_open is not None
            else env.fail_open
        ),
        external_url=args.prompt_guard_url or env.external_url,
        external_timeout=env.external_timeout,
        external_token=env.external_token,
        heuristics_enabled=env.heuristics_enabled,
    )


def main():
    """Main entry point for the Allstacks MCP server"""
    global api_client

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Allstacks MCP Server - AI-ready interface to Allstacks API"
    )
    parser.add_argument(
        "--username", "-u", help="Username for HTTP Basic auth (paired with --password)"
    )
    parser.add_argument(
        "--password", "-p", help="Password for HTTP Basic auth (paired with --username)"
    )
    parser.add_argument(
        "--token",
        "-t",
        help=(
            "Personal Access Token / API Token for Bearer auth. "
            "Required for SSO-only users; alternative to --username/--password."
        ),
    )
    parser.add_argument(
        "--base-url",
        "-b",
        default="https://app.allstacks.com/api/v1/",
        help="Base URL for the API (default: https://app.allstacks.com/api/v1/)",
    )

    # PromptGuard response-scanning flags
    parser.add_argument(
        "--prompt-guard",
        action="store_true",
        default=None,
        help=(
            "Enable PromptGuard response scanning for indirect prompt injection. "
            "Also enabled by env ALLSTACKS_PROMPT_GUARD=1."
        ),
    )
    parser.add_argument(
        "--prompt-guard-fail-open",
        action="store_true",
        default=None,
        help=(
            "If the external scanner is unreachable, allow responses through "
            "instead of blocking (fail-open). Default is fail-closed."
        ),
    )
    parser.add_argument(
        "--prompt-guard-url",
        default=None,
        help=(
            "URL of an external PromptGuard scanner service (e.g. Llama "
            "PromptGuard 2 wrapper). Optional; heuristics run regardless."
        ),
    )

    # Parse arguments
    args = parser.parse_args()

    if args.token and (args.username or args.password):
        parser.error("--token cannot be combined with --username/--password")
    if not args.token and not (args.username and args.password):
        parser.error("must provide --token, or both --username and --password")

    pg_config = _build_prompt_guard_config(args)

    if pg_config.enabled:
        print(
            "PromptGuard: enabled"
            f" | fail-{'open' if pg_config.fail_open else 'closed'}"
            f" | external={'yes' if pg_config.external_url else 'no'}"
            f" | heuristics={'on' if pg_config.heuristics_enabled else 'off'}",
            file=sys.stderr,
        )

    if args.token:
        api_client = AllstacksAPIClient(
            base_url=args.base_url,
            token=args.token,
            prompt_guard_config=pg_config,
        )
    else:
        api_client = AllstacksAPIClient(
            args.username,
            args.password,
            args.base_url,
            prompt_guard_config=pg_config,
        )

    # Register all tools from the various modules
    register_all_tools()

    # Run the MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
