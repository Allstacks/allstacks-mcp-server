# Allstacks MCP Server

<!-- mcp-name: com.allstacks/allstacks-mcp -->

A comprehensive Model Context Protocol (MCP) server providing AI-ready access to the Allstacks API using HTTP Basic Authentication.

## Overview

This MCP server exposes **208+ tools** organized into **12 categories** for comprehensive interaction with Allstacks:

### Tool Categories

1. **Metrics & Analytics (18 tools)**: GMDTS data, Metrics V2, insight configs, population benchmarks, company metrics
2. **Service Items & Work Items (21 tools)**: Complete CRUD for work items, parent service items, property keys, estimation methods, notes, filter sets
3. **Users & Teams (23 tools)**: Full user management, invites, roles, team tags, personal access tokens, service users
4. **Organization & Projects (28 tools)**: Organizations, projects, settings, services, calendars, time periods, slots configuration
5. **Dashboards & Widgets (20 tools)**: Complete dashboard/widget CRUD, shared links, cloning, widget management
6. **Employee Analytics (9 tools)**: Employee metrics, cohorts, work items, timeline, summary, periods
7. **Forecasting & Planning (11 tools)**: V3 forecasts, velocity, scenarios, capacity planning, chart analysis
8. **Labels & Tagging (17 tools)**: Labels, label families, bulk operations, service item label assignment
9. **Alerts & Monitoring (16 tools)**: Alert rules, active alerts, notifications, subscriptions, preferences
10. **AI & Intelligence (18 tools)**: AI reports, Action AI code query, metric builder, pattern analysis, surveys, DX scores, AI tool usage
11. **Work Bundles (13 tools)**: Selectable work bundle management, forecasting, metrics, cloning
12. **Risk Management (14 tools)**: Risk definitions, project risks, assessment, trends, resolution

## Project Structure

```
allstacks-mcp/
├── server.py                    # Main entry point - 208+ tools
├── allstacks_mcp/
│   ├── __init__.py
│   ├── client.py               # HTTP Basic Auth client
│   └── tools/                  # Tool modules by category
│       ├── __init__.py
│       ├── metrics.py          # 18 metrics tools
│       ├── service_items.py    # 21 service item tools
│       ├── users_teams.py      # 23 user/team tools
│       ├── org_projects.py     # 28 org/project tools
│       ├── dashboards.py       # 20 dashboard tools
│       ├── employee.py         # 9 employee analytics tools
│       ├── forecasting.py      # 11 forecasting tools
│       ├── labels.py           # 17 label management tools
│       ├── alerts.py           # 16 alert/monitoring tools
│       ├── ai_analytics.py     # 18 AI & analytics tools
│       ├── work_bundles.py     # 13 work bundle tools
│       └── risk_management.py  # 14 risk management tools
├── pyproject.toml
├── uv.lock
├── FILTERED_ENDPOINTS.md       # Endpoint verification document
├── TOOLS_MAPPING.md            # Complete API mapping
├── ENDPOINT_VERIFICATION.md    # Verification results
└── README.md
```

## Installation

1. Clone this repository
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Authentication & Security

### Required Credentials

The server uses **HTTP Basic Authentication** to connect to the Allstacks API. You'll need:
- **Username**: Your Allstacks username or email address
- **Password**: Your Allstacks password or API key
- **Base URL**: (Optional) Default is `https://api.allstacks.com/api/v1/`

### 🔒 Security Best Practices

#### Credential Management

**⚠️ IMPORTANT**: Your credentials provide full access to your Allstacks account.

1. **Use Environment Variables** (Recommended)
   ```bash
   export ALLSTACKS_USERNAME="your-username"
   export ALLSTACKS_PASSWORD="your-api-key"
   ```

2. **Use Allstacks API Keys** instead of passwords when possible
   - Generate API keys from your Allstacks account settings
   - API keys can be revoked without changing your password

3. **Never commit credentials** to version control
   - The MCP client config file may contain credentials
   - Keep config files in `.gitignore`

4. **Rotate credentials regularly** for enhanced security

#### Process Security

