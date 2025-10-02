#!/bin/bash

# Build script for creating allstacks-mcp bundle
# This script packages the MCP server for distribution

set -e  # Exit on error

echo "🚀 Building allstacks-mcp bundle..."

# Configuration
BUNDLE_NAME="allstacks-mcp"
VERSION="1.0.0"
BUILD_DIR="dist"
BUNDLE_DIR="$BUILD_DIR/$BUNDLE_NAME"

# Clean previous builds
echo "📦 Cleaning previous builds..."
rm -rf $BUILD_DIR/
mkdir -p $BUILD_DIR/

# Create bundle directory structure
echo "📁 Creating bundle directory..."
mkdir -p $BUNDLE_DIR

# Copy Python source files
echo "📝 Copying source files..."
if [ -d "allstacks_mcp" ]; then
    cp -r allstacks_mcp/ $BUNDLE_DIR/
fi

# Copy main server file
if [ -f "server.py" ]; then
    cp server.py $BUNDLE_DIR/
fi

# Copy configuration files
echo "📋 Copying configuration files..."
[ -f "README.md" ] && cp README.md $BUNDLE_DIR/
[ -f ".gitignore" ] && cp .gitignore $BUNDLE_DIR/
[ -f ".python-version" ] && cp .python-version $BUNDLE_DIR/
[ -f "pyproject.toml" ] && cp pyproject.toml $BUNDLE_DIR/
[ -f "uv.lock" ] && cp uv.lock $BUNDLE_DIR/

# Generate requirements.txt from pyproject.toml
echo "📝 Generating requirements.txt..."
cat > $BUNDLE_DIR/requirements.txt <<EOF
# Allstacks MCP Server Requirements
argparse>=1.4.0
httpx>=0.28.1
mcp[cli]>=1.7.1
EOF

# Create mcp.json
echo "⚙️ Creating mcp.json..."
cat > $BUNDLE_DIR/mcp.json <<EOF
{
  "name": "$BUNDLE_NAME",
  "version": "$VERSION",
  "description": "MCP Server for Allstacks API - 79 tools across 14 categories for engineering intelligence",
  "author": "Jeremy Freeman",
  "license": "MIT",
  "runtime": "python",
  "main": "server.py",
  "commands": {
    "start": "uv run server.py"
  },
  "categories": [
    "Metrics Data Retrieval (7 tools)",
    "Service Items & Filtering (6 tools)",
    "User & Team Management (4 tools)",
    "Organization & Projects (4 tools)",
    "AI & Analytics (4 tools)",
    "Dashboards & Widgets (5 tools)",
    "Employee & Productivity (5 tools)",
    "Forecasting & Planning (5 tools)",
    "Labels & Tagging (5 tools)",
    "Alerts & Monitoring (5 tools)",
    "Portfolio & Deliverables (5 tools)",
    "Milestones & Pinned Milestones (6 tools)",
    "Attainment & Goals (7 tools)",
    "Portfolio Analytics (7 tools)"
  ],
  "requirements": {
    "python": ">=3.13",
    "uv": "recommended"
  },
  "authentication": {
    "type": "http-basic",
    "required": ["username", "password"]
  },
  "capabilities": {
    "tools": 79,
    "resources": false,
    "prompts": false
  }
}
EOF

# Create package.json
echo "📦 Creating package.json..."
cat > $BUNDLE_DIR/package.json <<EOF
{
  "name": "@allstacks/mcp-server",
  "version": "$VERSION",
  "description": "MCP Server for Allstacks Analytics - 79 AI-native engineering intelligence tools",
  "author": "Jeremy Freeman",
  "license": "MIT",
  "keywords": [
    "mcp",
    "allstacks",
    "analytics",
    "engineering-intelligence",
    "metrics",
    "portfolio-management",
    "okr",
    "devex"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/allstacks/allstacks-mcp.git"
  },
  "mcp": {
    "type": "python",
    "runtime": "python3",
    "entry": "server.py",
    "manager": "uv"
  }
}
EOF

