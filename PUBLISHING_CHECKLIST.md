# Publishing Checklist for Allstacks MCP Server

## ✅ Completed (Ready for Publishing)

All preparatory work has been completed:

- ✅ **Security review completed** - No critical security issues found
- ✅ **server.json created** - MCP Registry configuration ready
- ✅ **pyproject.toml updated** - Added MCP name for verification
- ✅ **README updated** - Added security documentation and mcp-name identifier
- ✅ **GitHub Actions workflow created** - Automated publishing configured
- ✅ **server.json validated** - Confirmed valid JSON structure
- ✅ **SECURITY.md created** - Comprehensive security documentation
- ✅ **PUBLISHING.md created** - Detailed publishing guide

## 🚀 Next Steps (Required Actions)

You need to complete these steps to publish to the MCP Registry:

### 1. DNS Configuration (Required)

Since you're using the `com.allstacks/allstacks-mcp` namespace, you must set up DNS authentication:

```bash
# Generate Ed25519 keypair
openssl genpkey -algorithm Ed25519 -out mcp-key.pem

# Get the public key for DNS
echo "allstacks.com. IN TXT \"v=MCPv1; k=ed25519; p=$(openssl pkey -in mcp-key.pem -pubout -outform DER | tail -c 32 | base64)\""
```

**Action**: Add the generated TXT record to your DNS for `allstacks.com`

**Verify DNS**:
```bash
dig TXT allstacks.com +short
```

### 2. GitHub Repository Configuration

#### Add GitHub Secrets

Go to: Repository Settings → Secrets and variables → Actions

Add two secrets:

| Secret Name | Value | How to Get |
|------------|-------|------------|
| `PYPI_API_TOKEN` | Your PyPI API token | https://pypi.org/manage/account/token/ |
| `MCP_PRIVATE_KEY` | Contents of `mcp-key.pem` | Copy entire file contents |

**Important**: Keep `mcp-key.pem` secure - don't commit it!

### 3. PyPI Account Setup

1. Create account at https://pypi.org/ (if you don't have one)
2. Generate an API token: https://pypi.org/manage/account/token/
3. Add token to GitHub secrets (step 2 above)

### 4. First Manual Publish (Recommended)

Before enabling automated publishing, test manually:

```bash
# Install MCP publisher
brew install mcp-publisher
# OR download binary (see PUBLISHING.md)

# Build package
uv build

# Publish to PyPI
uv publish

# Authenticate with MCP Registry (convert PEM to hex and pass with --private-key)
PRIVATE_KEY_HEX=$(openssl pkey -in mcp-key.pem -outform DER | tail -c 32 | xxd -p -u -c 9999)
mcp-publisher login dns --domain allstacks.com --private-key $PRIVATE_KEY_HEX

# Publish to MCP Registry
mcp-publisher publish

# Verify
curl "https://registry.modelcontextprotocol.io/v0/servers?search=allstacks"
```

### 5. Automated Publishing (After Manual Success)

Once manual publishing works, future releases are automatic:

```bash
# Update versions in pyproject.toml and server.json
# Commit changes
git add .
git commit -m "Bump version to 0.2.0"

# Create and push tag
git tag v0.2.0
git push origin v0.2.0

# GitHub Actions will automatically publish!
```

## 📋 Pre-Publication Checklist

Before your first release:

- [ ] DNS TXT record added and verified
- [ ] GitHub secrets configured (`PYPI_API_TOKEN`, `MCP_PRIVATE_KEY`)
- [ ] PyPI account created and API token generated
- [ ] `mcp-key.pem` stored securely (not in git!)
- [ ] Tested server locally with `uv run server.py --username test --password test`
- [ ] Reviewed and understood SECURITY.md
- [ ] Updated README with any additional usage examples
- [ ] Decided on initial version number (recommend: 0.1.0)

## 🔍 Security Review Summary

### ✅ No Critical Issues Found

**Security Strengths**:
- Credentials passed via CLI args (not hardcoded)
- Uses HTTP Basic Auth with httpx
- No SQL injection risk (API wrapper only)
- Proper error handling
- No credential logging or storage

