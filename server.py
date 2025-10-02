#!/usr/bin/env python3
"""
Allstacks MCP Server - AI-ready interface to Allstacks API

This modular MCP server provides 208+ tools across 12 categories for interacting
with the Allstacks API using HTTP Basic Authentication.
"""

import argparse
from mcp.server.fastmcp import FastMCP

from allstacks_mcp.client import AllstacksAPIClient
from allstacks_mcp.tools import (
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
    risk_management
)

# Initialize FastMCP server
mcp = FastMCP("Allstacks-MCP")

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


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Allstacks MCP Server - AI-ready interface to Allstacks API'
    )
    parser.add_argument(
        '--username', '-u',
        required=True,
        help='Username for HTTP Basic authentication'
    )
    parser.add_argument(
        '--password', '-p',
        required=True,
        help='Password for HTTP Basic authentication'
    )
    parser.add_argument(
        '--base-url', '-b',
        default='https://api.allstacks.com/api/v1/',
        help='Base URL for the API (default: https://api.allstacks.com/api/v1/)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the API client with HTTP Basic Auth
    api_client = AllstacksAPIClient(args.username, args.password, args.base_url)
    
    # Register all tools from the various modules
    register_all_tools()
    
    # Run the MCP server
    mcp.run(transport='stdio')

