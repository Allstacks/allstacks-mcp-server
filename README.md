# Allstacks MCP Server

A modular Model Context Protocol (MCP) server providing AI-ready access to the Allstacks API using HTTP Basic Authentication.

## Overview

This MCP server exposes **54 tools** organized into **10 categories** for comprehensive interaction with Allstacks:

### Tool Categories

1. **Metrics Data Retrieval (7 tools)**: Access time-series metrics, V2 data explorer, and insight configurations
2. **Service Items & Filtering (6 tools)**: List and search work items, PRs, commits with comprehensive filtering
3. **User & Team Management (4 tools)**: Manage users, teams, and organizational hierarchies
4. **Organization & Projects (4 tools)**: Access projects, services, and work bundles
5. **AI & Analytics (4 tools)**: Get investment analysis, workflow insights, DevEx metrics, and capitalization reports
6. **Dashboards & Widgets (5 tools)**: Manage dashboards, widgets, and shared links
7. **Employee & Productivity (5 tools)**: Track employee metrics, activity periods, and user management
8. **Forecasting & Planning (5 tools)**: Access forecasts, capacity planning, and chart analysis
9. **Labels & Tagging (5 tools)**: Manage labels, tags, and user categorization
10. **Alerts & Monitoring (5 tools)**: Monitor service health, alerts, risks, and audit logs

## Project Structure

```
allstacks-mcp/
├── server.py                    # Main entry point
├── allstacks_mcp/
│   ├── __init__.py
│   ├── client.py               # HTTP Basic Auth client
│   └── tools/                  # Tool modules by category
│       ├── __init__.py
│       ├── metrics.py
│       ├── service_items.py
│       ├── users_teams.py
│       ├── org_projects.py
│       ├── ai_analytics.py
│       ├── dashboards.py
│       ├── employee.py
│       ├── forecasting.py
│       ├── labels.py
│       └── alerts.py
├── pyproject.toml
└── README.md
```

## Installation

1. Clone this repository
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Authentication

The server uses **HTTP Basic Authentication**. You'll need:
- A valid Allstacks username
- A corresponding password or API key

## Usage

### Running the Server

```bash
uv run server.py --username YOUR_USERNAME --password YOUR_PASSWORD
```

**Command-line options:**
- `--username` or `-u`: Username for HTTP Basic authentication (required)
- `--password` or `-p`: Password for HTTP Basic authentication (required)
- `--base-url` or `-b`: Override the default API base URL (default: `https://api.allstacks.com/api/v1/`)

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop's `claude_desktop_config.json`):

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
                "--username",
                "YOUR_USERNAME",
                "--password",
                "YOUR_PASSWORD"
            ]
        }
    }
}
```

## Available Tools

### 1. Metrics Data Retrieval (7 tools)
- `list_metrics` - List all available metric types
- `get_metric_info` - Get detailed metric information
- `get_gmdts_data` - Fetch Generated Metric Data Time Series
- `get_metrics_v2_data` - Fetch data using Metrics V2 configuration
- `list_metrics_v2_configs` - List saved V2 configurations
- `create_metrics_v2_config` - Create new V2 configuration
- `get_insight_configs` - Get insight configurations

### 2. Service Items & Filtering (6 tools)
- `list_service_items` - List work items with filtering
- `get_item_props` - Get available item properties
- `get_configuration_options` - Get configuration options
- `search_service_items` - Full-text search across items
- `get_parent_service_items` - Get hierarchical parent items
- `get_metrics_filter_sets` - Get saved filter sets

### 3. User & Team Management (4 tools)
- `list_service_users` - List users with merge handling
- `get_user_mapping` - Map user keys to names
- `get_user_tags` - Get user categorization tags
- `get_team_categories` - List team hierarchies

### 4. Organization & Projects (4 tools)
- `get_organization_settings` - Get org configuration
- `list_projects` - List all projects
- `get_project_services` - Get connected services
- `get_enabled_work_bundles` - List work bundles

### 5. AI & Analytics (4 tools)
- `get_organization_investments` - Get investment analysis
- `generate_workflow_analysis` - Generate AI workflow reports
- `get_developer_experience_metrics` - Get DevEx metrics
- `get_capitalization_report` - Get R&D capitalization report

### 6. Dashboards & Widgets (5 tools)
- `list_dashboards` - List dashboards
- `get_dashboard_widgets` - Get dashboard widgets
- `create_dashboard_widget` - Create new widget
- `get_shared_links` - Get shared dashboard links
- `create_shared_link` - Create shared dashboard link

### 7. Employee & Productivity (5 tools)
- `get_employee_metrics` - Get employee productivity metrics
- `get_employee_periods` - Get employee activity periods
- `get_employee_users` - Get employee user list
- `get_employee_metric_data` - Get detailed employee metrics
- `merge_service_users` - Merge multiple service users

### 8. Forecasting & Planning (5 tools)
- `get_forecast_v3` - Get v3 forecast data
- `get_slots` - Get resource slots/capacity
- `analyze_chart_data` - Analyze chart data
- `get_chart_analysis` - Get AI analysis for charts
- `get_company_metrics` - Get company-level metrics

### 9. Labels & Tagging (5 tools)
- `list_labels` - List all labels
- `create_label` - Create new label
- `add_service_user_tags` - Add tags to users
- `remove_service_user_tags` - Remove tags from users
- `get_manageable_roles` - Get roles and permissions

### 10. Alerts & Monitoring (5 tools)
- `get_service_item_alerts` - Get service item alerts
- `get_deliverable_risks` - Get deliverable risk assessment
- `get_service_health` - Get service health status
- `get_error_logs` - Get error logs
- `get_audit_log` - Get audit log

## Development

### Adding New Tools

1. Choose the appropriate category in `allstacks_mcp/tools/` or create a new module
2. Add your tool function decorated with `@mcp.tool()`
3. Register it in the module's `register_tools()` function
4. Import and register the module in `server.py` if new

### Modular Structure Benefits

- **Organized**: Tools grouped by functional category
- **Maintainable**: Easy to find and update specific tools
- **Extensible**: Simple to add new categories or tools
- **Testable**: Each module can be tested independently

## Requirements

- Python 3.13+
- httpx (async HTTP client)
- mcp[cli] (Model Context Protocol)

## License

MIT