# Create setup script for easy installation
echo "🔧 Creating setup script..."
cat > $BUNDLE_DIR/setup.sh <<'SETUPEOF'
#!/bin/bash

echo "🚀 Setting up allstacks-mcp server..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
required_version="3.13"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "⚠️  Warning: Python 3.13 or higher is recommended (found $python_version)"
fi

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✅ Found uv package manager"
    echo "📦 Installing dependencies with uv..."
    uv sync
else
    echo "⚠️  uv not found, falling back to pip"
    echo "💡 For better performance, install uv: https://docs.astral.sh/uv/"
    echo "📦 Installing dependencies with pip..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Set your credentials as command-line arguments:"
echo "   --username YOUR_USERNAME --password YOUR_PASSWORD"
echo ""
echo "2. Run the server:"
echo "   uv run server.py --username YOUR_USERNAME --password YOUR_PASSWORD"
echo "   # or with pip:"
echo "   python server.py --username YOUR_USERNAME --password YOUR_PASSWORD"
echo ""
echo "3. Configure in Claude Desktop (see INSTALL.md for details)"
SETUPEOF

chmod +x $BUNDLE_DIR/setup.sh

# Create installation instructions
echo "📚 Creating installation instructions..."
cat > $BUNDLE_DIR/INSTALL.md <<'INSTALLEOF'
# Allstacks MCP Server Installation Guide

## Quick Start

### 1. Extract the Bundle

**Mac/Linux:**
```bash
tar -xzf allstacks-mcp-1.0.0.mcpb
cd allstacks-mcp/
```

**Windows:**
```bash
unzip allstacks-mcp-1.0.0.zip
cd allstacks-mcp/
```

### 2. Run Setup

```bash
./setup.sh
```

Or manually install dependencies:
```bash
# Using uv (recommended)
uv sync

# Using pip
pip install -r requirements.txt
```

### 3. Test the Server

```bash
uv run server.py --username YOUR_USERNAME --password YOUR_PASSWORD
# or
python server.py --username YOUR_USERNAME --password YOUR_PASSWORD
```

## Claude Desktop Configuration

Add to your Claude Desktop config file:

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "allstacks": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/allstacks-mcp",
        "run",
        "server.py",
        "--username",
        "YOUR_ALLSTACKS_USERNAME",
        "--password",
        "YOUR_ALLSTACKS_PASSWORD"
      ]
    }
  }
}
```

**Note:** Replace:
- `/Users/YOUR_USERNAME/.local/bin/uv` with output of `which uv`
- `/ABSOLUTE/PATH/TO/allstacks-mcp` with the full path to this directory
- `YOUR_ALLSTACKS_USERNAME` with your Allstacks username
- `YOUR_ALLSTACKS_PASSWORD` with your Allstacks password or API key

### Alternative: Using Python directly

```json
{
  "mcpServers": {
    "allstacks": {
      "command": "/ABSOLUTE/PATH/TO/allstacks-mcp/.venv/bin/python",
      "args": [
        "server.py",
        "--username",
        "YOUR_ALLSTACKS_USERNAME",
        "--password",
        "YOUR_ALLSTACKS_PASSWORD"
      ],
      "cwd": "/ABSOLUTE/PATH/TO/allstacks-mcp"
    }
  }
}
```

### Optional: Custom Base URL

If you need a different API endpoint:

```bash
uv run server.py \
  --username YOUR_USERNAME \
  --password YOUR_PASSWORD \
  --base-url https://custom-api.allstacks.com/api/v1/
