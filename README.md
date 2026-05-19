# Allstacks MCP Server

<!-- mcp-name: com.allstacks/allstacks-mcp -->

A comprehensive Model Context Protocol (MCP) server providing AI-ready access to the Allstacks API. Authenticate with either HTTP Basic (username + password) or a Bearer Personal Access Token.

## Overview

This MCP server exposes **187 tools** organized into **12 categories** for comprehensive interaction with Allstacks:

### Tool Categories

1. **Metrics & Analytics (20 tools)**: GMDTS data, Metrics V2 (including capitalization preview), templates, insight configs, population benchmarks, company metrics
2. **Service Items & Work Items (18 tools)**: Complete CRUD for work items, parent service items, property keys, estimation methods, notes, filter sets
3. **Users & Teams (20 tools)**: Full user management, invites, roles, team tags, personal access tokens, service users
4. **Organization & Projects (28 tools)**: Organizations, projects, settings, services, calendars, time periods, slots, capitalization reports (V2)
5. **Dashboards & Widgets (18 tools)**: Complete dashboard/widget CRUD, shared links, cloning, widget management
6. **Employee Analytics (8 tools)**: Employee metrics, cohorts, work items, timeline, summary, periods
7. **Forecasting & Planning (9 tools)**: V3 forecasts, velocity, scenarios, capacity planning, chart analysis
8. **Labels & Tagging (15 tools)**: Labels, label families, bulk operations, service item label assignment
9. **Alerts & Monitoring (13 tools)**: Alert rules, active alerts, notifications, subscriptions, preferences
10. **AI & Intelligence (14 tools)**: AI reports, Action AI code query, metric builder, AI metric builder (project), pattern analysis, surveys, DX scores, AI tool usage
11. **Work Bundles (12 tools)**: Selectable work bundle management, forecasting, metrics, cloning
12. **Risk Management (12 tools)**: Risk definitions, project risks, assessment, trends, resolution

## Project Structure

```
allstacks-mcp-server/
├── allstacks_mcp/
│   ├── __init__.py
│   ├── __main__.py             # python -m allstacks_mcp entry point
│   ├── server.py               # Main entry — 187 tools, arg parsing
│   ├── client.py               # HTTP client (Basic + Bearer auth)
│   └── tools/                  # Tool modules by category
│       ├── __init__.py
│       ├── metrics.py          # 20 metrics tools
│       ├── service_items.py    # 18 service item tools
│       ├── users_teams.py      # 20 user/team tools
│       ├── org_projects.py     # 28 org/project tools
│       ├── dashboards.py       # 18 dashboard tools
│       ├── employee.py         # 8 employee analytics tools
│       ├── forecasting.py      # 9 forecasting tools
│       ├── labels.py           # 15 label management tools
│       ├── alerts.py           # 13 alert/monitoring tools
│       ├── ai_analytics.py     # 14 AI & analytics tools
│       ├── work_bundles.py     # 12 work bundle tools
│       └── risk_management.py  # 12 risk management tools
├── pyproject.toml
├── uv.lock
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Allstacks account with either:
  - Personal Access Token (PAT) from the Allstacks UI — **recommended for all users, required for SSO**
  - Username + password (only for local accounts, not SSO)

### Installation

The simplest way to use the Allstacks MCP server is via `uvx`, which installs and runs the server in one command:

```bash
uvx allstacks-mcp --token YOUR_PAT --base-url https://app.allstacks.com/api/v1/
```

That's it! The server will start and be ready to accept MCP connections.

> See [Authentication Modes](#authentication-modes) for the full set of supported auth options (PAT vs. HTTP Basic) and when to use each. For local development or contributing to this project, see the [Local Development](#local-development) section below.

## Authentication & Security

### Authentication Modes

The server supports two authentication modes. Pick **one** — they are mutually exclusive.

#### Option A — Bearer auth with a Personal Access Token (recommended; required for SSO users)

Generate a PAT in the Allstacks UI under **Personal Access Tokens** and pass it with `--token`:

```bash
uvx allstacks-mcp --token YOUR_PAT --base-url https://app.allstacks.com/api/v1/
```

- ✅ Works for **all users**, including SSO-only accounts
- ✅ Tokens can be revoked from the UI without changing account credentials
- ✅ More secure than password-based auth
- Token is sent as `Authorization: Bearer <token>`

#### Option B — HTTP Basic auth with username + password

Only works for **local accounts** that have a password set. SSO-only users will get a 401 error.

```bash
uvx allstacks-mcp --username your-email@example.com --password your-password --base-url https://app.allstacks.com/api/v1/
```

- ⚠️ Only for local accounts (not SSO users)
- Credentials are sent using HTTP Basic authentication

**Base URL:** The default is `https://app.allstacks.com/api/v1/`. Override with `--base-url` if your deployment uses a different endpoint.

### 🔒 Security Best Practices

#### Credential Management

**⚠️ IMPORTANT**: Your credentials provide full access to your Allstacks account.

1. **Prefer Personal Access Tokens over passwords** — revocable, scoped, and the only option for SSO users.

