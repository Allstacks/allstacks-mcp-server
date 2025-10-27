# Publishing Guide

This document explains how to publish the Allstacks MCP Server to the MCP Registry and PyPI.

## Prerequisites

### 1. DNS Authentication Setup (Required for com.allstacks/* namespace)

Since we're using the `com.allstacks/allstacks-mcp` namespace, you need DNS-based authentication:

#### Generate Ed25519 Keypair

```bash
# Generate private key
openssl genpkey -algorithm Ed25519 -out mcp-key.pem

# Extract public key for DNS
echo "allstacks.com. IN TXT \"v=MCPv1; k=ed25519; p=$(openssl pkey -in mcp-key.pem -pubout -outform DER | tail -c 32 | base64)\""
```

#### Add DNS TXT Record

Add the generated TXT record to your DNS configuration for `allstacks.com`:

```
allstacks.com. IN TXT "v=MCPv1; k=ed25519; p=<BASE64_PUBLIC_KEY>"
```

**DNS Provider Examples:**
- **Cloudflare**: DNS → Records → Add TXT record
- **Route 53**: Hosted zones → Create record → TXT type
- **Google Cloud DNS**: DNS → Add record → TXT type

#### Test DNS Verification

```bash
dig TXT allstacks.com +short
# Should show your MCP TXT record
```

### 2. PyPI Setup

#### Create PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token with project scope (after first upload)
3. Save the token securely

#### Add to GitHub Secrets

Add `PYPI_API_TOKEN` to repository secrets:
- Go to repository Settings → Secrets and variables → Actions
- Add new repository secret: `PYPI_API_TOKEN`

### 3. GitHub Repository Setup

#### Required Secrets

Add these secrets to your GitHub repository:

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `PYPI_API_TOKEN` | PyPI publishing token | From https://pypi.org/manage/account/token/ |
| `MCP_PRIVATE_KEY` | Ed25519 private key for DNS auth | Contents of `mcp-key.pem` file |

**Important**: Store `mcp-key.pem` securely and never commit it to version control!

## Manual Publishing (First Time)

For the first release, you may want to publish manually to ensure everything works:

### 1. Install MCP Publisher CLI

```bash
# macOS/Linux with Homebrew
brew install mcp-publisher

# Or download binary
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher
sudo mv mcp-publisher /usr/local/bin/
```

### 2. Update Version

Update version in three places:
1. `pyproject.toml`: `version = "0.1.0"`
2. `server.json`: `"version": "0.1.0"`
3. `server.json`: `"packages"[0]."version": "0.1.0"`

### 3. Build and Publish to PyPI

```bash
# Build package
uv build

# Publish to PyPI
uv publish
```

### 4. Authenticate with MCP Registry

```bash
# DNS authentication
mcp-publisher login dns --domain allstacks.com --private-key-file mcp-key.pem
```

### 5. Publish to MCP Registry

```bash
mcp-publisher publish
```

### 6. Verify Publication

```bash
# Check MCP Registry
curl "https://registry.modelcontextprotocol.io/v0/servers?search=allstacks"

# Check PyPI
curl "https://pypi.org/pypi/allstacks-mcp/json"
```

## Automated Publishing with GitHub Actions

Once secrets are configured, publishing is automatic:

### Release Process

```bash
# Update version numbers in pyproject.toml and server.json
# Commit changes
git add pyproject.toml server.json
git commit -m "Bump version to 0.2.0"

# Create and push tag
git tag v0.2.0
git push origin v0.2.0
```

The GitHub Actions workflow will automatically:
1. ✅ Build the Python package
2. ✅ Publish to PyPI
3. ✅ Update server.json version
4. ✅ Authenticate with MCP Registry
5. ✅ Publish to MCP Registry

### Monitoring the Workflow

- View workflow runs: https://github.com/allstacks/allstacks-mcp/actions
- Check workflow logs for errors
- Verify PyPI publication: https://pypi.org/project/allstacks-mcp/
- Verify MCP Registry: Search for "allstacks" in MCP clients

