"""
UFM Configuration Differentiator Tool

A tool for comparing UFM (Unified Fabric Manager) configurations between NVIDIA servers
or between two UFM Docker images.
"""

__version__ = "0.3.0"

# Import Docker manager for easier access
try:
    from .docker_operations import DockerManager
except ImportError:
    # Docker operations module may not be available in specific environments
    pass 