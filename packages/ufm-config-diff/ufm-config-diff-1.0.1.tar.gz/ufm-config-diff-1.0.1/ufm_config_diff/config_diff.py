import paramiko
import os
import re
import logging
import argparse
from io import StringIO
import sys
import shutil
import json
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Initialize colorama for cross-platform color support
init()

# Custom help formatter to add colors and examples
class ColorHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=30, width=None):
        super().__init__(prog, indent_increment, max_help_position, width)
        
    def _split_lines(self, text, width):
        # Apply colors to specific phrases in the help text
        text = text.replace('[EXAMPLES]', f'{Fore.YELLOW}EXAMPLES:{Style.RESET_ALL}')
        text = text.replace('[NOTE]', f'{Fore.CYAN}NOTE:{Style.RESET_ALL}')
        text = text.replace('[WARNING]', f'{Fore.RED}WARNING:{Style.RESET_ALL}')
        
        # Color key terms
        text = text.replace('docker mode', f'{Fore.GREEN}docker mode{Style.RESET_ALL}')
        text = text.replace('--email', f'{Fore.GREEN}--email{Style.RESET_ALL}')
        text = text.replace('--fabric-interface', f'{Fore.GREEN}--fabric-interface{Style.RESET_ALL}')
        text = text.replace('--mgmt-interface', f'{Fore.GREEN}--mgmt-interface{Style.RESET_ALL}')
        text = text.replace('--yes', f'{Fore.GREEN}--yes{Style.RESET_ALL}')
        text = text.replace('-y', f'{Fore.GREEN}-y{Style.RESET_ALL}')
        
        # Handle example commands with indentation and color
        lines = []
        for line in text.splitlines():
            if line.strip().startswith('$'):
                # This is an example command
                line = f"{Fore.CYAN}{line}{Style.RESET_ALL}"
            lines.extend(super()._split_lines(line, width))
        return lines

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Helper function to compare version strings without external dependencies
def compare_versions(version1, version2):
    """Compare two version strings, returns True if version2 > version1"""
    try:
        # Split versions by dots and compare numerically
        v1_parts = re.split(r'[.-]', version1.lower().replace('build', '').strip())
        v2_parts = re.split(r'[.-]', version2.lower().replace('build', '').strip())
        
        # Convert to integers where possible
        v1_cleaned = []
        v2_cleaned = []
        
        for part in v1_parts:
            try:
                v1_cleaned.append(int(part))
            except ValueError:
                v1_cleaned.append(part)
                
        for part in v2_parts:
            try:
                v2_cleaned.append(int(part))
            except ValueError:
                v2_cleaned.append(part)
        
        # Compare each part
        for i in range(min(len(v1_cleaned), len(v2_cleaned))):
            # If both parts are integers, compare numerically
            if isinstance(v1_cleaned[i], int) and isinstance(v2_cleaned[i], int):
                if v1_cleaned[i] < v2_cleaned[i]:
                    return True
                elif v1_cleaned[i] > v2_cleaned[i]:
                    return False
            # Otherwise compare as strings
            else:
                if str(v1_cleaned[i]) < str(v2_cleaned[i]):
                    return True
                elif str(v1_cleaned[i]) > str(v2_cleaned[i]):
                    return False
                    
        # If we've compared all parts and they're equal so far,
        # the longer version is considered greater
        return len(v1_cleaned) < len(v2_cleaned)
    except Exception as e:
        logger.warning(f"Error comparing versions, falling back to string comparison: {e}")
        # If all else fails, fall back to lexicographical comparison
        return version2 > version1

