# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in this MCP server, please report it to:
- **Email**: security@allstacks.com (or your appropriate contact)
- **GitHub**: Open a security advisory at https://github.com/allstacks/allstacks-mcp/security/advisories

Please do NOT report security vulnerabilities through public GitHub issues.

## Security Considerations

### Authentication & Credentials

This MCP server uses HTTP Basic Authentication to connect to the Allstacks API.

#### Credential Storage Risks

**⚠️ Command-Line Exposure**
- Credentials passed via `--username` and `--password` are visible in process lists
- Shell history may contain credentials
- **Mitigation**: Use environment variables or configuration files

**✅ Recommended Approaches**
1. Environment variables (preferred for production)
2. Secure configuration files with restricted permissions
3. Secrets management systems (e.g., AWS Secrets Manager, HashiCorp Vault)

#### API Key Management

- **Use API keys** instead of passwords when possible
- Generate keys from Allstacks account settings
- Rotate keys regularly (recommended: every 90 days)
- Revoke compromised keys immediately
- Use separate keys for different environments (dev, staging, prod)

### Data Access & Privacy

#### What This Server Does

- ✅ Passes requests directly to Allstacks API
- ✅ Returns API responses without modification
- ✅ No credential storage or logging
- ✅ No data persistence
- ✅ No caching of sensitive data

#### What This Server Does NOT Do

- ❌ Does not store credentials on disk
- ❌ Does not log API requests/responses
- ❌ Does not cache user data
- ❌ Does not modify or filter API responses
- ❌ Does not transmit data to third parties

### AI Assistant Access

When using this MCP server with AI assistants:

**The AI will have**:
- Full access to all data accessible via your credentials
- Same permissions as your Allstacks user account
- Ability to read, create, modify, and delete resources

**Security Recommendations**:
1. Create a dedicated Allstacks account for AI use
2. Apply principle of least privilege
3. Limit permissions to only what's needed
4. Monitor API usage and audit logs
5. Review AI-generated changes before applying
6. Use read-only API keys when possible

### Network Security

#### TLS/HTTPS
- All API communication uses HTTPS
- Default Allstacks API endpoint: `https://api.allstacks.com/api/v1/`
- Certificate validation is enforced by httpx library

#### Timeouts
- HTTP requests timeout after 30 seconds
- Prevents hung connections and resource exhaustion

### Input Validation

#### JSON Parsing
- All JSON inputs are validated using `json.loads()`
- Invalid JSON returns error messages (does not crash)
- No code execution from user input

#### Parameter Validation
- Type hints enforce parameter types
- MCP framework validates tool parameters
- No SQL injection risk (no direct database access)
- No XSS risk (server-to-server communication only)

### Dependencies

This server has minimal dependencies:
- `httpx` - HTTP client (actively maintained, secure)
- `mcp` - Model Context Protocol SDK
- `argparse` - Standard library

**Security Updates**:
- Monitor dependencies for security advisories
- Update dependencies regularly using `uv sync --upgrade`
- Review SECURITY.md in dependency repositories

### Rate Limiting

- No client-side rate limiting implemented
- Relies on Allstacks API rate limits
- httpx timeout prevents request flooding

### Error Handling

- HTTP errors are caught and returned as JSON
- No stack traces exposed to end users
- Error messages do not leak sensitive information
- Credentials never included in error responses

## Security Checklist for Deployment

- [ ] Use environment variables for credentials
- [ ] Use API keys instead of passwords
- [ ] Set up credential rotation schedule
- [ ] Create dedicated service account for AI access
- [ ] Apply least-privilege permissions
- [ ] Monitor API usage and audit logs
- [ ] Keep dependencies up to date
- [ ] Review security advisories regularly
- [ ] Test with read-only credentials first
- [ ] Document incident response procedures

## Compliance Considerations

### Data Residency
- Data flows through: AI Client → MCP Server → Allstacks API
- No data stored or cached by this server
- Allstacks API data residency policies apply

### Audit Logging
- This server does not perform logging
- Use Allstacks API audit logs for tracking
- AI assistant may log interactions (check AI provider policies)

### Access Control
- Authentication handled by Allstacks API
- Authorization determined by Allstacks user permissions
- No additional access control layer in this server

## Vulnerability Disclosure Timeline

1. **Report received**: Acknowledged within 48 hours
2. **Initial assessment**: Within 7 days
3. **Fix developed**: Timeframe depends on severity
4. **Fix released**: Security patches released ASAP
5. **Public disclosure**: 90 days after fix or earlier if actively exploited

## Security Best Practices for Users

### During Development
- Use test/development Allstacks accounts
- Never use production credentials in development
- Review all AI-generated API calls before execution

### In Production
- Use environment variables for all secrets
- Implement secrets rotation
- Monitor API usage patterns
- Set up alerting for unusual activity
- Regular security audits

### For Organizations
- Establish MCP server usage policies
- Require security training for users
- Implement access reviews
- Maintain inventory of API keys
- Document security incidents

## Contact

For security concerns or questions:
- Security Email: security@allstacks.com
- GitHub Security Advisories: https://github.com/allstacks/allstacks-mcp/security

---

**Last Updated**: October 27, 2025  
**Version**: 0.1.0

