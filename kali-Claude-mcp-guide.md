# Kali Security MCP Server for Claude Desktop

A comprehensive Model Context Protocol (MCP) server that integrates Kali Linux security tools with Claude Desktop for educational penetration testing.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/)
[![WSL2](https://img.shields.io/badge/WSL2-Required-green.svg)](https://docs.microsoft.com/en-us/windows/wsl/)

## ⚠️ Legal Disclaimer

**EDUCATIONAL USE ONLY**

This tool is for educational purposes and authorized security testing only. Unauthorized penetration testing is **ILLEGAL** in most jurisdictions.

- ✅ Only test systems you **own**
- ✅ Get **written permission** before testing any system
- ✅ Follow responsible disclosure practices
- ❌ **Never** scan unauthorized systems

**Violations can result in criminal prosecution under computer fraud laws (CFAA, Computer Misuse Act, etc.)**

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Tools](#available-tools)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Security Scanning Tools
- **nmap** - Network port scanning and service detection
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

### Custom Commands
- **run_custom_command** - Execute arbitrary shell commands (advanced users)

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

# 3. Configure Claude Desktop (in PowerShell)
.\setup-windows.ps1

# 4. Restart Claude Desktop

# 5. Test in Claude
"List all available security tools"
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

#### Verify Installation
```powershell
# PowerShell
docker --version
wsl --list --verbose
```

```bash
# WSL Terminal
docker ps
```

### Step 2: Clone Repository

```bash
# In WSL terminal
git clone https://github.com/yourusername/kali-mcp-server.git
cd kali-mcp-server
```

### Step 3: Build Docker Image

```bash
# In WSL terminal (this takes 5-10 minutes)
docker build -t kali-security-mcp-server .
```

**Expected Output:**
```
[+] Building 300.2s (12/12) FINISHED
 => [internal] load build definition
 => => transferring dockerfile: 1.01kB
 ...
 => exporting to image
Successfully built abc123def456
Successfully tagged kali-security-mcp-server:latest
```

### Step 4: Verify Build

```bash
# Check image exists
docker images | grep kali-security

# Test container runs
docker run --rm -it kali-security-mcp-server python3 -c 'print("Success!")'
```

### Step 5: Configure Windows

Run the setup script in **Windows PowerShell**:

```powershell
# Navigate to cloned directory
cd C:\path\to\kali-mcp-server

# Run setup script
.\setup-windows.ps1
```

**Or manually create config:**

```powershell
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$configContent = @"
{
  "mcpServers": {
    "kali-security": {
      "command": "wsl",
      "args": [
        "docker",
        "run",
        "-i",
        "--rm",
        "--privileged",
        "--network=host",
        "kali-security-mcp-server"
      ]
    }
  }
}
"@
[System.IO.File]::WriteAllText($configPath, $configContent)
```

### Step 6: Restart Claude Desktop

1. **Completely quit** Claude Desktop (check system tray)
2. Wait 5 seconds
3. **Restart** Claude Desktop
4. Look for 🔨 hammer icon at bottom of chat

### Step 7: Verify Installation

In Claude Desktop, ask:
```
"What security tools do you have available?"
```

Expected response should list all available tools.

---

## Configuration

### Claude Desktop Config Location

**Windows**: `C:\Users\USERNAME\AppData\Roaming\Claude\claude_desktop_config.json`

### Config File Structure

```json
{
  "mcpServers": {
    "kali-security": {
      "command": "wsl",
      "args": [
        "docker",
        "run",
        "-i",
        "--rm",
        "--privileged",
        "--network=host",
        "kali-security-mcp-server"
      ]
    }
  }
}
```

### Important Flags

| Flag | Purpose | Required |
|------|---------|----------|
| `--privileged` | Network scanning capabilities | Yes |
| `--network=host` | Direct network access | Yes |
| `-i` | Interactive mode | Yes |
| `--rm` | Remove container after exit | Recommended |

---

## Available Tools

### Network Scanning

#### nmap_scan
```
"Scan 192.168.1.100 for open ports"
"Run nmap with -sV -sC options on example.com"
```

**Parameters:**
- `target` (required): IP address or domain
- `options` (optional): nmap flags (default: `-sV -sC`)

#### quick_recon
```
"Perform quick reconnaissance on 192.168.1.1"
```

**Parameters:**
- `target` (required): IP address or domain

### Web Vulnerability Scanning

#### nikto_scan
```
"Scan http://192.168.1.100 with Nikto"
```

**Parameters:**
- `target` (required): URL
- `port` (optional): Port number (default: `80`)

#### dirb_scan
```
"Brute force directories on http://example.com"
```

**Parameters:**
- `target` (required): URL
- `wordlist` (optional): Path to wordlist

#### wpscan_scan
```
"Check http://example.com/wordpress for vulnerabilities"
```

**Parameters:**
- `target` (required): WordPress URL
- `enumerate` (optional): What to enumerate (default: `p,t,u`)

### SQL Injection Testing

#### sqlmap_scan
```
"Test http://example.com/page.php?id=1 for SQL injection"
```

**Parameters:**
- `target` (required): URL with parameter
- `data` (optional): POST data

### Exploit Search

#### searchsploit_query
```
"Search for Apache 2.4 exploits"
"Find WordPress 5.0 vulnerabilities"
```

**Parameters:**
- `keyword` (required): Search term

### Package Management

#### apt_install
```
"Install metasploit-framework"
"Install burpsuite"
```

**Parameters:**
- `package` (required): Package name

#### apt_search
```
"Search for wireless hacking tools"
```

**Parameters:**
- `keyword` (required): Search term

#### list_installed_tools
```
"List all installed security tools"
```

### Git Operations

#### git_clone
```
"Clone https://github.com/danielmiessler/SecLists"
```

**Parameters:**
- `repo_url` (required): Git repository URL
- `destination` (optional): Target directory

#### git_pull
```
"Update the repository at /app/SecLists"
```

**Parameters:**
- `repo_path` (optional): Repository path (default: `/app`)

### Advanced

#### run_custom_command
```
"Run: ls -la /usr/share/wordlists"
```

**Parameters:**
- `command` (required): Shell command

**⚠️ Warning**: Use with caution. Can execute any command as root.

---

## Usage Examples

### Example 1: Basic Network Scan

```
User: "I need to scan my local server at 192.168.1.100"

Claude: I'll perform a comprehensive scan of your server.

[Executes nmap_scan]

Results:
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1
80/tcp  open  http        Apache 2.4.41
443/tcp open  https       Apache 2.4.41
3306/tcp open mysql       MySQL 5.7.33

Recommendations:
- SSH is exposed - ensure strong authentication
- Update Apache (current version has known CVEs)
- MySQL should not be externally accessible
```

### Example 2: WordPress Security Audit

```
User: "Audit my WordPress site at http://mysite.local"

Claude: I'll perform a comprehensive WordPress security scan.

[Executes wpscan_scan]

Findings:
✓ WordPress core is up to date (6.4.2)
⚠ Plugin "contact-form-7" is outdated (v5.5.3)
⚠ Theme "twentytwenty" has known XSS vulnerability
✗ XML-RPC is enabled (DoS risk)
✗ User enumeration possible

Priority Actions:
1. Update Contact Form 7 to latest version
2. Update or replace twentytwenty theme
3. Disable XML-RPC in wp-config.php
4. Implement user enumeration protection
```

### Example 3: Web Application Testing

```
User: "Test my development site for common vulnerabilities"

Claude: I'll run a comprehensive vulnerability assessment.

[Executes nikto_scan]
[Executes dirb_scan]

Nikto Results:
- Server: Apache/2.4.41 (outdated)
- Found: /admin directory (no authentication)
- Found: .git directory exposed
- Missing security headers (X-Frame-Options, CSP)

DIRB Results:
- /admin (200 OK)
- /backup (403 Forbidden)
- /config.php.bak (200 OK)
- /.git (200 OK)

Critical Issues:
1. Git repository exposed - full source code accessible
2. Backup file contains credentials
3. Admin panel accessible without VPN

Immediate Actions Required:
1. Remove .git directory from web root
2. Delete backup files
3. Restrict admin access by IP
4. Add security headers
```

### Example 4: Installing Additional Tools

```
User: "I need to install Metasploit"

Claude: I'll install Metasploit Framework for you.

[Executes apt_install with "metasploit-framework"]

Installation successful!

Metasploit Framework has been installed. You can now:
- Search and use exploit modules
- Perform vulnerability validation
- Generate payloads
- Conduct penetration testing

Would you like me to search for a specific exploit?
```

### Example 5: SQL Injection Testing

```
User: "Check if this login form is vulnerable: http://testsite.local/login.php"

Claude: I'll test for SQL injection vulnerabilities.

[Executes sqlmap_scan]

⚠ CRITICAL VULNERABILITY FOUND

SQL Injection Details:
- Parameter: username
- Injection Type: Boolean-based blind
- Database: MySQL 5.7.33
- Risk: HIGH - Full database access possible

The application is vulnerable to SQL injection. An attacker can:
- Extract all database contents
- Modify/delete data
- Potentially execute system commands

Required Fixes:
1. Use parameterized queries/prepared statements
2. Implement input validation
3. Apply principle of least privilege to DB user
4. Add Web Application Firewall (WAF)
5. Enable query logging for forensics

Sample secure code:
```php
// INSECURE (current)
$query = "SELECT * FROM users WHERE username='$_POST[username]'";

// SECURE (recommended)
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$_POST['username']]);
```
```