# SSH Helper Function
def ssh_connect(host, username, password):
    try:
        logger.info(f"Connecting to {host}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        return ssh
    except Exception as e:
        logger.error(f"SSH connection failed for {host}: {e}")
        raise

# Function to fetch files with .cfg and .conf extensions
def fetch_config_files(ssh, path="/opt/ufm/"):
    try:
        files = []
        stdin, stdout, stderr = ssh.exec_command('find {} -type f \\( -name "*.cfg" -o -name "*.conf" \\)'.format(path))
        files = stdout.read().decode().splitlines()
        logger.info(f"Found {len(files)} configuration files.")
        return files
    except Exception as e:
        logger.error(f"Failed to fetch configuration files: {e}")
        raise

# Function to fetch UFM version
def fetch_ufm_version(ssh, path="/opt/ufm/files/ufm_version"):
    try:
        stdin, stdout, stderr = ssh.exec_command(f"cat {path}")
        version = stdout.read().decode().strip()
        if version:
            logger.info(f"UFM Version: {version}")
            return version
        else:
            logger.error("UFM version file not found or empty.")
            return None
    except Exception as e:
        logger.error(f"Failed to fetch UFM version: {e}")
        raise

# Function to get UFM version
def get_ufm_version(ssh, host=None):
    try:
        # Execute the command and get the output
        stdin, stdout, stderr = ssh.exec_command("cat /opt/ufm/ufm_config_files/ufm_version")
        version = stdout.read().decode('utf-8').strip()
        
        # Add error logging
        error = stderr.read().decode('utf-8').strip()
        if error:
            logger.error(f"Error reading UFM version on {host}: {error}")
        
        # Add debug logging
        logger.debug(f"UFM version read: {version}")
        
        if not version:
            logger.warning(f"UFM version file is empty on {host}")
            return "Unknown"
            
        return version
    except Exception as e:
        if host:
            logger.error(f"Error reading UFM version on {host}: {e}")
        else:
            logger.error(f"Error reading UFM version: {e}")
        return "Unknown"

def strip_ansi_codes(text):
    """Remove ANSI escape sequences from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# Function to compare parameters between two configuration files
def compare_files(ssh1, ssh2, file_path):
    try:
        # Read content from both servers
        stdin1, stdout1, stderr1 = ssh1.exec_command(f"cat {file_path}")
        stdin2, stdout2, stderr2 = ssh2.exec_command(f"cat {file_path}")
        
        # Read raw bytes instead of trying to decode as UTF-8
        file1_content = stdout1.read()
        file2_content = stdout2.read()

        try:
            # Try to decode as UTF-8 first
            file1_lines = [strip_ansi_codes(line) for line in file1_content.decode('utf-8').splitlines()]
            file2_lines = [strip_ansi_codes(line) for line in file2_content.decode('utf-8').splitlines()]
        except UnicodeDecodeError:
            # If UTF-8 fails, treat as binary and compare raw bytes
            if file1_content != file2_content:
                return [("Binary file differs", "Binary file differs", "Modified")]
            return []

        # Parse parameters from both files
        def parse_config(lines):
            params = {}
            for line in lines:
                line = line.strip()
                # Skip empty lines, comments, and UFM version lines
                if (not line or 
                    line.startswith('#') or 
                    line.startswith(';') or 
                    'UFM Version' in line):  # Skip UFM Version lines
                    continue
                # Try to split on common parameter separators (=, :, space)
                for separator in ['=', ':', ' ']:
                    if separator in line:
                        key, value = line.split(separator, 1)
                        key = key.strip()
                        value = value.strip()
                        params[key] = value
                        break
            return params

        params1 = parse_config(file1_lines)
        params2 = parse_config(file2_lines)

        # Compare parameters
        diff = []
        # Check all keys from first file
        for key in params1:
            if key in params2:
                if params1[key] != params2[key]:
                    diff.append((
                        f"{key}: {params1[key]}",
                        f"{key}: {params2[key]}",
                        "Modified"
                    ))
            else:
                diff.append((f"{key}: {params1[key]}", "Parameter not found", "Parameter Deleted"))

        # Check for parameters only in second file
        for key in params2:
            if key not in params1:
                diff.append(("Parameter not found", f"{key}: {params2[key]}", "New Parameter added"))

        # Sort by status: Modified, New Parameter, Parameter Deleted
        def sort_key(item):
            status = item[2]
            if status == "Modified":
                return 0
            elif status == "New Parameter added":
                return 1
            else:  # "Parameter Deleted"
                return 2
                
        diff.sort(key=sort_key)
        return diff

    except Exception as e:
        logger.error(f"Error comparing file {file_path} between servers: {e}")
        raise

def compare_configurations(server1, server2, fast_mode=False):
    try:
        ssh1 = ssh_connect(server1['host'], server1['username'], server1['password'])
        ssh2 = ssh_connect(server2['host'], server2['username'], server2['password'])

        # Check UFM version files exist on both servers
        logger.info("Checking UFM installation on servers...")
        if not check_ufm_version(ssh1, server1['host']):
            print(f"\nError: UFM version file not found on {server1['host']}")
            print("Please ensure UFM is properly installed and the version file exists at /opt/ufm/files/ufm_version")
            sys.exit(1)
            
        if not check_ufm_version(ssh2, server2['host']):
            print(f"\nError: UFM version file not found on {server2['host']}")
            print("Please ensure UFM is properly installed and the version file exists at /opt/ufm/files/ufm_version")
            sys.exit(1)

        # If we get here, both servers have UFM version files
        logger.info("UFM installation verified on both servers")
        
        # Get UFM versions
        ufm_version1 = get_ufm_version(ssh1, server1['host'])
        ufm_version2 = get_ufm_version(ssh2, server2['host'])
        
        # Get SHARP versions
        sharp_version1 = get_sharp_version(ssh1, server1['host'])
        sharp_version2 = get_sharp_version(ssh2, server2['host'])

        # Get MFT versions
        mft_version1 = get_mft_version(ssh1, server1['host'])
        mft_version2 = get_mft_version(ssh2, server2['host'])

        # Get OpenSM versions
        opensm_version1 = get_opensm_version(ssh1, server1['host'])
        opensm_version2 = get_opensm_version(ssh2, server2['host'])

        base_path = "/opt/ufm/files/"
        
        if fast_mode:
            # In fast mode, only check specific files with their full paths
            critical_files = [
                '/opt/ufm/ufm_config_files/conf/gv.cfg',
                '/opt/ufm/ufm_config_files/conf/opensm/opensm.conf',
                '/opt/ufm/ufm_config_files/conf/sharp/sharp_am.cfg', 
                '/etc/mft/mft.conf'
            ]
            files1 = critical_files
            files2 = critical_files
        else:
            # Get list of all files from both servers
            stdin1, stdout1, stderr1 = ssh1.exec_command(f"find {base_path} -type f")
            stdin2, stdout2, stderr2 = ssh2.exec_command(f"find {base_path} -type f")
            
            files1 = stdout1.read().decode('utf-8').splitlines()
            files2 = stdout2.read().decode('utf-8').splitlines()

        # Compare files and collect differences
        file_comparisons = []
        common_files = set(files1).intersection(set(files2))

        for file_path in common_files:
            file_diff = compare_files(ssh1, ssh2, file_path)
            if file_diff:
                file_comparisons.append({"file": file_path, "diff": file_diff})

        # Determine version order for display
        swap_servers = compare_versions(ufm_version1, ufm_version2)
        
        # If server2 has a higher version, we'll display it on the right as requested
        if swap_servers:
            # We're already good - server 2 has the higher version and will be on the right
            is_swapped = False
        else:
            # We need to swap to put the higher version on the right
            server1, server2 = server2, server1
            ufm_version1, ufm_version2 = ufm_version2, ufm_version1
            sharp_version1, sharp_version2 = sharp_version2, sharp_version1
            mft_version1, mft_version2 = mft_version2, mft_version1
            opensm_version1, opensm_version2 = opensm_version2, opensm_version1
            is_swapped = True
            
            # Also swap the diff data for display
            for file_comp in file_comparisons:
                swapped_diff = []
                for diff1, diff2, status in file_comp['diff']:
                    swapped_diff.append((diff2, diff1, status))
                file_comp['diff'] = swapped_diff

        return {
            'ufm_version1': ufm_version1,
            'ufm_version2': ufm_version2,
            'sharp_version1': sharp_version1,
            'sharp_version2': sharp_version2,
            'mft_version1': mft_version1,
            'mft_version2': mft_version2,
            'opensm_version1': opensm_version1,
            'opensm_version2': opensm_version2,
            'files': file_comparisons,
            'server1': server1,
            'server2': server2,
            'is_swapped': is_swapped
        }

    except Exception as e:
        logger.error(f"Error comparing configurations: {e}")
        raise
    finally:
        ssh1.close()
        ssh2.close()

def check_ufm_version(ssh, host):
    """Check if UFM version file exists and is readable"""
    try:
        # First check if the file exists
        stdin, stdout, stderr = ssh.exec_command("test -f /opt/ufm/ufm_config_files/ufm_version && echo 'exists'")
        if not stdout.read().decode('utf-8').strip():
            logger.error(f"UFM version file not found on {host}")
            return False
        return True
    except Exception as e:
        logger.error(f"Error checking UFM version on {host}: {e}")
        return False

def get_sharp_version(ssh, host=None):
    """Extract SHARP version from sharp_am.cfg"""
    try:
        # First check if file exists
        stdin, stdout, stderr = ssh.exec_command("test -f /opt/ufm/ufm_config_files/conf/sharp/sharp_am.cfg && echo 'exists'")
        if not stdout.read().decode('utf-8').strip():
            if host:
                logger.warning(f"{Fore.YELLOW}SHARP configuration file not found on {host} - Searched in: /opt/ufm/ufm_config_files/conf/sharp/sharp_am.cfg{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}SHARP configuration file not found - Searched in: /opt/ufm/ufm_config_files/conf/sharp/sharp_am.cfg{Style.RESET_ALL}")
            return "Unknown"
            
        cmd = "grep '# Version:' /opt/ufm/ufm_config_files/conf/sharp/sharp_am.cfg"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        version_line = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        
        if error:
            if host:
                logger.warning(f"{Fore.YELLOW}Error reading SHARP version on {host}: {error}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}Error reading SHARP version: {error}{Style.RESET_ALL}")
        
        if version_line:
            # Extract version number from "# Version: X.Y.Z"
            version = version_line.split(':')[1].strip()
            return version
        else:
            if host:
                logger.warning(f"{Fore.YELLOW}Version line not found in SHARP config file on {host}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}Version line not found in SHARP config file{Style.RESET_ALL}")
    except Exception as e:
        if host:
            logger.error(f"{Fore.YELLOW}Error reading SHARP version on {host}: {e}{Style.RESET_ALL}")
        else:
            logger.error(f"{Fore.YELLOW}Error reading SHARP version: {e}{Style.RESET_ALL}")
    return "Unknown"

def get_mft_version(ssh, host=None):
    """Extract MFT version from mst version command"""
    try:
        # First check if mst command exists
        stdin, stdout, stderr = ssh.exec_command("command -v mst || echo 'not found'")
        result = stdout.read().decode('utf-8').strip()
        if 'not found' in result:
            if host:
                logger.warning(f"{Fore.YELLOW}MFT tools (mst) not installed on {host}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}MFT tools (mst) not installed{Style.RESET_ALL}")
            return "Not Installed"
            
        cmd = "mst version"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        version_line = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        
        if error:
            if host:
                logger.warning(f"{Fore.YELLOW}Error executing mst version on {host}: {error}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}Error executing mst version: {error}{Style.RESET_ALL}")
        
        if version_line:
            # Try to find the part starting with "mft" and extract version until the comma
            if 'mft' in version_line:
                mft_part = version_line.split('mft')[1].strip()
                version = mft_part.split(',')[0]
                return version
            else:
                if host:
                    logger.warning(f"{Fore.YELLOW}Unexpected format from mst version on {host}: {version_line}{Style.RESET_ALL}")
                else:
                    logger.warning(f"{Fore.YELLOW}Unexpected format from mst version: {version_line}{Style.RESET_ALL}")
        else:
            if host:
                logger.warning(f"{Fore.YELLOW}Empty output from mst version on {host}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}Empty output from mst version{Style.RESET_ALL}")
    except Exception as e:
        if host:
            logger.error(f"{Fore.YELLOW}Error reading MFT version on {host}: {e}{Style.RESET_ALL}")
        else:
            logger.error(f"{Fore.YELLOW}Error reading MFT version: {e}{Style.RESET_ALL}")
    return "Unknown"

def get_opensm_version(ssh, host=None):
    """Extract OpenSM version from opensm.log"""
    try:
        # First check if log file exists
        stdin, stdout, stderr = ssh.exec_command("test -f /opt/ufm/ufm_config_files/log/opensm.log && echo 'exists'")
        if not stdout.read().decode('utf-8').strip():
            if host:
                logger.warning(f"{Fore.YELLOW}OpenSM log file not found on {host} - Searched in: /opt/ufm/ufm_config_files/log/opensm.log{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}OpenSM log file not found - Searched in: /opt/ufm/ufm_config_files/log/opensm.log{Style.RESET_ALL}")
            return "Log Not Found"
            
        cmd = "cat /opt/ufm/ufm_config_files/log/opensm.log | grep OpenSM | head -1 | sed 's/.*\\(OpenSM [^ ]*\\).*/\\1/'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        version_line = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        
        if error:
            if host:
                logger.warning(f"{Fore.YELLOW}Error parsing OpenSM log on {host}: {error}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}Error parsing OpenSM log: {error}{Style.RESET_ALL}")
        
        if version_line:
            # The command already formats the output as "OpenSM X.Y.Z"
            if 'OpenSM' in version_line:
                return version_line.split('OpenSM ')[1]
            else:
                if host:
                    logger.warning(f"{Fore.YELLOW}Unexpected format from OpenSM log on {host}: {version_line}{Style.RESET_ALL}")
                else:
                    logger.warning(f"{Fore.YELLOW}Unexpected format from OpenSM log: {version_line}{Style.RESET_ALL}")
        else:
            if host:
                logger.warning(f"{Fore.YELLOW}No OpenSM version found in log on {host}{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}No OpenSM version found in log{Style.RESET_ALL}")
    except Exception as e:
        if host:
            logger.error(f"{Fore.YELLOW}Error reading OpenSM version on {host}: {e}{Style.RESET_ALL}")
        else:
            logger.error(f"{Fore.YELLOW}Error reading OpenSM version: {e}{Style.RESET_ALL}")
    return "Unknown"

def generate_html_report(server1, server2, comparisons, output_file):
    """Generate HTML report with enhanced UI/UX"""
    try:
        # Create a unique ID for each file for table of contents links
        file_ids = {}
        for i, file_comp in enumerate(comparisons['files']):
            file_path = file_comp['file']
            file_id = f"file-{i}"
            file_ids[file_path] = file_id
        
        # Determine which versions are different and need markers
        version_diff = {
            'ufm': comparisons['ufm_version1'] != comparisons['ufm_version2'],
            'sharp': comparisons['sharp_version1'] != comparisons['sharp_version2'],
            'mft': comparisons['mft_version1'] != comparisons['mft_version2'],
            'opensm': comparisons['opensm_version1'] != comparisons['opensm_version2']
        }
        
        # Define CSS separately to avoid issues with -- in CSS variables
        css = """
    <style>
        :root {
            --nvidia-green: #76b900;
            --nvidia-dark: #1a1a1a;
            --nvidia-light: #f2f2f2;
            --diff-color: #ffeb99;
            --missing-color: #ffcccc;
            --matching-color: #e6ffe6;
            --version-diff: #ff8c00;
            --modified-color: #ffcc66;
            --new-param-color: #99ff99;
            --deleted-param-color: #ff9999;
            --missing-file-color: #ffa500;
        }
        
        body {
            font-family: 'DINPro', Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #ffffff;
        }
        
        .container {
            width: 95%;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: var(--nvidia-dark);
            color: #fff;
            padding: 20px;
            margin-bottom: 30px;
        }
        
        h1, h2, h3, h4 {
            font-family: 'DINPro-Bold', Arial, sans-serif;
            margin-top: 0;
        }
        
        h1 {
            color: var(--nvidia-green);
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        h2 {
            color: var(--nvidia-dark);
            font-size: 1.8em;
            margin: 20px 0;
            border-bottom: 2px solid var(--nvidia-green);
            padding-bottom: 8px;
        }
        
        h3 {
            color: var(--nvidia-dark);
            font-size: 1.4em;
            margin: 15px 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            font-size: 13px;
        }
        
        th {
            background-color: var(--nvidia-dark);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: bold;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
            vertical-align: top;
            word-wrap: break-word;
            max-width: 450px;
            font-family: 'DINPro', Arial, sans-serif;
            font-size: 13px;
        }
        
        /* Column widths */
        th:nth-child(1), td:nth-child(1) { width: 40%; }
        th:nth-child(2), td:nth-child(2) { width: 40%; }
        th:nth-child(3), td:nth-child(3) { width: 20%; }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:hover {
            background-color: #f1f1f1;
        }
        
        .diff {
            background-color: var(--diff-color);
            font-weight: bold;
        }
        
        .missing {
            background-color: var(--missing-color);
            color: #cc0000;
            font-weight: bold;
        }
        
        .status-modified {
            background-color: var(--modified-color) !important;
            font-weight: bold !important;
        }
        
        .status-new {
            background-color: var(--new-param-color) !important;
            font-weight: bold !important;
        }
        
        .status-deleted {
            background-color: var(--deleted-param-color) !important;
            font-weight: bold !important;
        }
        
        .status-badge {
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-badge.status-modified {
            background-color: #ffc107;
            color: #000000;
        }
        
        .status-badge.status-new {
            background-color: #28a745;
            color: #000000;
        }
        
        .status-badge.status-deleted {
            background-color: #dc3545;
            color: #000000;
        }
        
        .toc {
            background-color: var(--nvidia-light);
            padding: 20px;
            margin-bottom: 30px;
            border-left: 4px solid var(--nvidia-green);
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 8px 0;
        }
        
        .toc a {
            color: #0066cc; /* Hyperlink blue color */
            text-decoration: underline; /* Underline to make it look like a hyperlink */
            padding: 5px;
            display: block;
            transition: all 0.2s ease;
        }
        
        .toc a:hover {
            background-color: var(--nvidia-green);
            color: white;
            text-decoration: none; /* Remove underline on hover */
        }
        
        .server-info {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .server-card {
            flex: 1;
            min-width: 300px;
            background-color: var(--nvidia-light);
            margin: 0 10px 10px 0;
            padding: 15px;
            border-radius: 4px;
        }
        
        .server-card h3 {
            color: var(--nvidia-green);
            margin-top: 0;
        }
        
        .version-box {
            padding: 8px;
            margin: 5px 0;
            background-color: white;
            border-left: 3px solid var(--nvidia-green);
        }
        
        /* Version difference marker */
        .version-diff {
            position: relative;
            border-left: 3px solid var(--version-diff) !important;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            background-color: var(--nvidia-dark);
            color: white;
        }
        
        /* Scrollable TOC for many files */
        .toc-scroll {
            max-height: 300px;
            overflow-y: auto;
        }
        
        /* Style for the search filter in DataTables */
        .dataTables_filter input {
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        /* Style DataTables pagination */
        .dataTables_paginate .paginate_button {
            background-color: var(--nvidia-light);
            border: 1px solid #ddd;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .dataTables_paginate .paginate_button.current {
            background-color: var(--nvidia-green);
            color: white;
            border: 1px solid var(--nvidia-green);
        }
        
        /* Bold for differing values */
        .diff-value {
            font-weight: bold;
        }
        
        /* Ensure DataTables controls align left */
        .dataTables_wrapper .dataTables_length,
        .dataTables_wrapper .dataTables_filter,
        .dataTables_wrapper .dataTables_info,
        .dataTables_wrapper .dataTables_paginate {
            text-align: left;
            margin-bottom: 10px;
        }
        
        /* Ensure DataTables aligns with page content */
        .dataTables_wrapper {
            width: 100%;
            margin: 0 auto;
        }
        
        /* Table controls styling */
        .table-controls {
            margin: 15px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid var(--nvidia-green);
        }
        
        .table-controls input[type="text"] {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            width: 300px;
            margin-right: 10px;
        }
        
        .table-controls button {
            padding: 8px 15px;
            background-color: var(--nvidia-green);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 5px;
        }
        
        .table-controls button:hover {
            background-color: #5a9500;
        }
        
        .table-controls button.active {
            background-color: var(--nvidia-dark);
        }
        
        /* Sortable headers */
        th.sortable {
            cursor: pointer;
            position: relative;
            user-select: none;
        }
        
        th.sortable:hover {
            background-color: #555;
        }
        
        th.sortable::after {
            content: ' ↕';
            font-size: 12px;
            color: #ccc;
        }
        
        th.sortable.sort-asc::after {
            content: ' ↑';
            color: var(--nvidia-green);
        }
        
        th.sortable.sort-desc::after {
            content: ' ↓';
            color: var(--nvidia-green);
        }
        
        /* Hidden rows for filtering */
        tr.filtered-out {
            display: none;
        }
        
        /* Responsive tables */
        @media screen and (max-width: 1200px) {
            table {
                width: 100%;
                display: block;
                overflow-x: auto; /* Allow horizontal scrolling only if absolutely necessary */
            }
            .table-controls input[type="text"] {
                width: 200px;
            }
        }
    </style>
"""
        # JavaScript for smooth scrolling, sorting, and filtering - no external dependencies
        js_code = """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Smooth scrolling for TOC links
            const tocLinks = document.querySelectorAll('.toc a');
            tocLinks.forEach(function(link) {
                link.addEventListener('click', function(event) {
                    if (this.hash !== '') {
                        event.preventDefault();
                        const target = document.querySelector(this.hash);
                        if (target) {
                            target.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }
                    }
                });
            });
            
            // Initialize table functionality
            initializeTables();
        });
        
        function initializeTables() {
            const tables = document.querySelectorAll('table');
            tables.forEach(function(table, index) {
                if (table.querySelector('tbody')) {
                    addTableControls(table, index);
                    addSortingToHeaders(table);
                }
            });
        }
        
        function addTableControls(table, tableIndex) {
            const controlsDiv = document.createElement('div');
            controlsDiv.className = 'table-controls';
            controlsDiv.innerHTML = `
                <input type="text" id="filter-${tableIndex}" placeholder="🔍 Filter table..." onkeyup="filterTable(${tableIndex}, this.value)">
                <button onclick="filterByStatus(${tableIndex}, 'Modified')" id="btn-modified-${tableIndex}">Modified</button>
                <button onclick="filterByStatus(${tableIndex}, 'New Parameter')" id="btn-new-${tableIndex}">New</button>
                <button onclick="filterByStatus(${tableIndex}, 'Deleted Parameter')" id="btn-deleted-${tableIndex}">Deleted</button>
                <button onclick="clearFilters(${tableIndex})" id="btn-clear-${tableIndex}">Clear Filters</button>
            `;
            table.parentNode.insertBefore(controlsDiv, table);
        }
        
        function addSortingToHeaders(table) {
            const headers = table.querySelectorAll('th');
            headers.forEach(function(header, columnIndex) {
                header.classList.add('sortable');
                header.addEventListener('click', function() {
                    sortTable(table, columnIndex);
                });
            });
        }
        
        function filterTable(tableIndex, filterValue) {
            const tables = document.querySelectorAll('table');
            const table = tables[tableIndex];
            const rows = table.querySelectorAll('tbody tr');
            
            filterValue = filterValue.toLowerCase();
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(filterValue)) {
                    row.classList.remove('filtered-out');
                } else {
                    row.classList.add('filtered-out');
                }
            });
            
            // Clear status filter buttons
            clearStatusButtons(tableIndex);
        }
        
        function filterByStatus(tableIndex, status) {
            const tables = document.querySelectorAll('table');
            const table = tables[tableIndex];
            const rows = table.querySelectorAll('tbody tr');
            
            // Clear text filter
            document.getElementById(`filter-${tableIndex}`).value = '';
            
            // Clear all status buttons
            clearStatusButtons(tableIndex);
            
            // Activate current button
            const buttonId = status === 'Modified' ? `btn-modified-${tableIndex}` : 
                            status === 'New Parameter' ? `btn-new-${tableIndex}` : 
                            `btn-deleted-${tableIndex}`;
            document.getElementById(buttonId).classList.add('active');
            
            rows.forEach(function(row) {
                const statusCell = row.querySelector('td:last-child');
                if (statusCell && statusCell.textContent.includes(status.replace(' Parameter', ''))) {
                    row.classList.remove('filtered-out');
                } else {
                    row.classList.add('filtered-out');
                }
            });
        }
        
        function clearFilters(tableIndex) {
            const tables = document.querySelectorAll('table');
            const table = tables[tableIndex];
            const rows = table.querySelectorAll('tbody tr');
            
            // Clear text filter
            document.getElementById(`filter-${tableIndex}`).value = '';
            
            // Clear status buttons
            clearStatusButtons(tableIndex);
            
            // Show all rows
            rows.forEach(function(row) {
                row.classList.remove('filtered-out');
            });
        }
        
        function clearStatusButtons(tableIndex) {
            const buttons = [`btn-modified-${tableIndex}`, `btn-new-${tableIndex}`, `btn-deleted-${tableIndex}`];
            buttons.forEach(function(buttonId) {
                const button = document.getElementById(buttonId);
                if (button) {
                    button.classList.remove('active');
                }
            });
        }
        
        function sortTable(table, columnIndex) {
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const header = table.querySelectorAll('th')[columnIndex];
            
            // Determine sort direction
            let isAscending = true;
            if (header.classList.contains('sort-asc')) {
                isAscending = false;
            }
            
            // Clear all sort classes
            table.querySelectorAll('th').forEach(function(th) {
                th.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add appropriate sort class
            header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
            
            // Sort rows
            rows.sort(function(a, b) {
                const aText = a.querySelectorAll('td')[columnIndex].textContent.trim();
                const bText = b.querySelectorAll('td')[columnIndex].textContent.trim();
                
                // Handle status column specially
                if (columnIndex === 2) { // Status column
                    const statusOrder = {'Modified': 1, 'New': 2, 'Deleted': 3};
                    const aStatus = aText.includes('Modified') ? 1 : aText.includes('New') ? 2 : 3;
                    const bStatus = bText.includes('Modified') ? 1 : bText.includes('New') ? 2 : 3;
                    return isAscending ? aStatus - bStatus : bStatus - aStatus;
                }
                
                // Regular text comparison
                if (isAscending) {
                    return aText.localeCompare(bText);
                } else {
                    return bText.localeCompare(aText);
                }
            });
            
            // Re-append sorted rows
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        }
    </script>
"""

        # Build HTML without external dependencies
        html_head = f"""<!DOCTYPE html>
<html>
<head>
    <title>UFM Configuration Comparison Report</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {css}
</head>
<body>
    <header>
        <div class="container">
            <h1>UFM Configuration Comparison Report</h1>
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </header>
    
    <div class="container">
        <div class="server-info">
            <div class="server-card">
                <h3>Server 1: {comparisons['server1']['host']}</h3>
                <div class="version-box{' version-diff' if version_diff['ufm'] else ''}">UFM Version: {comparisons['ufm_version1']}</div>
                <div class="version-box{' version-diff' if version_diff['sharp'] else ''}">SHARP Version: {comparisons['sharp_version1']}</div>
                <div class="version-box{' version-diff' if version_diff['mft'] else ''}">MFT Version: {comparisons['mft_version1']}</div>
                <div class="version-box{' version-diff' if version_diff['opensm'] else ''}">OpenSM Version: {comparisons['opensm_version1']}</div>
            </div>
            <div class="server-card">
                <h3>Server 2: {comparisons['server2']['host']}</h3>
                <div class="version-box{' version-diff' if version_diff['ufm'] else ''}">UFM Version: {comparisons['ufm_version2']}</div>
                <div class="version-box{' version-diff' if version_diff['sharp'] else ''}">SHARP Version: {comparisons['sharp_version2']}</div>
                <div class="version-box{' version-diff' if version_diff['mft'] else ''}">MFT Version: {comparisons['mft_version2']}</div>
                <div class="version-box{' version-diff' if version_diff['opensm'] else ''}">OpenSM Version: {comparisons['opensm_version2']}</div>
            </div>
        </div>
        
        <h2>Table of Contents</h2>
        <div class="toc">
            <div class="toc-scroll">
                <ul>
"""

        # Build table of contents
        toc = ""
        for file_path, file_id in file_ids.items():
            toc += f'                    <li><a href="#{file_id}">{file_path}</a></li>\n'

        # Middle part of HTML
        html_middle = """
                </ul>
            </div>
        </div>
        
        <h2>Configuration Differences</h2>
"""

        # Build tables for each file
        tables = ""
        for file_comp in comparisons['files']:
            file_path = file_comp['file']
            file_id = file_ids[file_path]
            
            # Table header with server info - note that we may have swapped the servers
            tables += f"""
        <h3 id="{file_id}">{file_path}</h3>
        <table id="table-{file_id}">
            <thead>
                <tr>
                    <th>Server 1 ({comparisons['server1']['host']}: {comparisons['ufm_version1']})</th>
                    <th>Server 2 ({comparisons['server2']['host']}: {comparisons['ufm_version2']})</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""
            
            # Table rows
            for diff1, diff2, status in file_comp['diff']:
                is_diff1_missing = 'not found' in diff1
                is_diff2_missing = 'not found' in diff2
                
                # Apply bold to differing values by wrapping in a span with a class
                if not is_diff1_missing and not is_diff2_missing:
                    diff1_display = f'<span class="diff-value">{diff1}</span>'
                    diff2_display = f'<span class="diff-value">{diff2}</span>'
                else:
                    diff1_display = diff1
                    diff2_display = diff2
                
                # Set status class and badge
                row_class = ""
                status_badge_class = ""
                if status == "Modified":
                    row_class = "status-modified"
                    status_badge_class = "status-badge status-modified"
                elif status == "New Parameter added":
                    row_class = "status-new"
                    status_badge_class = "status-badge status-new"
                    status = "New Parameter"
                elif status == "Parameter Deleted":
                    row_class = "status-deleted"
                    status_badge_class = "status-badge status-deleted"
                    status = "Deleted Parameter"
                
                tables += f"""
                <tr class="{row_class}">
                    <td class="{'missing' if is_diff1_missing else 'diff'}">{diff1_display}</td>
                    <td class="{'missing' if is_diff2_missing else 'diff'}">{diff2_display}</td>
                    <td><span class="{status_badge_class}">{status}</span></td>
                </tr>"""
            
            tables += """
            </tbody>
        </table>"""

        # Footer part
        footer = f"""
        {js_code}
        
        <footer>
            <p>NVIDIA UFM Configuration Comparison Tool</p>
            <p>&copy; {datetime.now().strftime("%Y")} NVIDIA Corporation. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>
"""

        # Combine all parts
        html_content = html_head + toc + html_middle + tables + footer

        # Generate HTML report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Enhanced HTML report generated: {output_file}")

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise

def extract_version_info_from_configs(old_configs_dir, new_configs_dir):
    """Extract version information from configuration files"""
    
    # Initialize version dictionaries
    old_versions = {
        'ufm': 'Unknown',
        'sharp': 'Unknown', 
        'mft': 'Unknown',
        'opensm': 'Unknown'
    }
    
    new_versions = {
        'ufm': 'Unknown',
        'sharp': 'Unknown',
        'mft': 'Unknown', 
        'opensm': 'Unknown'
    }
    
    # Extract UFM versions
    old_ufm_version_file = os.path.join(old_configs_dir, "ufm_version")
    new_ufm_version_file = os.path.join(new_configs_dir, "ufm_version")
    
    if os.path.exists(old_ufm_version_file):
        try:
            with open(old_ufm_version_file, 'r') as f:
                content = f.read().strip()
                if content:
                    old_versions['ufm'] = content
                    print(f"  Old UFM version: {content}")
        except Exception as e:
            logger.warning(f"Error reading old UFM version: {e}")
    
    if os.path.exists(new_ufm_version_file):
        try:
            with open(new_ufm_version_file, 'r') as f:
                content = f.read().strip()
                if content:
                    new_versions['ufm'] = content
                    print(f"  New UFM version: {content}")
        except Exception as e:
            logger.warning(f"Error reading new UFM version: {e}")
    
    # Extract SHARP versions from sharp_am.cfg
    old_sharp_file = os.path.join(old_configs_dir, "sharp_am.cfg")
    new_sharp_file = os.path.join(new_configs_dir, "sharp_am.cfg")
    
    for file_path, versions_dict, label in [
        (old_sharp_file, old_versions, "Old"),
        (new_sharp_file, new_versions, "New")
    ]:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        if '# Version:' in line:
                            version = line.split(':')[1].strip()
                            versions_dict['sharp'] = version
                            print(f"  {label} SHARP version: {version}")
                            break
            except Exception as e:
                logger.warning(f"Error reading {label} SHARP version: {e}")
    
    # Extract MFT versions from mft_version file (extracted using mft -V command)
    old_mft_version_file = os.path.join(old_configs_dir, "mft_version")
    new_mft_version_file = os.path.join(new_configs_dir, "mft_version")
    
    for file_path, versions_dict, label in [
        (old_mft_version_file, old_versions, "Old"),
        (new_mft_version_file, new_versions, "New")
    ]:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        # Parse MFT version output from "mst version" command
                        # Example: "mst, mft 4.33.0-53, built on May 12 2025, 13:36:46. Git SHA Hash: N/A"
                        # We want to extract "mft 4.33.0-53"
                        version_match = re.search(r'mft\s+([0-9]+\.[0-9]+\.[0-9]+-[0-9]+)', content, re.IGNORECASE)
                        if version_match:
                            # Extract just the version number part (e.g., "4.33.0-53")
                            versions_dict['mft'] = version_match.group(1)
                            print(f"  {label} MFT version: {version_match.group(1)}")
                        else:
                            # Fallback: try to extract any version pattern
                            version_pattern = re.search(r'([0-9]+\.[0-9]+\.[0-9]+-[0-9]+)', content)
                            if version_pattern:
                                versions_dict['mft'] = version_pattern.group(1)
                                print(f"  {label} MFT version (parsed): {version_pattern.group(1)}")
                            else:
                                # If no specific pattern found, try to extract the first part after "mft"
                                mft_match = re.search(r'mft\s+([^,\s]+)', content, re.IGNORECASE)
                                if mft_match:
                                    versions_dict['mft'] = mft_match.group(1)
                                    print(f"  {label} MFT version (extracted): {mft_match.group(1)}")
                                else:
                                    # Last resort: use the first line
                                    versions_dict['mft'] = content.split('\n')[0]
                                    print(f"  {label} MFT version (raw): {content.split()[0] if content.split() else content}")
            except Exception as e:
                logger.warning(f"Error reading {label} MFT version: {e}")
        else:
            # Fallback: try to extract from mft.conf if mft_version file doesn't exist
            mft_conf_file = os.path.join(old_configs_dir if label == "Old" else new_configs_dir, "mft.conf")
            if os.path.exists(mft_conf_file):
                try:
                    with open(mft_conf_file, 'r') as f:
                        content = f.read()
                        # Look for version patterns in MFT config
                        version_match = re.search(r'version[:\s]+([0-9]+\.[0-9]+\.[0-9]+)', content, re.IGNORECASE)
                        if version_match:
                            versions_dict['mft'] = version_match.group(1)
                            print(f"  {label} MFT version (from config): {version_match.group(1)}")
                except Exception as e:
                    logger.warning(f"Error reading {label} MFT config: {e}")
    
    # Extract OpenSM versions from opensm.conf
    old_opensm_file = os.path.join(old_configs_dir, "opensm.conf")
    new_opensm_file = os.path.join(new_configs_dir, "opensm.conf")
    
    for file_path, versions_dict, label in [
        (old_opensm_file, old_versions, "Old"),
        (new_opensm_file, new_versions, "New")
    ]:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Look for OpenSM version in comments
                    version_match = re.search(r'opensm[:\s]+([0-9]+\.[0-9]+(?:\.[0-9]+)?)', content, re.IGNORECASE)
                    if version_match:
                        versions_dict['opensm'] = version_match.group(1)
                        print(f"  {label} OpenSM version: {version_match.group(1)}")
                    else:
                        # Look for version patterns in the file
                        for line in content.splitlines():
                            if 'opensm' in line.lower() and 'version' in line.lower():
                                version_pattern = re.search(r'([0-9]+\.[0-9]+(?:\.[0-9]+)?)', line)
                                if version_pattern:
                                    versions_dict['opensm'] = f"OpenSM {version_pattern.group(1)}"
                                    print(f"  {label} OpenSM version (from config): {version_pattern.group(1)}")
                                    break
            except Exception as e:
                logger.warning(f"Error reading {label} OpenSM version: {e}")
    
    return {
        'old_versions': old_versions,
        'new_versions': new_versions,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def save_version_info(version_data, results_dir):
    """Save version information to results directory"""
    
    # Create version comparison report
    version_report = f"""# UFM Version Comparison Report
Generated on: {version_data['timestamp']}

## Server 1 (Old Version) - UFM 6.20.0
- UFM Version: {version_data['old_versions']['ufm']}
- SHARP Version: {version_data['old_versions']['sharp']}
- MFT Version: {version_data['old_versions']['mft']}
- OpenSM Version: {version_data['old_versions']['opensm']}

## Server 2 (New Version) - UFM 6.21.0
- UFM Version: {version_data['new_versions']['ufm']}
- SHARP Version: {version_data['new_versions']['sharp']}
- MFT Version: {version_data['new_versions']['mft']}
- OpenSM Version: {version_data['new_versions']['opensm']}

## Version Changes Summary
"""
    
    # Add change analysis
    changes_found = False
    for component in ['ufm', 'sharp', 'mft', 'opensm']:
        old_ver = version_data['old_versions'][component]
        new_ver = version_data['new_versions'][component]
        if old_ver != new_ver:
            changes_found = True
            version_report += f"- {component.upper()}: {old_ver} → {new_ver}\n"
    
    if not changes_found:
        version_report += "- No version changes detected\n"
    
    # Save version report
    version_file = os.path.join(results_dir, "version_comparison.md")
    with open(version_file, 'w') as f:
        f.write(version_report)
    
    # Also save as JSON for programmatic access
    version_data_with_changes = version_data.copy()
    version_data_with_changes['changes'] = {}
    
    for component in ['ufm', 'sharp', 'mft', 'opensm']:
        if version_data['old_versions'][component] != version_data['new_versions'][component]:
            version_data_with_changes['changes'][component] = {
                'old': version_data['old_versions'][component],
                'new': version_data['new_versions'][component]
            }
    
    json_file = os.path.join(results_dir, "version_comparison.json")
    with open(json_file, 'w') as f:
        json.dump(version_data_with_changes, f, indent=2)
    
    print(f"{Fore.GREEN}Version information saved to:{Style.RESET_ALL}")
    print(f"  - {version_file}")
    print(f"  - {json_file}")

def send_email(receiver_email, file_path, version_data=None):
    """Send HTML report as email attachment"""
    try:
        # Get the report filename
        report_filename = os.path.basename(file_path)
        
        # Create message container
        msg = MIMEMultipart()
        msg['Subject'] = f'UFM Configuration Comparison Report - {datetime.now().strftime("%Y-%m-%d")}'
        msg['From'] = 'ufm-config-diff@nvidia.com'  # Change to a real email if needed
        msg['To'] = receiver_email
        
        # Create version comparison table for email body
        version_table = ""
        if version_data:
            version_table = f"""
            <h3>Component Version Comparison</h3>
            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; margin: 20px 0; font-family: Arial, sans-serif;">
                <thead>
                    <tr style="background-color: #333; color: white;">
                        <th>Component</th>
                        <th>Old Version</th>
                        <th>New Version</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>UFM</strong></td>
                        <td>{version_data['old_versions']['ufm']}</td>
                        <td>{version_data['new_versions']['ufm']}</td>
                        <td style="color: {'green' if version_data['old_versions']['ufm'] != version_data['new_versions']['ufm'] else 'gray'};">
                            {'Updated' if version_data['old_versions']['ufm'] != version_data['new_versions']['ufm'] else 'No Change'}
                        </td>
                    </tr>
                    <tr>
                        <td><strong>SHARP</strong></td>
                        <td>{version_data['old_versions']['sharp']}</td>
                        <td>{version_data['new_versions']['sharp']}</td>
                        <td style="color: {'green' if version_data['old_versions']['sharp'] != version_data['new_versions']['sharp'] else 'gray'};">
                            {'Updated' if version_data['old_versions']['sharp'] != version_data['new_versions']['sharp'] else 'No Change'}
                        </td>
                    </tr>
                    <tr>
                        <td><strong>MFT</strong></td>
                        <td>{version_data['old_versions']['mft']}</td>
                        <td>{version_data['new_versions']['mft']}</td>
                        <td style="color: {'green' if version_data['old_versions']['mft'] != version_data['new_versions']['mft'] else 'gray'};">
                            {'Updated' if version_data['old_versions']['mft'] != version_data['new_versions']['mft'] else 'No Change'}
                        </td>
                    </tr>
                    <tr>
                        <td><strong>OpenSM</strong></td>
                        <td>{version_data['old_versions']['opensm']}</td>
                        <td>{version_data['new_versions']['opensm']}</td>
                        <td style="color: {'green' if version_data['old_versions']['opensm'] != version_data['new_versions']['opensm'] else 'gray'};">
                            {'Updated' if version_data['old_versions']['opensm'] != version_data['new_versions']['opensm'] else 'No Change'}
                        </td>
                    </tr>
                </tbody>
            </table>
            """
        
        # Add message body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Hello,</p>
            <p>Please find attached the UFM Configuration Comparison Report.</p>
            {version_table}
            <p>This report was generated automatically by the UFM Configuration Differentiator Tool.</p>
            <p>Regards,<br>UFM Team</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        # Attach the HTML report
        with open(file_path, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="html")
            attachment.add_header('Content-Disposition', 'attachment', filename=report_filename)
            msg.attach(attachment)
        
        # Try to determine SMTP server - this is a simplification
        # In real environments, you'd need proper SMTP configuration
        try:
            # First try localhost
            server = smtplib.SMTP('localhost')
            server.send_message(msg)
            server.quit()
            logger.info(f"Email sent to {receiver_email}")
            print(f"{Fore.GREEN}Email with report sent to {receiver_email}{Style.RESET_ALL}")
            return True
        except Exception as e:
            # Try to use an environment variable for SMTP server
            smtp_server = os.environ.get('SMTP_SERVER')
            if smtp_server:
                try:
                    server = smtplib.SMTP(smtp_server)
                    server.send_message(msg)
                    server.quit()
                    logger.info(f"Email sent to {receiver_email} using {smtp_server}")
                    print(f"{Fore.GREEN}Email with report sent to {receiver_email}{Style.RESET_ALL}")
                    return True
                except Exception as e:
                    logger.error(f"Failed to send email using {smtp_server}: {e}")
            
            logger.error(f"Failed to send email: {e}")
            print(f"{Fore.YELLOW}Warning: Could not send email. Please make sure SMTP server is accessible.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}You may set SMTP_SERVER environment variable to specify your SMTP server.{Style.RESET_ALL}")
            return False
    except Exception as e:
        logger.error(f"Error preparing email: {e}")
        print(f"{Fore.YELLOW}Warning: Failed to prepare email: {e}{Style.RESET_ALL}")
        return False

def main():
    try:
        parser = argparse.ArgumentParser(
            description='Compare UFM configurations between two Docker images', 
            formatter_class=ColorHelpFormatter
        )
        
        # Required arguments
        parser.add_argument('old_image', help='Path to old UFM Docker image (.gz file)')
        parser.add_argument('new_image', help='Path to new UFM Docker image (.gz file)')
        parser.add_argument('license_file', help='Path to UFM license file')
        
        # Optional arguments
        parser.add_argument('--fabric-interface', help='Fabric interface to use for UFM')
        parser.add_argument('--mgmt-interface', help='Management interface to use for UFM')
        parser.add_argument('--email', 
                           help='Email address to send the report to. Requires an available SMTP server. '
                                'Set SMTP_SERVER environment variable to specify a custom server.')
        parser.add_argument('--yes', '-y', action='store_true',
                            help='Automatically answer YES to all prompts without user intervention')
        parser.add_argument('output_file', nargs='?', 
                            default=f'ufm_comparison_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html',
                            help='Output HTML file path (optional)')
        
        args = parser.parse_args()
        
        # Import Docker manager
        from ufm_config_diff.docker_operations import DockerManager
        
        # Create Docker manager
        docker_manager = DockerManager(
            args.old_image,
            args.new_image,
            args.license_file,
            fabric_interface=args.fabric_interface,
            mgmt_interface=args.mgmt_interface,
            auto_yes=args.yes
        )
        
        # Compare Docker images and get paths to extracted configs
        config_dirs = docker_manager.compare_docker_images()
        
        # Create a dummy server structure to reuse the report generation
        server1 = {
            'host': f"UFM Docker Old Image ({os.path.basename(args.old_image)})",
            'username': None,
            'password': None
        }
        
        server2 = {
            'host': f"UFM Docker New Image ({os.path.basename(args.new_image)})",
            'username': None,
            'password': None
        }
        
        # Create comparisons structure
        comparisons = {
            'server1': server1,
            'server2': server2,
            'files': []
        }
        
        # Compare configuration files directly from the extracted directories
        # First, handle files that exist in both directories or only in old directory
        # Filter out ufm_version file (used only for version extraction, not comparison)
        old_config_files = [f for f in os.listdir(config_dirs['old_configs_dir']) if f != 'ufm_version']
        for config_file in old_config_files:
            old_config_path = os.path.join(config_dirs['old_configs_dir'], config_file)
            new_config_path = os.path.join(config_dirs['new_configs_dir'], config_file)
            
            if os.path.isfile(old_config_path) and os.path.isfile(new_config_path):
                # Read file contents
                with open(old_config_path, 'r', errors='replace') as f:
                    old_content = f.read().splitlines()
                
                with open(new_config_path, 'r', errors='replace') as f:
                    new_content = f.read().splitlines()
                
                # Use similar parsing logic as in compare_files
                def parse_config(lines):
                    params = {}
                    for line in lines:
                        line = line.strip()
                        # Skip empty lines, comments, and UFM version lines
                        if (not line or 
                            line.startswith('#') or 
                            line.startswith(';') or 
                            'UFM Version' in line):  # Skip UFM Version lines
                            continue
                        # Try to split on common parameter separators (=, :, space)
                        for separator in ['=', ':', ' ']:
                            if separator in line:
                                key, value = line.split(separator, 1)
                                key = key.strip()
                                value = value.strip()
                                params[key] = value
                                break
                    return params
                
                params1 = parse_config(old_content)
                params2 = parse_config(new_content)
                
                # Compare parameters
                diff = []
                # Check all keys from first file
                for key in params1:
                    if key in params2:
                        if params1[key] != params2[key]:
                            diff.append((
                                f"{key}: {params1[key]}",
                                f"{key}: {params2[key]}",
                                "Modified"
                            ))
                    else:
                        diff.append((f"{key}: {params1[key]}", "Parameter not found", "Parameter Deleted"))
                
                # Check for parameters only in second file
                for key in params2:
                    if key not in params1:
                        diff.append(("Parameter not found", f"{key}: {params2[key]}", "New Parameter added"))
                
                # Sort by status: Modified, New Parameter, Parameter Deleted
                def sort_key(item):
                    status = item[2]
                    if status == "Modified":
                        return 0
                    elif status == "New Parameter added":
                        return 1
                    else:  # "Parameter Deleted"
                        return 2
                        
                diff.sort(key=sort_key)
                
                if diff:
                    comparisons['files'].append({
                        'file': f"/opt/ufm/ufm_config_files/conf/{config_file}",
                        'diff': diff
                    })
            elif os.path.isfile(old_config_path):
                # File exists only in old config
                comparisons['files'].append({
                    'file': f"/opt/ufm/ufm_config_files/conf/{config_file}",
                    'diff': [(f"File exists in {os.path.basename(args.old_image)}", 
                              f"File not found in {os.path.basename(args.new_image)}", 
                              "Parameter Deleted")]
                })
        
        # Now, handle files that exist only in the new config directory
        # Filter out ufm_version file (used only for version extraction, not comparison)
        new_config_files = [f for f in os.listdir(config_dirs['new_configs_dir']) if f != 'ufm_version']
        for config_file in new_config_files:
            old_config_path = os.path.join(config_dirs['old_configs_dir'], config_file)
            new_config_path = os.path.join(config_dirs['new_configs_dir'], config_file)
            
            # Only process if this file doesn't exist in the old directory
            if os.path.isfile(new_config_path) and not os.path.isfile(old_config_path):
                comparisons['files'].append({
                    'file': f"/opt/ufm/ufm_config_files/conf/{config_file}",
                    'diff': [(f"File not found in {os.path.basename(args.old_image)}", 
                              f"File exists in {os.path.basename(args.new_image)}", 
                              "New Parameter added")]
                })
        
        # Extract version information from configuration files
        print(f"{Fore.CYAN}Extracting version information from configuration files...{Style.RESET_ALL}")
        version_data = extract_version_info_from_configs(config_dirs['old_configs_dir'], config_dirs['new_configs_dir'])
        
        # Save version information to results directory
        if 'results_dir' in config_dirs:
            save_version_info(version_data, config_dirs['results_dir'])
        
        # Generate UFM version info for the report - use extracted version data
        comparisons['ufm_version1'] = version_data['old_versions']['ufm'] if version_data['old_versions']['ufm'] != 'Unknown' else os.path.basename(args.old_image)
        comparisons['ufm_version2'] = version_data['new_versions']['ufm'] if version_data['new_versions']['ufm'] != 'Unknown' else os.path.basename(args.new_image)
        comparisons['sharp_version1'] = version_data['old_versions']['sharp']
        comparisons['sharp_version2'] = version_data['new_versions']['sharp']
        comparisons['mft_version1'] = version_data['old_versions']['mft']
        comparisons['mft_version2'] = version_data['new_versions']['mft']
        comparisons['opensm_version1'] = version_data['old_versions']['opensm']
        comparisons['opensm_version2'] = version_data['new_versions']['opensm']
        comparisons['is_swapped'] = False
        
        # Debug: Print the version data being used for the report
        print(f"{Fore.CYAN}Version data for HTML report:{Style.RESET_ALL}")
        print(f"  UFM: {comparisons['ufm_version1']} -> {comparisons['ufm_version2']}")
        print(f"  SHARP: {comparisons['sharp_version1']} -> {comparisons['sharp_version2']}")
        print(f"  MFT: {comparisons['mft_version1']} -> {comparisons['mft_version2']}")
        print(f"  OpenSM: {comparisons['opensm_version1']} -> {comparisons['opensm_version2']}")
        
        # Generate HTML report
        generate_html_report(server1, server2, comparisons, args.output_file)
        
        # Move HTML report to results directory if it exists
        if 'results_dir' in config_dirs:
            results_dir = config_dirs['results_dir']
            report_filename = os.path.basename(args.output_file)
            results_report_path = os.path.join(results_dir, report_filename)
            
            # Copy the report to results directory
            if os.path.exists(args.output_file):
                shutil.copy2(args.output_file, results_report_path)
                logger.info(f"HTML report copied to {results_report_path}")
                print(f"{Fore.GREEN}HTML report copied to results directory: {results_report_path}{Style.RESET_ALL}")
        
        # Get the absolute path for the report file
        abs_path = os.path.abspath(args.output_file)
        logger.info(f"Docker image comparison report generated: {abs_path}")
        print(f"Docker image comparison report generated: {abs_path}")
        
        # Send email if requested
        if args.email:
            send_email(args.email, abs_path, version_data)
        
        print(f"{Fore.GREEN}Script completed successfully!{Style.RESET_ALL}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 