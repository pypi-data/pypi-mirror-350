#!/usr/bin/env python3
"""
EnvFy Validation Utilities

Validation functions for environment names, Python versions, package names, and other inputs.
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Tuple, Union
from packaging.version import Version, InvalidVersion
from packaging.requirements import Requirement, InvalidRequirement

from .exceptions import ValidationError, InvalidEnvironmentNameError


def validate_environment_name(name: str) -> bool:
    """Validate environment name according to EnvFy rules."""
    if not name:
        raise InvalidEnvironmentNameError(name, "Name cannot be empty")
    
    if len(name) > 50:
        raise InvalidEnvironmentNameError(name, "Name too long (max 50 characters)")
    
    # Must start with letter or underscore
    if not (name[0].isalpha() or name[0] == "_"):
        raise InvalidEnvironmentNameError(name, "Must start with letter or underscore")
    
    # Check valid characters
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_-]*$"
    if not re.match(pattern, name):
        raise InvalidEnvironmentNameError(name, "Can only contain letters, numbers, underscores, and hyphens")
    
    # Check reserved names
    reserved_names = {
        "con", "prn", "aux", "nul",
        "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
        "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
        "pip", "python", "envfy", "venv", "virtualenv",
        "test", "tests", "temp", "tmp", "cache",
        ".", "..", "__pycache__",
    }
    
    if name.lower() in reserved_names:
        raise InvalidEnvironmentNameError(name, f"'{name}' is a reserved name")
    
    return True


def validate_python_version(version: str) -> bool:
    """Validate Python version string."""
    if not version:
        raise ValidationError("python_version", version, "Version cannot be empty")
    
    # Remove 'python' prefix if present
    clean_version = version.lower()
    if clean_version.startswith("python"):
        clean_version = clean_version[6:]
    
    # Must start with digit
    if not clean_version[0].isdigit():
        raise ValidationError("python_version", version, "Version must start with a number")
    
    # Check version format
    version_pattern = r"^\d+\.\d+(\.\d+)?$"
    if not re.match(version_pattern, clean_version):
        raise ValidationError("python_version", version, "Invalid version format (expected X.Y or X.Y.Z)")
    
    try:
        # Parse and validate using packaging
        parsed_version = Version(clean_version)
        
        # Check if it's a reasonable Python version
        if parsed_version.major < 3 or (parsed_version.major == 3 and parsed_version.minor < 7):
            raise ValidationError("python_version", version, "Python 3.7+ is required")
        
        if parsed_version.major > 3 or (parsed_version.major == 3 and parsed_version.minor > 15):
            raise ValidationError("python_version", version, "Version too high (future version)")
            
    except InvalidVersion:
        raise ValidationError("python_version", version, "Invalid version format")
    
    return True


def validate_package_name(package: str) -> bool:
    """Validate package name or requirement specification."""
    if not package:
        raise ValidationError("package_name", package, "Package name cannot be empty")
    
    try:
        # Use packaging.requirements to validate
        requirement = Requirement(package)
        
        # Check package name format
        name_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$"
        if not re.match(name_pattern, requirement.name):
            raise ValidationError("package_name", package, "Invalid package name format")
        
        # Check for security issues
        dangerous_names = {
            "pip", "setuptools", "wheel", "python", "envfy"
        }
        if requirement.name.lower() in dangerous_names:
            raise ValidationError("package_name", package, f"'{requirement.name}' is a protected package")
            
    except InvalidRequirement as e:
        raise ValidationError("package_name", package, f"Invalid requirement: {e}")
    
    return True 