2. **Keep credentials out of shell history and config files** when possible. The server only reads credentials from CLI flags, so if you want to store them in environment variables, expand them into the flags at launch time:
   ```bash
   export ALLSTACKS_TOKEN="your-pat"
   uvx allstacks-mcp --token "$ALLSTACKS_TOKEN"

   # or, for Basic auth:
   export ALLSTACKS_USERNAME="your-username"
   export ALLSTACKS_PASSWORD="your-password"
   uvx allstacks-mcp --username "$ALLSTACKS_USERNAME" --password "$ALLSTACKS_PASSWORD"
   ```

3. **Never commit credentials** to version control
   - The MCP client config file may contain credentials
   - Keep config files in `.gitignore`

4. **Rotate credentials regularly** for enhanced security

#### Process Security

**Note**: Command-line arguments (`--username`, `--password`, `--token`) are visible in process lists, including when expanded from environment variables at launch. For production use:
- Restrict access to the host running the server so other users cannot read its process list
- Store credentials in a secure secrets manager and inject them only at launch time
- Use a dedicated Allstacks account or short-lived PAT that can be revoked quickly

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

### Running the Server Standalone

Bearer / PAT (recommended; required for SSO users):
```bash
uvx allstacks-mcp --token YOUR_PAT
```

Basic / username + password (local accounts only):
```bash
uvx allstacks-mcp --username YOUR_USERNAME --password YOUR_PASSWORD
```

**Command-line options:**
- `--token` or `-t`: Personal Access Token for Bearer auth (alternative to username/password)
- `--username` or `-u`: Username for HTTP Basic auth (paired with `--password`)
- `--password` or `-p`: Password for HTTP Basic auth (paired with `--username`)
- `--base-url` or `-b`: Override the default API base URL (default: `https://app.allstacks.com/api/v1/`)

Pass either `--token` OR both `--username` and `--password` — not both modes at once.

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop's `claude_desktop_config.json` or Claude Code's `mcp.json`).

**Recommended — PAT / Bearer auth (works for all users, including SSO):**
```json
{
    "mcpServers": {
        "allstacks": {
            "command": "uvx",
            "args": [
                "allstacks-mcp",
                "--token",
                "YOUR_PERSONAL_ACCESS_TOKEN",
                "--base-url",
                "https://app.allstacks.com/api/v1/"
            ]
        }
    }
}
```

**Alternative — Username + password (local accounts only):**
```json
{
    "mcpServers": {
        "allstacks": {
            "command": "uvx",
            "args": [
                "allstacks-mcp",
                "--username",
                "your-email@example.com",
                "--password",
                "your-password",
                "--base-url",
                "https://app.allstacks.com/api/v1/"
            ]
        }
    }
}
```

**Important Notes:**
- Replace `YOUR_PERSONAL_ACCESS_TOKEN` with your actual PAT from the Allstacks UI
- Or replace `your-email@example.com` and `your-password` with your credentials (local accounts only)
- The `--base-url` is optional (defaults to `https://app.allstacks.com/api/v1/`)
- `uvx` automatically installs and runs the latest version from PyPI — no manual installation needed!

> **Using a local clone for development?** See the [Local Development](#local-development) section for the configuration pattern.

## Features

### Comprehensive API Coverage

All tools are verified against the official Allstacks OpenAPI specification:
- ✅ All endpoints use correct paths and parameters
- ✅ Detailed parameter descriptions from official API docs
- ✅ Proper error handling and validation
- ✅ Authentication via Bearer token (PAT) or HTTP Basic
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

## Local Development

If you want to contribute to this project or run from a local clone instead of PyPI:

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/allstacks/allstacks-mcp-server.git
   cd allstacks-mcp-server
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

### Running from Local Clone

Bearer / PAT (recommended):
```bash
uv run python -m allstacks_mcp.server --token YOUR_PAT --base-url https://app.allstacks.com/api/v1/
```

Username + password (local accounts only):
```bash
uv run python -m allstacks_mcp.server --username YOUR_USERNAME --password YOUR_PASSWORD --base-url https://app.allstacks.com/api/v1/
```

### MCP Client Configuration (Local Clone)

For Claude Desktop or Claude Code, use this configuration pattern when working with a local clone:

```json
{
    "mcpServers": {
        "allstacks": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/allstacks-mcp-server",
                "run",
                "python",
                "-m",
                "allstacks_mcp.server",
                "--token",
                "YOUR_PAT",
                "--base-url",
                "https://app.allstacks.com/api/v1/"
            ]
        }
    }
}
```

Replace `/ABSOLUTE/PATH/TO/allstacks-mcp-server` with the full path to your cloned repository.

## Development

### Adding New Tools

1. Create or update a tool file in `allstacks_mcp/tools/`
2. Follow the existing pattern for tool registration
3. Include full docstrings with OpenAPI references
4. Add the module to `allstacks_mcp/tools/__init__.py`
5. Register it in `allstacks_mcp/server.py`'s `register_all_tools()` function

### Testing

When working on the codebase, run the server in development mode:

```bash
# From local clone with Bearer token
uv run python -m allstacks_mcp.server --token YOUR_PAT --base-url https://app.allstacks.com/api/v1/

# Or with a dev/staging environment
uv run python -m allstacks_mcp.server --token YOUR_PAT --base-url https://api-dev.allstacks.com/api/v1/
```

## License

MIT

## Support

For issues or questions about the Allstacks API, contact the Allstacks team.
For issues specific to this MCP server, please file an issue in the repository.
