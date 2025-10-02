# Allstacks MCP Server

A Model Context Protocol (MCP) server providing AI-ready access to the Allstacks API.

## Overview

This MCP server exposes 29 tools for interacting with Allstacks, including:

- **Metrics Data Retrieval (7 tools)**: Access time-series metrics, V2 data explorer, and insight configurations
- **Service Items & Filtering (6 tools)**: List and search work items, PRs, commits with comprehensive filtering
- **User & Team Management (4 tools)**: Manage users, teams, and organizational hierarchies
- **Organization & Projects (4 tools)**: Access projects, services, and work bundles
- **AI & Analytics (4 tools)**: Get investment analysis, workflow insights, DevEx metrics, and capitalization reports

## Installation

1. Clone this repository
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Usage

The server requires an Allstacks API token to authenticate requests.

### Running the Server

```bash
uv run server.py --api-token YOUR_API_TOKEN
```

Optional parameters:
- `--base-url` or `-u`: Override the default API base URL (default: `https://api.allstacks.com/api/v1/`)

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
    "mcpServers": {
        "allstacks": {
            "command": "uv",
            "args": [
                "--directory",
                "/absolute/path/to/allstacks-mcp",
                "run",
                "server.py",
                "--api-token",
                "YOUR_ALLSTACKS_API_TOKEN"
            ]
        }
    }
}
```

## Available Tools

### Metrics Data Retrieval
- `list_metrics` - List all available metric types
- `get_metric_info` - Get detailed metric information
- `get_gmdts_data` - Fetch Generated Metric Data Time Series
- `get_metrics_v2_data` - Fetch data using Metrics V2 configuration
- `list_metrics_v2_configs` - List saved V2 configurations
- `create_metrics_v2_config` - Create new V2 configuration
- `get_insight_configs` - Get insight configurations

### Service Items & Filtering
- `list_service_items` - List work items with filtering
- `get_item_props` - Get available item properties
- `get_configuration_options` - Get configuration options
- `search_service_items` - Full-text search across items
- `get_parent_service_items` - Get hierarchical parent items
- `get_metrics_filter_sets` - Get saved filter sets

### User & Team Management
- `list_service_users` - List users with merge handling
- `get_user_mapping` - Map user keys to names
- `get_user_tags` - Get user categorization tags
- `get_team_categories` - List team hierarchies

### Organization & Projects
- `get_organization_settings` - Get org configuration
- `list_projects` - List all projects
- `get_project_services` - Get connected services
- `get_enabled_work_bundles` - List work bundles

### AI & Analytics
- `get_organization_investments` - Get investment analysis
- `generate_workflow_analysis` - Generate AI workflow reports
- `get_developer_experience_metrics` - Get DevEx metrics
- `get_capitalization_report` - Get R&D capitalization report

## Requirements

- Python 3.13+
- httpx
- mcp[cli]

## License

MIT