**🟡 Medium Risk Items** (documented in SECURITY.md):
- Command-line credentials visible in process lists
  - **Mitigation**: Documented environment variable usage
- AI assistants get full account access
  - **Mitigation**: Recommend dedicated service account

**Minor Code Issues**:
- `api_client` global initialization pattern (non-critical)
- Unused `argparse` import (cosmetic)

### Required Credentials

Users need three things:
1. **Username**: Allstacks username/email (required, not secret)
2. **Password**: Allstacks password or API key (required, SECRET)
3. **Base URL**: API endpoint (optional, default provided)

All documented in README.md with security best practices.

## 🔐 Base URL Configuration

Default: `https://api.allstacks.com/api/v1/`

Users can override with:
```bash
--base-url https://api-dev.allstacks.com/api/v1/
```

For MCP client config, they would set environment variable:
```json
{
  "mcpServers": {
    "allstacks": {
      "command": "uv",
      "args": ["--directory", "/path/to/allstacks-mcp", "run", "server.py"],
      "env": {
        "ALLSTACKS_USERNAME": "user@example.com",
        "ALLSTACKS_PASSWORD": "api-key-here",
        "ALLSTACKS_BASE_URL": "https://api.allstacks.com/api/v1/"
      }
    }
  }
}
```

## 📦 What's Been Created

### New Files
1. **`server.json`** - MCP Registry configuration
2. **`.github/workflows/publish-mcp.yml`** - GitHub Actions workflow
3. **`SECURITY.md`** - Comprehensive security documentation
4. **`PUBLISHING.md`** - Detailed publishing guide
5. **`PUBLISHING_CHECKLIST.md`** - This file

### Modified Files
1. **`README.md`** - Added security section and mcp-name identifier
2. **`pyproject.toml`** - Added `[tool.mcp]` section with name

## 🎯 Publishing Options

You have two options for registry namespace:

### Option 1: `com.allstacks/*` (Currently Configured)
- **Pros**: Professional, matches domain
- **Cons**: Requires DNS verification
- **Requirements**: Add TXT record to allstacks.com DNS

### Option 2: `io.github.username/*` (Alternative)
- **Pros**: Easier, only needs GitHub OAuth
- **Cons**: Less professional namespace
- **Requirements**: Just GitHub authentication

To switch to GitHub namespace:
1. Change `server.json`: `"name": "io.github.yourusername/allstacks-mcp"`
2. Change `pyproject.toml`: `name = "io.github.yourusername/allstacks-mcp"`
3. Change README comment: `<!-- mcp-name: io.github.yourusername/allstacks-mcp -->`
4. Update workflow to use: `mcp-publisher login github-oidc`

## 📞 Getting Help

If you run into issues:

1. **DNS Issues**: See PUBLISHING.md "Troubleshooting" section
2. **PyPI Issues**: Check https://pypi.org/help/
3. **MCP Registry**: https://github.com/modelcontextprotocol/registry/issues
4. **General**: Review PUBLISHING.md comprehensive guide

## 🎉 Success Criteria

You'll know publishing worked when:

1. ✅ Package appears on PyPI: https://pypi.org/project/allstacks-mcp/
2. ✅ Server appears in MCP Registry search
3. ✅ Users can install: `uv pip install allstacks-mcp`
4. ✅ Users can find in MCP clients (Claude Desktop, etc.)

## ⚡ Quick Start (TL;DR)

```bash
# 1. Generate DNS key
openssl genpkey -algorithm Ed25519 -out mcp-key.pem
# Add TXT record to allstacks.com DNS

# 2. Add GitHub secrets
# PYPI_API_TOKEN and MCP_PRIVATE_KEY

# 3. Publish
uv build
uv publish
# Convert PEM -> hex and login (mcp-publisher expects hex for the private key)
PRIVATE_KEY_HEX=$(openssl pkey -in mcp-key.pem -outform DER | tail -c 32 | xxd -p -u -c 9999)
mcp-publisher login dns --domain allstacks.com --private-key $PRIVATE_KEY_HEX
mcp-publisher publish

# 4. For future releases
git tag v0.2.0 && git push origin v0.2.0
```

---

**Created**: October 27, 2025  
**Status**: Ready for Publishing  
**Next Action**: DNS Configuration