---

## Troubleshooting

### Issue 1: Claude Desktop Crashes on Startup

**Symptoms**: Application closes immediately after opening

**Cause**: Invalid JSON or BOM (Byte Order Mark) in config file

**Solution**:
```powershell
# Delete and recreate config
Remove-Item "$env:APPDATA\Claude\claude_desktop_config.json" -Force

# Use WriteAllText (NOT Out-File)
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$configContent = '{"mcpServers":{"kali-security":{"command":"wsl","args":["docker","run","-i","--rm","--privileged","--network=host","kali-security-mcp-server"]}}}'
[System.IO.File]::WriteAllText($configPath, $configContent)
```

**Check logs**:
```powershell
Get-Content "$env:APPDATA\Claude\logs\main.log" -Tail 50
```

---

### Issue 2: "Operation not permitted" Error

**Symptoms**: nmap scans fail with permission errors

**Cause**: Container lacks required capabilities

**Solution 1**: Verify `--privileged` flag
```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

Must include: `"--privileged"` and `"--network=host"`

**Solution 2**: Test manually
```bash
# In WSL - should work
docker run --rm -it --privileged --network=host kali-security-mcp-server nmap -F scanme.nmap.org
```

**Solution 3**: Check for conflicts
Ensure no other MCP server entries (like `MCP_DOCKER`) conflict with `kali-security`

---

### Issue 3: MCP Server Not Visible

**Symptoms**: No hammer icon 🔨 in Claude Desktop

**Cause**: Config file not found or invalid

**Diagnostics**:
```powershell
# Verify file exists
Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"

