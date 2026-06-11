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

# Copy or create mcp.json
if [ -f "mcp.json" ]; then
    echo "⚙️ Copying mcp.json..."
    cp mcp.json $BUNDLE_DIR/
else
    echo "⚙️ Creating mcp.json..."
    cat > $BUNDLE_DIR/mcp.json <<EOF
{
  "name": "$BUNDLE_NAME",
  "version": "$VERSION",
  "description": "MCP Server for Allstacks Analytics",
  "author": "Jeremy Freeman",
  "license": "MIT",
  "runtime": "python",
  "main": "server.py"
}
EOF
fi

# Copy or create package.json
if [ -f "package.json" ]; then
    echo "📦 Copying package.json..."
    cp package.json $BUNDLE_DIR/
else
    echo "📦 Creating package.json..."
    cat > $BUNDLE_DIR/package.json <<EOF
{
  "name": "@allstacks/$BUNDLE_NAME",
  "version": "$VERSION",
  "description": "MCP Server for Allstacks Analytics",
  "author": "Jeremy Freeman",
  "license": "MIT",
  "mcp": {
    "type": "python",
    "runtime": "python3",
    "entry": "server.py"
  }
}
EOF
fi

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

## Available Tools (170 Total)

Refer to the canonical catalog in `README.md` (Tool Categories) and runtime
discovery (`list_tool_categories`) for the current 13-category tool map.

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
- 170 tools across 13 categories
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

