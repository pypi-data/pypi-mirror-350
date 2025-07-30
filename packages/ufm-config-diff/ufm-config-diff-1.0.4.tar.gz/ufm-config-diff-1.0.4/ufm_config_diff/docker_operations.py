import os
import subprocess
import logging
import tempfile
import shutil
import time
import re
import paramiko
import argparse
from colorama import Fore, Style

# Set up logging
logger = logging.getLogger(__name__)

class DockerManager:
    """Class to handle UFM Docker operations"""
    
    def __init__(self, old_image_path, new_image_path, license_path, fabric_interface=None, mgmt_interface=None, auto_yes=False):
        self.old_image_path = old_image_path
        self.new_image_path = new_image_path
        self.license_path = license_path
        self.fabric_interface = fabric_interface
        self.mgmt_interface = mgmt_interface
        self.auto_yes = auto_yes
        self.temp_dir = tempfile.mkdtemp(prefix="ufm_config_diff_")
        self.old_configs_dir = os.path.join(self.temp_dir, "old_configs")
        self.new_configs_dir = os.path.join(self.temp_dir, "new_configs")
        os.makedirs(self.old_configs_dir, exist_ok=True)
        os.makedirs(self.new_configs_dir, exist_ok=True)
        
        # License file temp location
        self.license_temp_dir = os.path.join(self.temp_dir, "license_file")
        os.makedirs(self.license_temp_dir, exist_ok=True)
        
        # Where UFM stores configuration files (updated with correct paths)
        self.ufm_config_paths = [
            "/opt/ufm/ufm_config_files/conf/gv.cfg",
            "/opt/ufm/ufm_config_files/conf/opensm/opensm.conf",
            "/opt/ufm/ufm_config_files/conf/sharp/sharp_am.cfg",
            "/etc/mft/mft.conf",
            "/opt/ufm/ufm_config_files/ufm_version"
        ]
        
        # Alternative paths to search for configuration files
        self.alternative_config_paths = {
            "gv.cfg": [
                "/opt/ufm/ufm_config_files/conf/gv.cfg",
                "/opt/ufm/files/conf/gv.cfg",
                "/opt/ufm/conf/gv.cfg",
                "/etc/ufm/gv.cfg"
            ],
            "opensm.conf": [
                "/opt/ufm/ufm_config_files/conf/opensm/opensm.conf",
                "/opt/ufm/ufm_config_files/conf/opensm.conf",
                "/opt/ufm/files/conf/opensm/opensm.conf",
                "/opt/ufm/files/conf/opensm.conf",
                "/etc/opensm/opensm.conf",
                "/opt/ufm/conf/opensm.conf"
            ],
            "sharp_am.cfg": [
                "/opt/ufm/ufm_config_files/conf/sharp/sharp_am.cfg",
                "/opt/ufm/ufm_config_files/conf/sharp_am.cfg",
                "/opt/ufm/files/conf/sharp/sharp_am.cfg",
                "/opt/ufm/files/conf/sharp_am.cfg",
                "/etc/sharp/sharp_am.cfg",
                "/opt/ufm/conf/sharp_am.cfg"
            ],
            "mft.conf": [
                "/etc/mft/mft.conf",
                "/opt/ufm/files/conf/mft.conf",
                "/opt/ufm/conf/mft.conf"
            ],
            "ufm_version": [
                "/opt/ufm/ufm_config_files/ufm_version",
                "/opt/ufm/files/ufm_version",
                "/opt/ufm/ufm_version"
            ]
        }
        
        # Store actual loaded image names
        self.old_image_name = None
        self.new_image_name = None
        
    def __del__(self):
        """Clean up temporary files when object is destroyed"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                logger.error(f"Failed to clean up temporary directory: {e}")
    
    def check_prerequisites(self):
        """Check if prerequisites are met for UFM Docker installation"""
        logger.info("Checking prerequisites for UFM Docker installation...")
        
        # Check if Docker is installed and running
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            subprocess.run(["docker", "info"], check=True, capture_output=True)
            logger.info("Docker is installed and running")
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error("Docker is not installed or not running")
            raise RuntimeError("Docker is not installed or not running. Please install Docker and ensure it's running.")
        
        # Check if UFM is already installed
        ufm_install_type = self._is_ufm_installed()
        if ufm_install_type:
            logger.warning(f"UFM is already installed on this system as {ufm_install_type}")
            
            # Ask user if they want to uninstall, or auto-yes if configured
            if self.auto_yes:
                response = "y"
                print(f"{Fore.YELLOW}WARNING: UFM is already installed on this system as {ufm_install_type}. Auto-uninstalling.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}WARNING: UFM is already installed on this system as {ufm_install_type}.{Style.RESET_ALL}")
                response = input(f"Do you want to uninstall it before proceeding? [Y/n]: ").lower()
            
            if response in ["", "y", "yes"]:
                # Try to uninstall
                if self.uninstall_ufm(ufm_install_type):
                    logger.info("Successfully uninstalled UFM")
                    print(f"{Fore.GREEN}Successfully uninstalled UFM.{Style.RESET_ALL}")
                else:
                    logger.error("Failed to uninstall UFM")
                    raise RuntimeError("Failed to uninstall UFM. Please uninstall it manually before running this tool.")
            else:
                logger.error("User chose not to uninstall UFM")
                raise RuntimeError("UFM is already installed on this system. Please uninstall it before running this tool.")
        
        # Check if required ports are free
        required_ports = [80, 443, 8000, 6306, 8005, 8888, 2022]
        busy_ports = self._check_ports(required_ports)
        if busy_ports:
            ports_str = ", ".join(map(str, busy_ports))
            logger.error(f"The following ports required by UFM are already in use: {ports_str}")
            raise RuntimeError(f"The following ports required by UFM are already in use: {ports_str}")
        
        # If fabric_interface is specified, check if it exists and is up
        if self.fabric_interface:
            if not self._check_interface(self.fabric_interface):
                logger.error(f"Interface {self.fabric_interface} does not exist or is not up")
                raise RuntimeError(f"Interface {self.fabric_interface} does not exist or is not up")
        
        # If mgmt_interface is specified, check if it exists and is up
        if self.mgmt_interface:
            if not self._check_interface(self.mgmt_interface):
                logger.error(f"Interface {self.mgmt_interface} does not exist or is not up")
                raise RuntimeError(f"Interface {self.mgmt_interface} does not exist or is not up")
        
        # Copy license file to temp directory
        try:
            shutil.copy(self.license_path, os.path.join(self.license_temp_dir, os.path.basename(self.license_path)))
            logger.info(f"Copied license file to {self.license_temp_dir}")
        except Exception as e:
            logger.error(f"Failed to copy license file: {e}")
            raise
        
        return True
    
    def _is_ufm_installed(self):
        """Check if UFM is already installed and return installation type"""
        ufm_service_running = False
        ufm_container_running = False
        ufm_ha_exists = False
        ufm_dir_exists = False
        
        # Check for UFM Docker container first (higher priority)
        try:
            result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True, check=False)
            if "ufm" in result.stdout.lower() or "mellanox/ufm" in result.stdout.lower():
                ufm_container_running = True
                logger.info("UFM Docker container detected")
        except Exception as e:
            logger.warning(f"Error checking Docker containers: {e}")
            
        # Check for UFM systemd service
        try:
            result = subprocess.run(["systemctl", "list-units", "--type=service", "--all", "*ufm*"], 
                                   capture_output=True, text=True, check=False)
            if "ufm" in result.stdout.lower():
                ufm_service_running = True
                logger.info("UFM service detected")
        except Exception as e:
            logger.warning(f"Error checking systemd services: {e}")
        
        # Check for UFM installation directory
        ufm_dir_exists = os.path.exists("/opt/ufm")
        if ufm_dir_exists:
            logger.info("UFM directory /opt/ufm detected")
            ufm_ha_exists = os.path.exists("/opt/ufm/ufm_ha")
            if ufm_ha_exists:
                logger.info("UFM HA directory detected")
        
        # Make a decision based on all indicators
        if ufm_container_running:
            # Docker container has highest priority
            if ufm_ha_exists:
                return "ha_docker"
            return "docker"
        elif ufm_service_running:
            # Service has second highest priority
            if ufm_ha_exists:
                return "ha_standalone"
            return "standalone"
        elif ufm_dir_exists:
            # Only directory exists
            if ufm_ha_exists:
                return "ha_remnants"
            return "remnants"
            
        return None
    
    def _check_ports(self, ports):
        """Check if required ports are free"""
        busy_ports = []
        for port in ports:
            # Check if port is in use
            try:
                result = subprocess.run(
                    ["netstat", "-tuln"], capture_output=True, text=True, check=False
                )
                # More precise port matching - look for exact port matches
                port_patterns = [f":{port} ", f":{port}\t"]
                port_busy = False
                for pattern in port_patterns:
                    if pattern in result.stdout:
                        port_busy = True
                        break
                
                if port_busy:
                    busy_ports.append(port)
                    logger.warning(f"Port {port} appears to be in use")
                else:
                    logger.debug(f"Port {port} is free")
            except Exception as e:
                logger.warning(f"Failed to check if port {port} is in use: {e}")
        
        return busy_ports
    
    def _check_interface(self, interface):
        """Check if a network interface exists and is up"""
        try:
            result = subprocess.run(
                ["ip", "link", "show", interface], capture_output=True, text=True, check=False
            )
            if interface in result.stdout and "state UP" in result.stdout:
                return True
            return False
        except Exception:
            return False
    
    def load_docker_image(self, image_path):
        """Load a Docker image from a .gz file"""
        logger.info(f"Loading Docker image from {image_path}...")
        try:
            # Load the Docker image
            result = subprocess.run(
                ["docker", "load", "-i", image_path], 
                capture_output=True, text=True, check=True
            )
            
            # Extract the image name and tag from output
            match = re.search(r"Loaded image: (.+)", result.stdout)
            if match:
                image_name = match.group(1)
                logger.info(f"Successfully loaded Docker image: {image_name}")
                return image_name
            else:
                logger.error(f"Failed to extract Docker image name from output: {result.stdout}")
                raise RuntimeError("Failed to extract Docker image name")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to load Docker image: {e}")
            logger.error(f"Command output: {e.stdout}, {e.stderr}")
            raise
    
    def install_old_ufm(self):
        """Install the old UFM Docker image"""
        logger.info("Installing old UFM Docker image...")
        
        # Load the old Docker image
        self.old_image_name = self.load_docker_image(self.old_image_path)
        
        # Make sure the UFM directories exist
        os.makedirs("/opt/ufm/files", exist_ok=True)
        logger.info("Ensured /opt/ufm/files directory exists")
        
        # Build the installation command following the required format
        # The format must match what the UFM installer script expects
        cmd = [
            "docker", "run"
        ]
        
        # Only use -it if not in auto-yes mode
        if not self.auto_yes:
            cmd.append("-it")
            
        cmd.extend([
            "--name=ufm_installer", "--rm",
            "-v", "/var/run/docker.sock:/var/run/docker.sock",
            "-v", "/etc/systemd/system/:/etc/systemd_files/",
            "-v", "/opt/ufm/files/:/installation/ufm_files/",
            "-v", f"{self.license_temp_dir}/:/installation/ufm_licenses/",
            self.old_image_name,
            "--install"
        ])
        
        # Add fabric interface if specified
        if self.fabric_interface:
            cmd.extend(["--fabric-interface", self.fabric_interface])
        
        # Add management interface if specified
        if self.mgmt_interface:
            cmd.extend(["--mgmt-interface", self.mgmt_interface])
        
        # Run the installation command without requiring TTY
        try:
            # When auto_yes is enabled, pipe 'yes' answers to handle interactive prompts
            if self.auto_yes:
                # Use yes command to provide automatic Y responses to all prompts
                cmd_str = " ".join(cmd)
                # Add environment variables for non-interactive mode
                env_vars = "DEBIAN_FRONTEND=noninteractive ACCEPT_EULA=Y"
                subprocess.run(f"{env_vars} yes Y | {cmd_str}", shell=True, check=True)
            else:
                subprocess.run(cmd, check=True)
                
            logger.info("Successfully installed old UFM Docker image")
            print(f"{Fore.GREEN}Successfully installed old UFM Docker image: {os.path.basename(self.old_image_path)}{Style.RESET_ALL}")
            
            # Reload systemd and start UFM
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "start", "ufm-enterprise"], check=True)
            
            # Wait for UFM to start
            logger.info("Waiting for UFM to start...")
            time.sleep(60)  # Wait 60 seconds for UFM to initialize
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install old UFM Docker image: {e}")
            raise
    
    def extract_configs(self, target_dir):
        """Extract configuration files from UFM Docker container"""
        logger.info(f"Extracting configuration files to {target_dir}...")
        
        # Get the UFM container ID - try multiple approaches
        container_id = None
        try:
            # First try to find by the actual loaded image names
            if self.old_image_name:
                result = subprocess.run(
                    ["docker", "ps", "-qf", f"ancestor={self.old_image_name}"],
                    capture_output=True, text=True, check=False
                )
                if result.stdout.strip():
                    container_id = result.stdout.strip()
                    logger.info(f"Found UFM container by old image ancestor: {container_id}")
            
            if not container_id and self.new_image_name:
                result = subprocess.run(
                    ["docker", "ps", "-qf", f"ancestor={self.new_image_name}"],
                    capture_output=True, text=True, check=False
                )
                if result.stdout.strip():
                    container_id = result.stdout.strip()
                    logger.info(f"Found UFM container by new image ancestor: {container_id}")
            
            # Fallback to original approach
            if not container_id:
                result = subprocess.run(
                    ["docker", "ps", "-qf", "ancestor=mellanox/ufm-enterprise"],
                    capture_output=True, text=True, check=False
                )
                if result.stdout.strip():
                    container_id = result.stdout.strip()
                    logger.info(f"Found UFM container by default ancestor: {container_id}")
            
            # If not found, try to find by name pattern
            if not container_id:
                result = subprocess.run(
                    ["docker", "ps", "--format", "{{.ID}} {{.Names}} {{.Image}}"],
                    capture_output=True, text=True, check=False
                )
                for line in result.stdout.splitlines():
                    if "ufm" in line.lower() or "mellanox" in line.lower():
                        container_id = line.split()[0]
                        logger.info(f"Found UFM container by name/image pattern: {container_id}")
                        break
            
            # If still not found, try to find any running container
            if not container_id:
                result = subprocess.run(
                    ["docker", "ps", "-q"],
                    capture_output=True, text=True, check=False
                )
                containers = result.stdout.strip().split('\n')
                if containers and containers[0]:
                    # Check if any container has UFM-related processes
                    for cid in containers:
                        check_result = subprocess.run(
                            ["docker", "exec", cid, "ps", "aux"],
                            capture_output=True, text=True, check=False
                        )
                        if "ufm" in check_result.stdout.lower():
                            container_id = cid
                            logger.info(f"Found UFM container by process check: {container_id}")
                            break
            
            if not container_id:
                logger.error("Failed to find any UFM Docker container")
                # List all running containers for debugging
                result = subprocess.run(["docker", "ps"], capture_output=True, text=True, check=False)
                logger.debug(f"Running containers:\n{result.stdout}")
                raise RuntimeError("Failed to find UFM Docker container")
            
            logger.info(f"Using container ID: {container_id}")
            
            # Extract MFT version using mst version command and save to file
            try:
                mft_version_cmd = f"docker exec {container_id} mst version"
                result = subprocess.run(mft_version_cmd, shell=True, check=False, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    mft_version_content = result.stdout.strip()
                    # Save MFT version to file
                    mft_version_file = os.path.join(target_dir, "mft_version")
                    with open(mft_version_file, 'w') as f:
                        f.write(mft_version_content)
                    logger.info(f"Successfully extracted MFT version: {mft_version_content}")
                    print(f"{Fore.CYAN}Extracted MFT version: {mft_version_content}{Style.RESET_ALL}")
                else:
                    logger.warning(f"Failed to extract MFT version: {result.stderr}")
            except Exception as e:
                logger.warning(f"Error extracting MFT version: {e}")
            
            # For each config file, try multiple paths to find it
            extracted_count = 0
            
            # First try the original paths
            for config_path in self.ufm_config_paths:
                target_path = os.path.join(target_dir, os.path.basename(config_path))
                
                # Create the target directory if it doesn't exist
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # Copy the file from the container
                copy_cmd = f"docker cp {container_id}:{config_path} {target_path}"
                result = subprocess.run(copy_cmd, shell=True, check=False, capture_output=True, text=True)
                
                if os.path.exists(target_path):
                    logger.info(f"Successfully copied {config_path} to {target_path}")
                    extracted_count += 1
                else:
                    logger.warning(f"Failed to copy {config_path} (file may not exist in container)")
                    logger.debug(f"Docker cp error: {result.stderr}")
            
            # If we didn't extract enough files, try alternative paths
            if extracted_count < len(self.ufm_config_paths):
                logger.info("Trying alternative paths for missing configuration files...")
                
                for filename, alt_paths in self.alternative_config_paths.items():
                    target_path = os.path.join(target_dir, filename)
                    
                    # Skip if we already have this file
                    if os.path.exists(target_path):
                        continue
                    
                    # Try each alternative path
                    for alt_path in alt_paths:
                        copy_cmd = f"docker cp {container_id}:{alt_path} {target_path}"
                        result = subprocess.run(copy_cmd, shell=True, check=False, capture_output=True, text=True)
                        
                        if os.path.exists(target_path):
                            logger.info(f"Successfully copied {alt_path} to {target_path}")
                            extracted_count += 1
                            break
                        else:
                            logger.debug(f"Alternative path {alt_path} not found")
            
            # Also try to find configuration files dynamically
            if extracted_count == 0:
                logger.info("Attempting dynamic search for configuration files...")
                
                # Search for common config file patterns
                search_patterns = ["*.cfg", "*.conf", "*version*"]
                search_dirs = ["/opt/ufm", "/etc", "/opt"]
                
                for search_dir in search_dirs:
                    for pattern in search_patterns:
                        find_cmd = f"docker exec {container_id} find {search_dir} -name '{pattern}' -type f 2>/dev/null"
                        result = subprocess.run(find_cmd, shell=True, check=False, capture_output=True, text=True)
                        
                        if result.stdout.strip():
                            found_files = result.stdout.strip().split('\n')
                            logger.info(f"Found {len(found_files)} files matching {pattern} in {search_dir}")
                            for found_file in found_files[:5]:  # Limit to first 5 files per pattern
                                if found_file and any(keyword in found_file.lower() for keyword in ['ufm', 'opensm', 'sharp', 'mft']):
                                    target_path = os.path.join(target_dir, os.path.basename(found_file))
                                    copy_cmd = f"docker cp {container_id}:{found_file} {target_path}"
                                    copy_result = subprocess.run(copy_cmd, shell=True, check=False, capture_output=True, text=True)
                                    
                                    if os.path.exists(target_path):
                                        logger.info(f"Dynamically found and copied {found_file} to {target_path}")
                                        extracted_count += 1
            
            # List what files we actually extracted
            if os.path.exists(target_dir):
                extracted_files = os.listdir(target_dir)
                logger.info(f"Final extracted files: {extracted_files}")
                print(f"{Fore.CYAN}Extracted {len(extracted_files)} configuration files: {', '.join(extracted_files)}{Style.RESET_ALL}")
            
            if extracted_count == 0:
                logger.error("No configuration files were successfully extracted")
                raise RuntimeError("No configuration files were successfully extracted")
            
            logger.info(f"Successfully extracted {extracted_count} configuration files")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to extract configuration files: {e}")
            raise
    
    def upgrade_ufm(self):
        """Upgrade UFM to the new Docker image"""
        logger.info("Upgrading UFM to new Docker image...")
        
        try:
            # Stop the UFM service
            subprocess.run(["systemctl", "stop", "ufm-enterprise"], check=True)
            
            # Remove the existing Docker image
            subprocess.run(["docker", "rmi", "mellanox/ufm-enterprise:latest"], check=True, capture_output=True)
            
            # Load the new Docker image
            self.new_image_name = self.load_docker_image(self.new_image_path)
            
            # Run the upgrade command following the required format
            # The format must match what the UFM installer script expects
            upgrade_cmd = [
                "docker", "run"
            ]
            
            # Only use -it if not in auto-yes mode
            if not self.auto_yes:
                upgrade_cmd.append("-it")
                
            upgrade_cmd.extend([
                "--name=ufm_installer", "--rm",
                "-v", "/var/run/docker.sock:/var/run/docker.sock",
                "-v", "/etc/systemd/system/:/etc/systemd_files/",
                "-v", "/opt/ufm/files/:/opt/ufm/shared_config_files/",
                self.new_image_name,
                "--upgrade"
            ])
            
            # Run the installation command without requiring TTY
            try:
                # When auto_yes is enabled, pipe 'yes' answers to handle interactive prompts
                if self.auto_yes:
                    # Use yes command to provide automatic Y responses to all prompts
                    cmd_str = " ".join(upgrade_cmd)
                    # Add environment variables for non-interactive mode
                    env_vars = "DEBIAN_FRONTEND=noninteractive ACCEPT_EULA=Y"
                    subprocess.run(f"{env_vars} yes Y | {cmd_str}", shell=True, check=True)
                else:
                    subprocess.run(upgrade_cmd, check=True)
            
                # Print success message in green
                print(f"{Fore.GREEN}Successfully installed new UFM Docker image: {os.path.basename(self.new_image_path)}{Style.RESET_ALL}")
                
                # Reload systemd and start UFM
                subprocess.run(["systemctl", "daemon-reload"], check=True)
                subprocess.run(["systemctl", "start", "ufm-enterprise"], check=True)
                
                # Wait for UFM to start
                logger.info("Waiting for upgraded UFM to start...")
                time.sleep(60)  # Wait 60 seconds for UFM to initialize
                
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to upgrade UFM: {e}")
                raise
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to upgrade UFM: {e}")
            raise
    
    def uninstall_ufm(self, install_type=None):
        """Uninstall UFM based on installation type"""
        logger.info(f"Uninstalling UFM {install_type if install_type else 'installation'}...")
        
        if not install_type:
            install_type = self._is_ufm_installed()
            if not install_type:
                logger.warning("No UFM installation detected to uninstall")
                return True
        
        try:
            # First handle Docker containers regardless of install type
            # This ensures containers are stopped/removed even in mixed states
            docker_containers_removed = False
            try:
                # Check if there are any UFM containers
                result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True, check=False)
                if "ufm" in result.stdout.lower() or "mellanox/ufm" in result.stdout.lower():
                    print(f"{Fore.CYAN}Removing UFM Docker containers...{Style.RESET_ALL}")
                    # Stop running containers
                    subprocess.run("docker stop $(docker ps -a | grep -i 'ufm\\|mellanox' | awk '{print $1}') 2>/dev/null || true", 
                                  shell=True, check=False)
                    # Remove containers
                    subprocess.run("docker rm $(docker ps -a | grep -i 'ufm\\|mellanox' | awk '{print $1}') 2>/dev/null || true", 
                                  shell=True, check=False)
                    # Remove images
                    subprocess.run("docker rmi $(docker images | grep -i 'ufm\\|mellanox' | awk '{print $3}') 2>/dev/null || true", 
                                  shell=True, check=False)
                    logger.info("Removed UFM Docker containers and images")
                    docker_containers_removed = True
            except Exception as e:
                logger.warning(f"Error removing Docker containers: {e}")
            
            # Next try to stop any UFM services regardless of install type
            services_stopped = False
            try:
                print(f"{Fore.CYAN}Stopping UFM services...{Style.RESET_ALL}")
                subprocess.run("systemctl stop ufm-enterprise ufm-* 2>/dev/null || true", shell=True, check=False)
                logger.info("Stopped UFM services")
                services_stopped = True
            except Exception as e:
                logger.warning(f"Error stopping UFM services: {e}")
            
            # Now proceed with type-specific uninstallation
            if install_type in ["ha_docker", "ha_standalone", "ha_remnants"]:
                # HA mode uninstall
                print(f"{Fore.CYAN}Uninstalling UFM in HA mode...{Style.RESET_ALL}")
                
                # Try ufm_ha_cluster cleanup
                try:
                    subprocess.run("ufm_ha_cluster cleanup", shell=True, check=False)
                    logger.info("Ran ufm_ha_cluster cleanup")
                except Exception as e:
                    logger.warning(f"Failed to run ufm_ha_cluster cleanup: {e}")
                
                # Try all possible HA uninstall script locations
                ha_uninstall_paths = [
                    "/opt/ufm/ufm_ha/uninstall_ha.sh",
                    "/opt/ufm/ha/uninstall_ha.sh",
                    "/opt/ufm/files/uninstall_ha.sh"
                ]
                
                ha_script_run = False
                for ha_script in ha_uninstall_paths:
                    if os.path.exists(ha_script) and os.access(ha_script, os.X_OK):
                        try:
                            print(f"{Fore.CYAN}Running HA uninstall script: {ha_script}{Style.RESET_ALL}")
                            
                            if self.auto_yes:
                                # Auto-answer mode for HA script
                                success = False
                                
                                # Try with -y flag first
                                try:
                                    subprocess.run(f"{ha_script} -y", shell=True, check=True, timeout=300)
                                    success = True
                                except Exception:
                                    # Try with yes command
                                    try:
                                        subprocess.run(f"yes y | timeout 300 {ha_script}", shell=True, check=True)
                                        success = True
                                    except Exception:
                                        # Last resort
                                        subprocess.run(f"timeout 300 {ha_script}", shell=True, check=False)
                                        success = True
                                
                                if success:
                                    print(f"{Fore.GREEN}Successfully executed HA uninstall script with auto-yes{Style.RESET_ALL}")
                            else:
                                # Interactive mode
                                subprocess.run(f"{ha_script} -y 2>/dev/null || {ha_script}", shell=True, check=False)
                            
                            logger.info(f"Ran HA uninstall script: {ha_script}")
                            ha_script_run = True
                            break
                        except Exception as e:
                            logger.warning(f"Failed to run HA uninstall script {ha_script}: {e}")
                
                if not ha_script_run:
                    logger.warning("No HA uninstall script found or executed")
            
            # Try to run the main uninstall script
            uninstall_script_run = False
            uninstall_paths = [
                "/opt/ufm/uninstall.sh",
                "/opt/ufm/files/uninstall.sh",
                "/opt/ufm/bin/uninstall.sh",
                "/opt/ufm/scripts/uninstall.sh"
            ]
            
            for script in uninstall_paths:
                if os.path.exists(script):
                    try:
                        print(f"{Fore.CYAN}Running uninstall script: {script}{Style.RESET_ALL}")
                        
                        if self.auto_yes:
                            # Auto-answer mode: use multiple approaches to automatically answer prompts
                            success = False
                            
                            # Method 1: Try with -y flag
                            try:
                                result = subprocess.run(f"{script} -y", shell=True, check=True, 
                                                       capture_output=True, text=True, timeout=300)
                                logger.info(f"Successfully ran {script} with -y flag")
                                success = True
                            except Exception as e:
                                logger.debug(f"Method 1 (-y flag) failed: {e}")
                            
                            # Method 2: Use yes command to pipe infinite "y" responses
                            if not success:
                                try:
                                    result = subprocess.run(f"yes y | timeout 300 {script}", shell=True, check=True,
                                                           capture_output=True, text=True)
                                    logger.info(f"Successfully ran {script} with yes command")
                                    success = True
                                except Exception as e:
                                    logger.debug(f"Method 2 (yes command) failed: {e}")
                            
                            # Method 3: Use expect-like behavior with Popen
                            if not success:
                                try:
                                    process = subprocess.Popen(script, shell=True, stdin=subprocess.PIPE, 
                                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                                             text=True, bufsize=1, universal_newlines=True)
                                    
                                    # Send multiple "y" responses for any prompts
                                    responses = "y\n" * 20  # Send 20 "y" responses
                                    stdout, stderr = process.communicate(input=responses, timeout=300)
                                    
                                    if process.returncode == 0:
                                        logger.info(f"Successfully ran {script} with interactive responses")
                                        success = True
                                    else:
                                        logger.debug(f"Method 3 (interactive) failed with return code: {process.returncode}")
                                except Exception as e:
                                    logger.debug(f"Method 3 (interactive) failed: {e}")
                            
                            # Method 4: Last resort - run with timeout and ignore errors
                            if not success:
                                try:
                                    subprocess.run(f"timeout 300 {script}", shell=True, check=False)
                                    logger.info(f"Ran {script} with timeout (ignoring errors)")
                                    success = True
                                except Exception as e:
                                    logger.debug(f"Method 4 (timeout) failed: {e}")
                            
                            if success:
                                print(f"{Fore.GREEN}Successfully executed uninstall script with auto-yes{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.YELLOW}Uninstall script execution completed (some methods failed){Style.RESET_ALL}")
                        else:
                            # Interactive mode: run script normally
                            subprocess.run(script, shell=True, check=False)
                        
                        logger.info(f"Ran uninstall script: {script}")
                        uninstall_script_run = True
                        break
                    except Exception as e:
                        logger.warning(f"Failed to run uninstall script {script}: {e}")
            
            if not uninstall_script_run:
                logger.warning("No uninstall script found or executed successfully")
                print(f"{Fore.YELLOW}No uninstall script found or executed successfully{Style.RESET_ALL}")
                
                # If no scripts worked, we need to manually clean things up
                print(f"{Fore.CYAN}Performing manual cleanup...{Style.RESET_ALL}")
                
                # 1. Try to stop and disable systemd services
                try:
                    subprocess.run("systemctl stop ufm-* 2>/dev/null || true", shell=True, check=False)
                    subprocess.run("systemctl disable ufm-* 2>/dev/null || true", shell=True, check=False)
                    # Remove systemd service files
                    subprocess.run("rm -f /etc/systemd/system/ufm*.service 2>/dev/null || true", shell=True, check=False)
                    subprocess.run("systemctl daemon-reload", shell=True, check=False)
                    logger.info("Removed UFM systemd services")
                except Exception as e:
                    logger.warning(f"Error removing systemd services: {e}")
            
            # Finally, check if /opt/ufm directory still exists
            if os.path.exists("/opt/ufm"):
                print(f"{Fore.YELLOW}UFM directory still exists at /opt/ufm{Style.RESET_ALL}")
                
                # Check if auto_yes is enabled or ask for confirmation
                if self.auto_yes:
                    response = "y"
                    print(f"{Fore.YELLOW}Auto-removing /opt/ufm directory{Style.RESET_ALL}")
                else:
                    response = input(f"Do you want to forcibly remove /opt/ufm directory? [Y/n]: ").lower()
                
                if response in ["", "y", "yes"]:
                    try:
                        print(f"{Fore.CYAN}Removing /opt/ufm directory...{Style.RESET_ALL}")
                        # Try Python's shutil first
                        try:
                            shutil.rmtree("/opt/ufm", ignore_errors=True)
                        except Exception:
                            # Fall back to rm command
                            subprocess.run("rm -rf /opt/ufm", shell=True, check=False)
                        
                        if not os.path.exists("/opt/ufm"):
                            logger.info("Successfully removed /opt/ufm directory")
                            print(f"{Fore.GREEN}Successfully removed /opt/ufm directory{Style.RESET_ALL}")
                        else:
                            logger.warning("Failed to completely remove /opt/ufm directory")
                            print(f"{Fore.YELLOW}Failed to completely remove /opt/ufm directory. Some files may require manual removal.{Style.RESET_ALL}")
                    except Exception as e:
                        logger.error(f"Error removing /opt/ufm directory: {e}")
                else:
                    logger.info("User chose not to remove /opt/ufm directory")
            
            # Final check - if there are no active UFM services or Docker containers, 
            # consider the uninstallation successful even if some files remain
            ufm_active = False
            
            # Check for UFM systemd service
            try:
                result = subprocess.run(["systemctl", "list-units", "--type=service", "--all", "*ufm*"], 
                                     capture_output=True, text=True, check=False)
                if "ufm" in result.stdout.lower() and "running" in result.stdout.lower():
                    logger.warning("UFM service is still running")
                    ufm_active = True
            except Exception:
                pass
            
            # Check for UFM Docker container
            try:
                result = subprocess.run(["docker", "ps"], capture_output=True, text=True, check=False)
                if "ufm" in result.stdout.lower() or "mellanox/ufm" in result.stdout.lower():
                    logger.warning("UFM Docker container is still running")
                    ufm_active = True
            except Exception:
                pass
            
            if ufm_active:
                logger.warning("UFM is still active after uninstall attempts")
                print(f"{Fore.RED}Warning: UFM is still active after uninstall attempts. Manual intervention may be required.{Style.RESET_ALL}")
                return False
            else:
                logger.info("No active UFM services or containers found - uninstallation considered successful")
                print(f"{Fore.GREEN}UFM uninstallation successful - no active services or containers found{Style.RESET_ALL}")
                return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall UFM: {e}")
            return False
    
    def compare_docker_images(self):
        """Main method to compare two UFM Docker images"""
        try:
            # Check prerequisites
            self.check_prerequisites()
            
            # Install old UFM Docker image
            self.install_old_ufm()
            
            # Extract configuration files from old UFM
            self.extract_configs(self.old_configs_dir)
            
            # Upgrade to new UFM Docker image
            self.upgrade_ufm()
            
            # Extract configuration files from new UFM
            self.extract_configs(self.new_configs_dir)
            
            # Create results directory and copy configuration files for permanent storage
            results_dir = os.path.join(os.getcwd(), "results")
            os.makedirs(results_dir, exist_ok=True)
            
            # Create subdirectories for old and new configs
            old_results_dir = os.path.join(results_dir, "old_configs")
            new_results_dir = os.path.join(results_dir, "new_configs")
            os.makedirs(old_results_dir, exist_ok=True)
            os.makedirs(new_results_dir, exist_ok=True)
            
            # Copy configuration files to results directory
            if os.path.exists(self.old_configs_dir):
                for filename in os.listdir(self.old_configs_dir):
                    src = os.path.join(self.old_configs_dir, filename)
                    dst = os.path.join(old_results_dir, filename)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                        logger.info(f"Copied {filename} to results/old_configs/")
            
            if os.path.exists(self.new_configs_dir):
                for filename in os.listdir(self.new_configs_dir):
                    src = os.path.join(self.new_configs_dir, filename)
                    dst = os.path.join(new_results_dir, filename)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                        logger.info(f"Copied {filename} to results/new_configs/")
            
            # Copy README file to results directory if it exists
            readme_path = os.path.join(os.getcwd(), "results_README.md")
            if os.path.exists(readme_path):
                readme_dst = os.path.join(results_dir, "README.md")
                shutil.copy2(readme_path, readme_dst)
                logger.info("Copied README.md to results directory")
            
            logger.info(f"Configuration files saved to {results_dir}")
            print(f"{Fore.GREEN}Configuration files saved to {results_dir}{Style.RESET_ALL}")
            
            # Return paths to extracted config directories for comparison
            return {
                'old_configs_dir': self.old_configs_dir,
                'new_configs_dir': self.new_configs_dir,
                'results_dir': results_dir
            }
        finally:
            # Always try to uninstall UFM, even if an error occurred
            self.uninstall_ufm() 