# Validate JSON
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json

# Check logs
Get-Content "$env:APPDATA\Claude\logs\main.log" -Tail 100
```

**Look for**:
- ✅ `"Launching MCP Server: kali-security"`
- ❌ `"Error reading or parsing config file"`

---

### Issue 4: Docker Build Fails

**Error**: `unknown instruction: ```  `

**Cause**: Markdown code fences in Dockerfile

**Solution**: Ensure Dockerfile starts with `# Use Kali Linux...` (no backticks)

---

### Issue 5: WSL Can't Access Docker

**Symptoms**: `docker: command not found` in WSL

**Solution**:
1. Open Docker Desktop
2. Settings → Resources → WSL Integration
3. Enable integration with your WSL distro
4. Apply & Restart

**Verify**:
```bash
docker ps
```

---

### Issue 6: Python Syntax Errors

**Error**: `SyntaxError: invalid character '⚠'`

**Cause**: Emoji characters in Python code

**Solution**: 
1. Edit `kali_security_server.py`
2. Replace emojis with plain text:
   - `"WARNING: ..."` instead of `"⚠️ WARNING: ..."`
   - `"Success"` instead of `"✅ Success"`
3. Rebuild: `docker build -t kali-security-mcp-server .`

---

### Debug Checklist

Run through this checklist when troubleshooting:

