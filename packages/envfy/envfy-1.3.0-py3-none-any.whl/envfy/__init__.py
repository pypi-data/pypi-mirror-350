#!/usr/bin/env python3
"""
EnvFy - Professional Virtual Environment Manager

A fast, precise, and user-friendly Python virtual environment management tool
that makes working with virtual environments as easy as using pip.

Features:
- Lightning-fast environment creation and management
- Intuitive CLI interface with rich output
- Smart package installation and dependency management
- Environment templates and presets
- Cross-platform compatibility
- Advanced caching for optimal performance
"""

__version__ = "1.3.0"
__author__ = "Mmdrza"
__email__ = "Pymmdrza@gmail.com"
__license__ = "MIT"

# Public API exports
from .core.manager import EnvironmentManager
from .core.environment import Environment
from .core.config import Config
from .utils.exceptions import (
    EnvFyError,
    EnvironmentNotFoundError,
    EnvironmentExistsError,
    InvalidEnvironmentNameError,
    PythonNotFoundError,
    PackageInstallationError,
)

__all__ = [
    # Core classes
    "EnvironmentManager",
    "Environment", 
    "Config",
    # Exceptions
    "EnvFyError",
    "EnvironmentNotFoundError",
    "EnvironmentExistsError", 
    "InvalidEnvironmentNameError",
    "PythonNotFoundError",
    "PackageInstallationError",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

# Package metadata
metadata = {
    "name": "envfy",
    "version": __version__,
    "description": "Fast, precise, and user-friendly Python virtual environment management",
    "author": __author__,
    "email": __email__,
    "license": __license__,
    "url": "https://github.com/envfy/envfy",
} 
