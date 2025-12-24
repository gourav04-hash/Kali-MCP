#!/usr/bin/env python3
"""
Kali Security Tools MCP Server
Web penetration testing tools for educational purposes
"""
import os
import sys
import logging
import subprocess
import re
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("kali-security-server")

# Initialize MCP server
mcp = FastMCP("kali-security")

# Configuration
MAX_OUTPUT_LENGTH = 10000

# === UTILITY FUNCTIONS ===

def sanitize_input(input_str):
    """Sanitize input to prevent command injection."""
    if not input_str or not input_str.strip():
        return ""
    sanitized = re.sub(r'[;&|`$\(\)<>]', '', input_str.strip())
    return sanitized

def run_command(command, timeout=300):
    """Execute command safely and return formatted output."""
    try:
        logger.info(f"Executing command: {' '.join(command[:3])}...")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        if len(output) > MAX_OUTPUT_LENGTH:
            output = output[:MAX_OUTPUT_LENGTH] + "\n\n... (output truncated)"
        
        return output, result.returncode
    except subprocess.TimeoutExpired:
        return "Command timed out after {} seconds".format(timeout), 1
    except Exception as e:
        return str(e), 1

def format_output(title, output, returncode):
    """Format command output with visual indicators."""
    status = "Success - Scan Complete" if returncode == 0 else "Scan Completed with Warnings"
    return f"{status}\n\n{title}\n\n{output}"

# === MCP TOOLS ===

@mcp.tool()
async def nmap_scan(target: str = "", options: str = "-sV -sC") -> str:
    """Perform network port scan using nmap with version detection and default scripts."""
    if not target.strip():
        return "Error: Target is required (e.g., '192.168.1.1' or 'example.com')"
    
    target = sanitize_input(target)
    options = sanitize_input(options)
    
    if not target:
        return "Error: Invalid target after sanitization"
    
    logger.info(f"Running nmap scan on {target}")
    command = ["nmap"] + options.split() + [target]
    output, returncode = run_command(command, timeout=600)
    
    return format_output(f"Nmap Scan: {target}", output, returncode)

@mcp.tool()
async def nikto_scan(target: str = "", port: str = "80") -> str:
    """Perform web server vulnerability scan using Nikto."""
    if not target.strip():
        return "Error: Target URL is required (e.g., 'http://192.168.1.1')"
    
    target = sanitize_input(target)
    port = sanitize_input(port)
    
    if not target:
        return "Error: Invalid target after sanitization"
    
    logger.info(f"Running Nikto scan on {target}:{port}")
    command = ["nikto", "-h", target, "-p", port]
    output, returncode = run_command(command, timeout=600)
    
    return format_output(f"Nikto Web Scan: {target}:{port}", output, returncode)

@mcp.tool()
async def dirb_scan(target: str = "", wordlist: str = "/usr/share/dirb/wordlists/common.txt") -> str:
    """Perform directory brute force scan using DIRB to find hidden web paths."""
    if not target.strip():
        return "Error: Target URL is required (e.g., 'http://192.168.1.1')"
    
    target = sanitize_input(target)
    
    if not target:
        return "Error: Invalid target after sanitization"
    
    logger.info(f"Running DIRB scan on {target}")
    command = ["dirb", target, wordlist, "-S"]
    output, returncode = run_command(command, timeout=600)
    
    return format_output(f"DIRB Directory Scan: {target}", output, returncode)

@mcp.tool()
async def wpscan_scan(target: str = "", enumerate: str = "p,t,u") -> str:
    """Perform WordPress vulnerability scan using WPScan to enumerate plugins, themes, and users."""
    if not target.strip():
        return "Error: Target WordPress URL is required (e.g., 'http://192.168.1.1/wordpress')"
    
    target = sanitize_input(target)
    enumerate = sanitize_input(enumerate)
    
    if not target:
        return "Error: Invalid target after sanitization"
    
    logger.info(f"Running WPScan on {target}")
    command = ["wpscan", "--url", target, "--enumerate", enumerate, "--no-banner"]
    output, returncode = run_command(command, timeout=600)
    
    return format_output(f"WPScan WordPress Scan: {target}", output, returncode)

@mcp.tool()
async def sqlmap_scan(target: str = "", data: str = "") -> str:
    """Perform SQL injection testing using sqlmap on a target URL."""
    if not target.strip():
        return "Error: Target URL is required (e.g., 'http://192.168.1.1/page.php?id=1')"
    
    target = sanitize_input(target)
    
    if not target:
        return "Error: Invalid target after sanitization"
    
    logger.info(f"Running SQLMap on {target}")
    command = ["sqlmap", "-u", target, "--batch", "--banner"]
    
    if data.strip():
        data = sanitize_input(data)
        command.extend(["--data", data])
    
    output, returncode = run_command(command, timeout=600)
    
    return format_output(f"SQLMap SQL Injection Test: {target}", output, returncode)

@mcp.tool()
async def searchsploit_query(keyword: str = "") -> str:
    """Search exploit database using searchsploit for known vulnerabilities."""
    if not keyword.strip():
        return "Error: Search keyword is required (e.g., 'apache 2.4', 'wordpress 5.0')"
    
    keyword = sanitize_input(keyword)
    
    if not keyword:
        return "Error: Invalid keyword after sanitization"
    
    logger.info(f"Searching exploits for: {keyword}")
    command = ["searchsploit", keyword]
    output, returncode = run_command(command, timeout=60)
    
    return format_output(f"Exploit Database Search: {keyword}", output, returncode)