- [ ] Docker Desktop is running
- [ ] WSL2 integration enabled
- [ ] Image exists: `docker images | grep kali-security`
- [ ] Config exists: `Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"`
- [ ] JSON is valid: `Get-Content ... | ConvertFrom-Json`
- [ ] No BOM in config (check for `ï»¿` in logs)
- [ ] `--privileged` flag present
- [ ] Claude Desktop fully restarted (not just window closed)
- [ ] Container runs manually: `docker run --rm -it --privileged kali-security-mcp-server`
- [ ] No conflicting MCP servers in config
- [ ] Firewall/Antivirus not blocking Docker

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Windows System                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Claude Desktop (Windows App)              │  │
│  │                                                   │  │
│  │  Reads: claude_desktop_config.json               │  │
│  └───────────────────┬───────────────────────────────┘  │
│                      │                                   │
│                      │ Executes via WSL                  │
│                      ▼                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │           WSL2 (Linux Subsystem)                  │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │      Docker Container (Privileged)          │ │  │
│  │  │  ┌───────────────────────────────────────┐ │ │  │
│  │  │  │  Kali Linux Base                      │ │ │  │
│  │  │  │  ├─ Python 3.11                       │ │ │  │
│  │  │  │  ├─ FastMCP Server                    │ │ │  │
│  │  │  │  ├─ Security Tools                    │ │ │  │
│  │  │  │  │  ├─ nmap                           │ │ │  │
│  │  │  │  │  ├─ nikto                          │ │ │  │
│  │  │  │  │  ├─ sqlmap                         │ │ │  │
│  │  │  │  │  ├─ wpscan                         │ │ │  │
│  │  │  │  │  └─ dirb                           │ │ │  │
│  │  │  │  ├─ Package Manager (apt)             │ │ │  │
│  │  │  │  └─ Git                               │ │ │  │
│  │  │  └───────────────────────────────────────┘ │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

Communication Flow:
1. Claude Desktop → Reads config file
2. Claude Desktop → Launches WSL command
3. WSL → Starts Docker container with privileges
4. Container → Runs Python MCP server
5. MCP Server ← → Claude via stdio (JSON-RPC)
6. Security Tools ← → Network (with elevated privileges)
```

---

## Project Structure

```
kali-mcp-server/
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
├── kali_security_server.py       # Main MCP server code
├── setup-windows.ps1             # Windows setup script
├── README.md                     # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore file
```

---

## Security Best Practices

### Container Security
- ✅ Runs as root (required for security tools)
- ✅ Isolated from host (Docker container)
- ✅ No persistent storage (data lost on restart)
- ⚠️ Privileged mode (necessary for network access)

### Usage Guidelines
1. **Authorization**: Always get written permission
2. **Scope**: Stay within agreed boundaries
3. **Documentation**: Keep logs of all activities
4. **Disclosure**: Report findings responsibly
5. **Education**: Use for learning, not malicious purposes

### Legal Compliance
- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK
- Similar laws exist worldwide
- Penalties include fines and imprisonment

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guide
- Add docstrings to all functions
- Test all changes in isolated environment
- Update README with new features

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Anthropic](https://www.anthropic.com/) - Claude and MCP protocol
- [Kali Linux](https://www.kali.org/) - Security tool distribution
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- Security community - Tool developers

---

## Support

### Resources
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Kali Linux Tools](https://www.kali.org/tools/)
- [WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)

### Practice Platforms
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [OverTheWire](https://overthewire.org/)
- [PentesterLab](https://pentesterlab.com/)

### Getting Help
- Check [Issues](https://github.com/yourusername/kali-mcp-server/issues) for common problems
- Review [Troubleshooting](#troubleshooting) section
- Check Claude Desktop logs
- Test container manually in WSL

---

## Changelog

### v1.0.0 (2025-12-19)
- Initial release
- Core security scanning tools (nmap, nikto, sqlmap, wpscan, dirb)
- Package management (apt install/search)
- Git integration (clone/pull)
- Custom command execution
- Windows/WSL/Docker setup automation

---

## Roadmap

### Planned Features
- [ ] Metasploit integration
- [ ] Burp Suite proxy configuration
- [ ] Report generation (PDF/HTML)
- [ ] Automated vulnerability scoring
- [ ] Integration with vulnerability databases
- [ ] Web UI for configuration
- [ ] macOS and Linux support
- [ ] Persistent storage option

---

**Made with ❤️ for ethical hackers and security researchers**

**Remember: With great power comes great responsibility. Use wisely and legally.**
