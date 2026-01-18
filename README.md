# Kali Security MCP Server for Claude Desktop - Enhanced v2.0

A comprehensive Model Context Protocol (MCP) server that integrates Kali Linux security tools with Claude Desktop for educational penetration testing, now with enhanced security features.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/)
[![WSL2](https://img.shields.io/badge/WSL2-Required-green.svg)](https://docs.microsoft.com/en-us/windows/wsl/)
[![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)](https://github.com/yourusername/kali-mcp-server)

## ⚠️ Legal Disclaimer

**EDUCATIONAL USE ONLY**

This tool is for educational purposes and authorized security testing only. Unauthorized penetration testing is **ILLEGAL** in most jurisdictions.

- ✅ Only test systems you **own**
- ✅ Get **written permission** before testing any system
- ✅ Follow responsible disclosure practices
- ❌ **Never** scan unauthorized systems

**Violations can result in criminal prosecution under computer fraud laws (CFAA, Computer Misuse Act, etc.)**

---

## 🆕 What's New in v2.0

### Security Enhancements
- ✅ **Input Validation**: Comprehensive validation for all inputs (IP, URLs, options)
- ✅ **Rate Limiting**: 10 scans per hour per tool to prevent abuse
- ✅ **Private Network Blocking**: Automatic blocking of private IP ranges
- ✅ **Audit Logging**: Complete audit trail of all scan activities
- ✅ **Output Sanitization**: Automatic redaction of credentials and sensitive data
- ✅ **Options Whitelisting**: Only allowed nmap and tool options can be used
- ✅ **Result Caching**: 1-hour cache to reduce redundant scans

### New Features
- 📊 **Scan Statistics**: View usage statistics and remaining quota
- 🗑️ **Cache Management**: Clear cached results on demand
- 🔒 **Safe Command Execution**: Replaced dangerous `run_custom_command` with `run_safe_command`
- ⚙️ **Configuration File**: YAML-based configuration for easy customization
- 🐳 **Docker Compose**: Better resource management and deployment
- 📈 **Resource Limits**: CPU and memory limits to prevent system overload

### Improved Tools
- All tools now have comprehensive error handling
- Better timeout management with environment variable support
- Improved output formatting and readability
- Cache support for faster repeated scans

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Security Features](#security-features)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Security Scanning Tools
- **nmap** - Network port scanning with version detection
- **Nikto** - Web server vulnerability scanning
- **SQLMap** - SQL injection detection and exploitation
- **WPScan** - WordPress vulnerability scanning
- **dirb** - Web directory brute forcing
- **searchsploit** - Exploit database searching

### Package Management
- **apt_install** - Install security tools dynamically
- **apt_search** - Search for available packages
- **list_installed_tools** - View currently installed tools

### Git Integration
- **git_clone** - Clone security tool repositories
- **git_pull** - Update cloned repositories

### System Management
- **run_safe_command** - Execute whitelisted read-only commands
- **get_scan_statistics** - View scan usage and quota
- **clear_cache** - Clear cached scan results

### Security Features
- **Input Validation** - All inputs validated before execution
- **Rate Limiting** - Prevent scan abuse (10/hour per tool)
- **Audit Logging** - Complete activity logs in `/var/log/mcp_audit.log`
- **Result Caching** - Reduce redundant scans (1-hour TTL)
- **Private IP Blocking** - Automatic blocking of internal networks
- **Output Sanitization** - Automatic credential redaction

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose |
|----------|----------------|---------|
| Windows | 10/11 | Host operating system |
| WSL2 | Latest | Linux subsystem |
| Docker Desktop | Latest | Container runtime |
| Claude Desktop | 0.7.0+ | MCP client |

### System Requirements
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **Network**: Internet connection for package downloads

---

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/kali-mcp-server.git
cd kali-mcp-server

# 2. Build Docker image (in WSL)
docker build -t kali-security-mcp-server .

# OR use docker-compose
docker-compose build

# 3. Configure Claude Desktop (in PowerShell)
.\setup-windows.ps1

# 4. Restart Claude Desktop

# 5. Test in Claude
"List all available security tools"
"Show scan statistics"
```

---

## Installation

### Step 1: Install Prerequisites

#### Install WSL2
```powershell
# Run as Administrator in PowerShell
wsl --install
# Restart computer
```

#### Install Docker Desktop
1. Download from [docker.com](https://www.docker.com/products/docker-desktop)
2. Install with WSL2 backend enabled
3. Start Docker Desktop

### Step 2: Clone and Build

```bash
# In WSL terminal
git clone https://github.com/yourusername/kali-mcp-server.git
cd kali-mcp-server

# Build with docker-compose (recommended)
docker-compose build

# OR build manually
docker build -t kali-security-mcp-server .
```

### Step 3: Configure Claude Desktop

```powershell
# In PowerShell
cd C:\path\to\kali-mcp-server
.\setup-windows.ps1
```

Or manually edit:
```
C:\Users\USERNAME\AppData\Roaming\Claude\claude_desktop_config.json
```

### Step 4: Restart Claude Desktop

Fully quit and restart Claude Desktop. Look for the 🔨 hammer icon.

---

## Configuration

### config.yaml

The server now uses a YAML configuration file for easy customization:

```yaml
security:
  max_scans_per_hour: 10
  max_target_length: 255
  blocked_ranges:
    - "10.0.0.0/8"
    - "192.168.0.0/16"

timeouts:
  nmap: 600
  nikto: 600
  default: 300

cache:
  enabled: true
  ttl: 3600
```

### Environment Variables

Set these in docker-compose.yml or via docker run:

- `NMAP_TIMEOUT` - Nmap scan timeout (default: 600)
- `NIKTO_TIMEOUT` - Nikto scan timeout (default: 600)
- `SQLMAP_TIMEOUT` - SQLMap scan timeout (default: 600)
- `DEFAULT_TIMEOUT` - Default timeout for other tools (default: 300)

---

## Available Tools

### Network Scanning

#### nmap_scan
```
"Scan scanme.nmap.org for open ports"
```

**Features:**
- Input validation (IP/domain)
- Option whitelisting
- Result caching
- Rate limiting
- Audit logging

#### quick_recon
```
"Perform quick reconnaissance on scanme.nmap.org"
```

Fast reconnaissance with nmap -F.

### Web Vulnerability Scanning

#### nikto_scan
```
"Scan http://testphp.vulnweb.com with Nikto"
```

#### dirb_scan
```
"Brute force directories on http://testphp.vulnweb.com"
```

#### wpscan_scan
```
"Check http://example.com/wordpress for vulnerabilities"
```

### SQL Injection Testing

#### sqlmap_scan
```
"Test http://testphp.vulnweb.com/listproducts.php?cat=1 for SQL injection"
```

### System Management

#### run_safe_command
```
"Run: ls -la /usr/share/wordlists"
```

**Allowed commands:** ls, pwd, whoami, id, uname, cat, grep, find, head, tail

#### get_scan_statistics
```
"Show my scan statistics"
```

View remaining quota and usage.

#### clear_cache
```
"Clear all cached results"
```

---

## Security Features

### 1. Input Validation

All inputs are validated before execution:

```python
# IP/Domain validation
target = validate_target("192.168.1.1", "ip")

# URL validation
target = validate_target("http://example.com", "url")
```

### 2. Rate Limiting

Maximum 10 scans per hour per tool:

```python
if not check_rate_limit("nmap"):
    return "ERROR: Rate limit exceeded"
```

### 3. Private Network Blocking

Automatic blocking of private IP ranges:

- 10.0.0.0/8
- 172.16.0.0/12
- 192.168.0.0/16
- 127.0.0.0/8
- 169.254.0.0/16

### 4. Audit Logging

All scan activities logged to `/var/log/mcp_audit.log`:

```json
{
  "timestamp": "2025-12-24T10:30:00Z",
  "tool": "nmap",
  "target": "scanme.nmap.org",
  "success": true,
  "details": "options: -sV -sC"
}
```

### 5. Output Sanitization

Automatic redaction of sensitive data:

```python
output = sanitize_output(output)
# Redacts: passwords, API keys, tokens, paths
```

### 6. Result Caching

1-hour cache reduces redundant scans:

```python
cache_key = get_cache_key("nmap", target, options)
cached = get_cached_result(cache_key)
```

---

## Usage Examples

### Example 1: Basic Network Scan with Caching

```
User: "Scan scanme.nmap.org"

Claude: I'll scan scanme.nmap.org for you.

[First scan - takes 30 seconds]
Results: [scan output]

User: "Scan scanme.nmap.org again"

Claude: I'll scan scanme.nmap.org for you.

[CACHED RESULT - instant]
Results: [same output from cache]
```

### Example 2: Rate Limit Protection

```
User: [After 10 scans] "Scan another target"

Claude: ERROR: Rate limit exceeded. Maximum 10 scans per hour.

You can check your quota with: "Show scan statistics"
```

### Example 3: Private Network Protection

```
User: "Scan 192.168.1.1"

Claude: ERROR: Target 192.168.1.1 is in blocked range 192.168.0.0/16

Private network scanning is not allowed for security reasons.
```

### Example 4: Safe Command Execution

```
User: "Run: ls /usr/share/wordlists"

Claude: [Executes safely]
[INSTALLED] common.txt
[INSTALLED] rockyou.txt

User: "Run: rm -rf /"

Claude: ERROR: Command 'rm' is not allowed.

Allowed commands: ls, pwd, whoami, id, uname, cat, grep, find, head, tail
```

### Example 5: Scan Statistics

```
User: "Show my scan statistics"

Claude:
Scan Statistics (Last Hour)
============================================================

nmap:
  - Scans used: 3/10
  - Remaining: 7

nikto:
  - Scans used: 1/10
  - Remaining: 9

Total scans: 4
Rate Limit: 10 scans per hour per tool
```

---

## Troubleshooting

### Issue: "Rate limit exceeded"

**Solution**: Wait one hour or clear old scans:
```
docker restart kali-security-mcp
```

### Issue: "Target is in blocked range"

**Solution**: Only scan public IP addresses or use authorized domains like `scanme.nmap.org` or `testphp.vulnweb.com`.

### Issue: Cache showing old results

**Solution**: Clear cache:
```
"Clear all cached results"
```

### Issue: Audit log filling up disk

**Solution**: Rotate logs:
```bash
# In WSL
docker exec kali-security-mcp truncate -s 0 /var/log/mcp_audit.log
```

---

## Project Structure

```
kali-mcp-server/
├── Dockerfile                    # Enhanced container definition
├── docker-compose.yml            # Resource management (NEW)
├── requirements.txt              # Python dependencies
├── config.yaml                   # Configuration file (NEW)
├── kali_security_server.py       # Enhanced MCP server
├── setup-windows.ps1             # Windows setup script
├── README.md                     # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore file
```

---

## Changelog

### v2.0.0 (2025-12-24)
- ✅ Added comprehensive input validation
- ✅ Implemented rate limiting (10/hour per tool)
- ✅ Added private network blocking
- ✅ Implemented audit logging
- ✅ Added output sanitization
- ✅ Implemented result caching
- ✅ Added options whitelisting
- ✅ Replaced `run_custom_command` with `run_safe_command`
- ✅ Added `get_scan_statistics` tool
- ✅ Added `clear_cache` tool
- ✅ Created docker-compose.yml for resource management
- ✅ Created config.yaml for configuration
- ✅ Added comprehensive error handling
- ✅ Improved logging and debugging

### v1.0.0 (2025-12-19)
- Initial release

---

## Security Best Practices

### For Users
1. Only scan authorized targets
2. Monitor your scan statistics
3. Clear cache regularly
4. Review audit logs
5. Don't bypass rate limits

### For Developers
1. Never disable input validation
2. Keep audit logs secure
3. Monitor resource usage
4. Update blocked ranges as needed
5. Review security logs regularly

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure security checks pass
5. Update documentation
6. Submit pull request

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Acknowledgments

- [Anthropic](https://www.anthropic.com/) - Claude and MCP
- [Kali Linux](https://www.kali.org/) - Security tools
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP framework
- Security community

---

## Support

### Test Targets (Legal to Scan)
- **scanme.nmap.org** - Official nmap test server
- **testphp.vulnweb.com** - OWASP test application
- **demo.testfire.net** - IBM test application

### Resources
- [MCP Documentation](https://modelcontextprotocol.io/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Kali Linux Docs](https://www.kali.org/docs/)

---

**Made with ❤️ for ethical hackers and security researchers**

**v2.0 - Enhanced Security Edition**