@mcp.tool()
async def quick_recon(target: str = "") -> str:
    """Perform quick reconnaissance combining nmap and basic vulnerability checks."""
    if not target.strip():
        return "Error: Target is required (e.g., '192.168.1.1' or 'example.com')"
    
    target = sanitize_input(target)
    
    if not target:
        return "Error: Invalid target after sanitization"
    
    logger.info(f"Running quick recon on {target}")
    
    results = []
    
    command = ["nmap", "-F", "-sV", target]
    output, returncode = run_command(command, timeout=300)
    results.append(f"Quick Port Scan:\n{output}\n")
    
    return f"Quick Reconnaissance Complete\n\n{target}\n\n{''.join(results)}"

@mcp.tool()
async def apt_install(package: str = "") -> str:
    """Install a package using apt package manager."""
    if not package.strip():
        return "Error: Package name is required (e.g., 'metasploit-framework', 'burpsuite')"
    
    package = sanitize_input(package)
    
    if not package:
        return "Error: Invalid package name after sanitization"
    
    logger.info(f"Installing package: {package}")
    
    update_cmd = ["apt-get", "update"]
    update_output, update_ret = run_command(update_cmd, timeout=120)
    
    if update_ret != 0:
        return f"Error updating package list:\n{update_output}"
    
    install_cmd = ["apt-get", "install", "-y", package]
    install_output, install_ret = run_command(install_cmd, timeout=300)
    
    if install_ret == 0:
        return f"Successfully installed {package}\n\n{install_output}"
    else:
        return f"Error installing {package}:\n{install_output}"

@mcp.tool()
async def apt_search(keyword: str = "") -> str:
    """Search for available packages in apt repositories."""
    if not keyword.strip():
        return "Error: Search keyword is required"
    
    keyword = sanitize_input(keyword)
    
    if not keyword:
        return "Error: Invalid keyword after sanitization"
    
    logger.info(f"Searching for packages matching: {keyword}")
    command = ["apt-cache", "search", keyword]
    output, returncode = run_command(command, timeout=60)
    
    return format_output(f"Package Search Results: {keyword}", output, returncode)

@mcp.tool()
async def git_clone(repo_url: str = "", destination: str = "") -> str:
    """Clone a git repository to the specified destination."""
    if not repo_url.strip():
        return "Error: Repository URL is required (e.g., 'https://github.com/user/repo.git')"
    
    repo_url = sanitize_input(repo_url)
    
    if not repo_url:
        return "Error: Invalid repository URL after sanitization"
    
    logger.info(f"Cloning repository: {repo_url}")
    
    command = ["git", "clone", repo_url]
    
    if destination.strip():
        destination = sanitize_input(destination)
        command.append(destination)
    
    output, returncode = run_command(command, timeout=300)
    
    return format_output(f"Git Clone: {repo_url}", output, returncode)

@mcp.tool()
async def git_pull(repo_path: str = "/app") -> str:
    """Update a git repository by pulling latest changes."""
    if not repo_path.strip():
        repo_path = "/app"
    
    repo_path = sanitize_input(repo_path)
    
    logger.info(f"Pulling latest changes in: {repo_path}")
    command = ["git", "-C", repo_path, "pull"]
    output, returncode = run_command(command, timeout=120)
    
    return format_output(f"Git Pull: {repo_path}", output, returncode)

@mcp.tool()
async def list_installed_tools() -> str:
    """List security tools currently installed in the container."""
    logger.info("Listing installed security tools")
    
    tools_to_check = [
        "nmap", "nikto", "sqlmap", "wpscan", "dirb", "searchsploit",
        "metasploit-framework", "burpsuite", "john", "hydra", "aircrack-ng",
        "wireshark", "tcpdump", "netcat", "gobuster", "ffuf"
    ]
    
    results = []
    for tool in tools_to_check:
        check_cmd = ["which", tool]
        output, returncode = run_command(check_cmd, timeout=5)
        
        if returncode == 0 and output.strip():
            results.append(f"[INSTALLED] {tool}: {output.strip()}")
        else:
            results.append(f"[NOT FOUND] {tool}")
    
    return "Installed Security Tools:\n\n" + "\n".join(results)

@mcp.tool()
async def run_custom_command(command: str = "") -> str:
    """Execute a custom shell command in the container (use with caution)."""
    if not command.strip():
        return "Error: Command is required"
    
    command = command.strip()
    
    logger.info(f"Executing custom command: {command[:50]}...")
    logger.warning("WARNING: Running custom command - ensure this is safe!")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        if len(output) > MAX_OUTPUT_LENGTH:
            output = output[:MAX_OUTPUT_LENGTH] + "\n\n... (output truncated)"
        
        status = "Success" if result.returncode == 0 else "Failed"
        return f"{status} - Custom Command\n\n{output}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 120 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    if os.geteuid() != 0:
        logger.error("ERROR: This server must run as root for security tools to work properly")
        logger.error("Please rebuild the Docker image or run the container with --user root")
        sys.exit(1)
    
    logger.info("Starting Kali Security Tools MCP server...")
    logger.info("Running as root user (required for network scanning tools)")
    logger.warning("WARNING: EDUCATIONAL USE ONLY - Only scan systems you own or have permission to test")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
