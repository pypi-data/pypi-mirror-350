#!/usr/bin/env python3
"""
EnvFy Validation Utilities

Validation functions for environment names, Python versions, package names, and other inputs.
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Tuple, Union, Dict, Any
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


def validate_environment_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate environment configuration data.
    
    Args:
        config: Environment configuration dictionary
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        # Validate environment name if present
        if 'name' in config:
            try:
                validate_environment_name(config['name'])
            except Exception as e:
                issues.append(f"Invalid name: {str(e)}")
        
        # Validate Python version if present
        if 'python_version' in config and config['python_version']:
            try:
                validate_python_version(config['python_version'])
            except Exception as e:
                issues.append(f"Invalid Python version: {str(e)}")
        
        # Validate packages if present
        if 'packages' in config and config['packages']:
            if not isinstance(config['packages'], list):
                issues.append("Packages must be a list")
            else:
                for i, package in enumerate(config['packages']):
                    try:
                        validate_package_name(package)
                    except Exception as e:
                        issues.append(f"Invalid package at index {i}: {str(e)}")
        
        # Validate requirements file if present
        if 'requirements_file' in config and config['requirements_file']:
            req_file = Path(config['requirements_file'])
            if not req_file.exists():
                issues.append(f"Requirements file not found: {req_file}")
            elif not req_file.is_file():
                issues.append(f"Requirements path is not a file: {req_file}")
        
        # Validate boolean fields
        bool_fields = [
            'system_site_packages', 'without_pip', 'site_packages', 
            'symlinks', 'upgrade_deps', 'auto_activate_on_cd'
        ]
        for field in bool_fields:
            if field in config and not isinstance(config[field], bool):
                issues.append(f"Field '{field}' must be a boolean")
        
        # Validate environment variables if present
        if 'env_vars' in config and config['env_vars']:
            if not isinstance(config['env_vars'], dict):
                issues.append("Environment variables must be a dictionary")
            else:
                for key, value in config['env_vars'].items():
                    if not isinstance(key, str):
                        issues.append(f"Environment variable key must be string: {key}")
                    if not isinstance(value, str):
                        issues.append(f"Environment variable value must be string: {value}")
        
        # Validate tags if present
        if 'tags' in config and config['tags']:
            if not isinstance(config['tags'], list):
                issues.append("Tags must be a list")
            else:
                for i, tag in enumerate(config['tags']):
                    if not isinstance(tag, str):
                        issues.append(f"Tag at index {i} must be a string")
                    elif not tag.strip():
                        issues.append(f"Tag at index {i} cannot be empty")
        
        # Validate description if present
        if 'description' in config and config['description'] is not None:
            if not isinstance(config['description'], str):
                issues.append("Description must be a string")
            elif len(config['description']) > 500:
                issues.append("Description too long (max 500 characters)")
        
        # Validate project path if present
        if 'project_path' in config and config['project_path']:
            project_path = Path(config['project_path'])
            if not project_path.exists():
                issues.append(f"Project path does not exist: {project_path}")
        
        return len(issues) == 0, issues
        
    except Exception as e:
        issues.append(f"Configuration validation error: {str(e)}")
        return False, issues 