```

## Available Tools (79 Total)

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

### 11. Portfolio & Deliverables (5 tools)
- `list_portfolios` - List all portfolios
- `get_portfolio_details` - Get portfolio details
- `create_portfolio` - Create new portfolio
- `list_deliverables` - List project deliverables
- `get_deliverable_status` - Get deliverable status

### 12. Milestones & Pinned Milestones (6 tools)
- `list_milestones` - List all milestones
- `get_pinned_milestones` - Get pinned milestones
- `pin_milestone` - Pin a milestone
- `unpin_milestone` - Unpin a milestone
- `get_milestone_report` - Generate milestone report
- `create_milestone` - Create new milestone

### 13. Attainment & Goals (7 tools)
- `get_attainment_metrics` - Get attainment metrics for OKRs
- `list_attainment_goals` - List attainment goals
- `create_attainment_goal` - Create new attainment goal
- `get_attainment_progress` - Get goal progress tracking
- `get_attainment_widget_data` - Get attainment widget data
- `create_attainment_widget` - Create attainment widget
- `get_attainment_report` - Generate attainment report

### 14. Portfolio Analytics (7 tools)
- `get_portfolio_health` - Get portfolio health metrics
- `get_portfolio_timeline` - Get portfolio timeline view
- `get_portfolio_allocation` - Get resource allocation
- `get_portfolio_dependencies` - Get dependency map
- `compare_portfolios` - Compare multiple portfolios
- `get_portfolio_forecast` - Get portfolio forecast
- `export_portfolio_report` - Export portfolio report

## Troubleshooting

### "spawn uv ENOENT" Error in Claude Desktop

This means Claude Desktop can't find the `uv` command. Use the full path:

```bash
which uv  # Get the full path (e.g., /Users/username/.local/bin/uv)
```

Then use that path in your `claude_desktop_config.json`.

### Import Errors

Make sure you've run the setup script or installed dependencies:

```bash
./setup.sh
# or
uv sync
# or
pip install -r requirements.txt
```

### Authentication Errors

- Verify your username and password are correct
- Check if you need to use an API key instead of password
- Ensure you have network access to the Allstacks API

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Contact your Allstacks administrator
- File an issue in the project repository

## Version

Allstacks MCP Server v1.0.0
- 79 tools across 14 categories
- HTTP Basic Authentication
- Python 3.13+ recommended
INSTALLEOF

# Create the .mcpb archive
echo "📦 Creating MCPB archive..."
cd $BUILD_DIR/
tar -czf $BUNDLE_NAME-$VERSION.mcpb $BUNDLE_NAME/
cd ..

# Create a zip alternative for Windows users
echo "📦 Creating ZIP archive for Windows..."
cd $BUILD_DIR/
zip -r -q $BUNDLE_NAME-$VERSION.zip $BUNDLE_NAME/
cd ..

# Calculate file sizes
MCPB_SIZE=$(du -h $BUILD_DIR/$BUNDLE_NAME-$VERSION.mcpb | cut -f1)
ZIP_SIZE=$(du -h $BUILD_DIR/$BUNDLE_NAME-$VERSION.zip | cut -f1)

# Summary
echo ""
echo "✅ Build complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 MCPB Bundle:  $BUILD_DIR/$BUNDLE_NAME-$VERSION.mcpb ($MCPB_SIZE)"
echo "📦 ZIP Archive:  $BUILD_DIR/$BUNDLE_NAME-$VERSION.zip ($ZIP_SIZE)"
echo "📁 Source Dir:   $BUILD_DIR/$BUNDLE_NAME/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📤 Distribution Files:"
echo "   • $BUNDLE_NAME-$VERSION.mcpb - for Mac/Linux users"
echo "   • $BUNDLE_NAME-$VERSION.zip - for Windows users"
echo "   • Include INSTALL.md for setup instructions"
echo ""
echo "🧪 Test the bundle locally:"
echo "   cd $BUILD_DIR && tar -xzf $BUNDLE_NAME-$VERSION.mcpb"
echo "   cd $BUNDLE_NAME && ./setup.sh"
echo "   uv run server.py --username test --password test"
echo ""
echo "📋 Files included in bundle:"
echo "   ✓ allstacks_mcp/ (source code)"
echo "   ✓ server.py (entry point)"
echo "   ✓ requirements.txt"
echo "   ✓ pyproject.toml & uv.lock"
echo "   ✓ README.md & INSTALL.md"
echo "   ✓ mcp.json & package.json"
echo "   ✓ setup.sh (automated setup)"
echo ""