**Note**: Command-line arguments (`--username`, `--password`) are visible in process lists. For production use:
- Use environment variables
- Use secure configuration files
- Consider using a secrets management system

#### Data Access & Privacy

This MCP server acts as a **pass-through** to the Allstacks API:
- ✅ Does not store or log your credentials
- ✅ Does not cache API responses
- ✅ Does not persist any data locally
- ✅ Returns API data as-is without modification

**AI Access**: When used with AI assistants (e.g., Claude), the AI will have access to:
- All data accessible via your Allstacks credentials
- The same permissions as your Allstacks user account
- Ability to create, modify, and delete resources (depending on your permissions)

**Recommendation**: Consider using a dedicated Allstacks account with limited permissions for AI access.

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
                "/ABSOLUTE/PATH/TO/allstacks-mcp",
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

**Important Notes:**
- Replace `/ABSOLUTE/PATH/TO/allstacks-mcp` with the full path to this directory
- Replace `YOUR_USERNAME` and `YOUR_PASSWORD` with your actual credentials
- On macOS, `uv` is typically located at `~/.local/bin/uv` - ensure it's in your PATH or use the full path
- Claude Desktop doesn't inherit your shell's PATH, so using the full path to `uv` is more reliable

### Alternative Configuration (Direct Python)

If you prefer to use Python directly from a virtual environment:

```json
{
    "mcpServers": {
        "allstacks": {
            "command": "/ABSOLUTE/PATH/TO/allstacks-mcp/.venv/bin/python",
            "args": [
                "/ABSOLUTE/PATH/TO/allstacks-mcp/server.py",
                "--username",
                "YOUR_USERNAME",
                "--password",
                "YOUR_PASSWORD"
            ]
        }
    }
}
```

## Features

### Comprehensive API Coverage

All tools are verified against the official Allstacks OpenAPI specification:
- ✅ All endpoints use correct paths and parameters
- ✅ Detailed parameter descriptions from official API docs
- ✅ Proper error handling and validation
- ✅ HTTP Basic Auth support
- ✅ Async/await for performance

### Modular Architecture

Tools are organized into logical categories matching the Allstacks API structure:
- Easy to navigate and understand
- Clear separation of concerns
- Consistent patterns across all tools
- Well-documented with OpenAPI references

### Rich Tool Descriptions

Every tool includes:
- Purpose and use case
- Required and optional parameters
- Expected return formats
- OpenAPI endpoint reference
- Example usage patterns

## Example Tool Usage

### Get GMDTS Metrics Data
```python
# Get Generated Metric Data Time Series (GMDTS)
get_gmdts_data(
    project_id=123,
    metric_type="Velocity",
    start_date=1704067200000,
    end_date=1706745600000
)
```

### List Work Items with Filtering
```python
# List service items with filtering
list_service_items(
    item_type="CARD",
    limit=100,
    offset=0
)
```

### Create AI Report
```python
# Generate AI analysis report
create_ai_report(
    org_id=456,
    report_type="project_health",
    project_id=123
)
```

### Forecast Work Bundle
```python
# Get Monte Carlo forecast for work bundle
get_work_bundle_forecast(
    project_id=123,
    bundle_id=789,
    confidence_level=80
)
```

## API Compatibility

This server is built against the official Allstacks API v1 specification and includes:
- Non-admin endpoints only (no destructive operations)
- Full CRUD for resources where appropriate
- Bulk operations for efficiency
- Proper pagination support
- Query parameter validation

## Development

### Adding New Tools

1. Create or update a tool file in `allstacks_mcp/tools/`
2. Follow the existing pattern for tool registration
3. Include full docstrings with OpenAPI references
4. Add the module to `allstacks_mcp/tools/__init__.py`
5. Register it in `server.py`'s `register_all_tools()` function

### Testing

```bash
# Run the server in development mode
uv run server.py --username test_user --password test_pass --base-url https://api-dev.allstacks.com/api/v1/
```

## License

MIT

## Support

For issues or questions about the Allstacks API, contact the Allstacks team.
For issues specific to this MCP server, please file an issue in the repository.