## Versioning Strategy

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking API changes
- **MINOR** (0.2.0): New features, backward compatible
- **PATCH** (0.1.1): Bug fixes, backward compatible

### Version Update Checklist

- [ ] Update `pyproject.toml` version
- [ ] Update `server.json` version (2 places)
- [ ] Update CHANGELOG.md (if you have one)
- [ ] Commit version bump
- [ ] Create git tag: `git tag v0.x.y`
- [ ] Push tag: `git push origin v0.x.y`

## Troubleshooting

### DNS Authentication Fails

**Symptoms**: `mcp-publisher login dns` fails with "DNS verification failed"

**Solutions**:
1. Wait for DNS propagation (can take up to 48 hours)
2. Verify TXT record: `dig TXT allstacks.com +short`
3. Check public key format (must be base64 encoded)
4. Ensure TXT record format: `v=MCPv1; k=ed25519; p=<base64>`

### PyPI Publishing Fails

**Symptoms**: `uv publish` fails with authentication error

**Solutions**:
1. Verify PYPI_API_TOKEN is set correctly in GitHub secrets
2. Check token has correct project scope
3. For first upload, use token with "Upload packages" scope
4. After first upload, create project-scoped token

### Package Validation Fails

**Symptoms**: MCP Registry rejects publication with "Package validation failed"

**Solutions**:
1. Verify README contains: `<!-- mcp-name: com.allstacks/allstacks-mcp -->`
2. Check package is published to PyPI first
3. Wait a few minutes after PyPI publication
4. Verify identifier in server.json matches PyPI package name

### GitHub Actions Workflow Fails

**Symptoms**: Workflow fails at publish steps

**Solutions**:
1. Check secrets are configured: Settings → Secrets → Actions
2. Verify `MCP_PRIVATE_KEY` is the raw Ed25519 private key (starts with `-----BEGIN PRIVATE KEY-----`)
3. Check workflow logs for specific error messages
4. Ensure Python 3.13+ is available

## Version Management

### Pre-release Versions

For testing before official release:

```bash
# Update to pre-release version
# pyproject.toml: version = "0.2.0-beta.1"
# server.json: "version": "0.2.0-beta.1"

git tag v0.2.0-beta.1
git push origin v0.2.0-beta.1
```

### Yanking a Release

If you need to remove a broken release from PyPI:

```bash
pip install twine
twine yank allstacks-mcp==0.1.0 -m "Reason for yanking"
```

**Note**: Yanked releases are still installable if explicitly specified, but not suggested to users.

## Post-Publication Checklist

After publishing a new version:

- [ ] Verify on PyPI: https://pypi.org/project/allstacks-mcp/
- [ ] Verify in MCP Registry search
- [ ] Test installation: `uv pip install allstacks-mcp`
- [ ] Update documentation if needed
- [ ] Announce release (if applicable)
- [ ] Monitor for issues

## Security Considerations

### Key Management

- **Never commit** `mcp-key.pem` to version control
- Store private key securely (password manager, secrets vault)
- Rotate keys annually
- Use separate keys for different environments if needed

### Secrets Rotation

To rotate MCP authentication:

```bash
# Generate new keypair
openssl genpkey -algorithm Ed25519 -out mcp-key-new.pem

# Update DNS TXT record with new public key
# Update MCP_PRIVATE_KEY secret in GitHub

# Test with new key
mcp-publisher login dns --domain allstacks.com --private-key-file mcp-key-new.pem

# Once verified, delete old key
rm mcp-key.pem
mv mcp-key-new.pem mcp-key.pem
```

## Resources

- **MCP Publishing Docs**: https://modelcontextprotocol.io/docs/publishing
- **PyPI Publishing**: https://packaging.python.org/tutorials/packaging-projects/
- **uv Documentation**: https://docs.astral.sh/uv/
- **GitHub Actions**: https://docs.github.com/en/actions

## Support

For publishing issues:
- MCP Registry: https://github.com/modelcontextprotocol/registry/issues
- PyPI: https://github.com/pypi/support/issues
- This project: https://github.com/allstacks/allstacks-mcp/issues

---

**Last Updated**: October 27, 2025  
**Version**: 0.1.0

