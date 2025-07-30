"""
py-arrakis - A Python SDK for Arrakis.

This package provides a Python interface to the Arrakis VM sandbox system.
"""

__version__ = "2.0.0"

# API version prefix for all REST API endpoints
API_VERSION = "/v1"

# Import main classes to make them available at the package level
from .sandbox import Sandbox
from .sandbox_manager import SandboxManager

# Define public API
__all__ = ["Sandbox", "SandboxManager", "API_VERSION"]
