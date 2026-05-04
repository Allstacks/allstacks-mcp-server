#!/usr/bin/env python3
"""
Allstacks MCP Server - AI-ready interface to Allstacks API

This modular MCP server provides 194+ tools across 12 categories for interacting
with the Allstacks API using HTTP Basic Authentication.
"""

import argparse
from mcp.server.fastmcp import FastMCP

from .client import AllstacksAPIClient
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
    "get_org_dashboard, list_dashboard_widgets. (5) AI insights — list_ai_reports, "
    "get_insights, get_developer_experience_score as appropriate. "
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


def main():
    """Main entry point for the Allstacks MCP server"""
    global api_client

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Allstacks MCP Server - AI-ready interface to Allstacks API"
    )
    parser.add_argument(
        "--username", "-u", required=True, help="Username for HTTP Basic authentication"
    )
    parser.add_argument(
        "--password", "-p", required=True, help="Password for HTTP Basic authentication"
    )
    parser.add_argument(
        "--base-url",
        "-b",
        default="https://api.allstacks.com/api/v1/",
        help="Base URL for the API (default: https://api.allstacks.com/api/v1/)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Initialize the API client with HTTP Basic Auth
    api_client = AllstacksAPIClient(args.username, args.password, args.base_url)

    # Register all tools from the various modules
    register_all_tools()

    # Run the MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
