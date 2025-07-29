#!/usr/bin/env python3
"""
EnvFy Custom Exceptions

Defines all custom exception classes used throughout the EnvFy package.
"""

from typing import Optional, Any


class EnvFyError(Exception):
    """Base exception class for all EnvFy errors."""
    
    def __init__(self, message: str, details: Optional[str] = None, code: Optional[int] = None):
        self.message = message
        self.details = details
        self.code = code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.message}')"


class EnvironmentNotFoundError(EnvFyError):
    """Raised when a requested environment does not exist."""
    
    def __init__(self, env_name: str, details: Optional[str] = None):
        message = f"Environment '{env_name}' not found"
        super().__init__(message, details, code=404)
        self.env_name = env_name


class EnvironmentExistsError(EnvFyError):
    """Raised when trying to create an environment that already exists."""
    
    def __init__(self, env_name: str, details: Optional[str] = None):
        message = f"Environment '{env_name}' already exists"
        super().__init__(message, details, code=409)
        self.env_name = env_name


class InvalidEnvironmentNameError(EnvFyError):
    """Raised when an invalid environment name is provided."""
    
    def __init__(self, env_name: str, reason: Optional[str] = None):
        message = f"Invalid environment name '{env_name}'"
        if reason:
            message += f": {reason}"
        super().__init__(message, code=400)
        self.env_name = env_name
        self.reason = reason


class PythonNotFoundError(EnvFyError):
    """Raised when a specified Python version or executable is not found."""
    
    def __init__(self, python_version: Optional[str] = None, details: Optional[str] = None):
        if python_version:
            message = f"Python {python_version} not found"
        else:
            message = "Python executable not found"
        super().__init__(message, details, code=404)
        self.python_version = python_version


class PackageInstallationError(EnvFyError):
    """Raised when package installation fails."""
    
    def __init__(self, package: str, env_name: str, details: Optional[str] = None):
        message = f"Failed to install package '{package}' in environment '{env_name}'"
        super().__init__(message, details, code=500)
        self.package = package
        self.env_name = env_name


class ConfigurationError(EnvFyError):
    """Raised when there's an error in configuration."""
    
    def __init__(self, message: str, config_file: Optional[str] = None):
        super().__init__(message, code=400)
        self.config_file = config_file


class PermissionError(EnvFyError):
    """Raised when there's a permission error."""
    
    def __init__(self, operation: str, path: str):
        message = f"Permission denied: cannot {operation} '{path}'"
        super().__init__(message, code=403)
        self.operation = operation
        self.path = path


class NetworkError(EnvFyError):
    """Raised when there's a network-related error."""
    
    def __init__(self, message: str, url: Optional[str] = None):
        super().__init__(message, code=503)
        self.url = url


class DependencyError(EnvFyError):
    """Raised when there's a dependency-related error."""
    
    def __init__(self, message: str, dependency: Optional[str] = None):
        super().__init__(message, code=424)
        self.dependency = dependency


class TemplateError(EnvFyError):
    """Raised when there's an error with environment templates."""
    
    def __init__(self, template_name: str, message: str):
        full_message = f"Template '{template_name}' error: {message}"
        super().__init__(full_message, code=400)
        self.template_name = template_name


class BackupError(EnvFyError):
    """Raised when backup operations fail."""
    
    def __init__(self, operation: str, env_name: str, details: Optional[str] = None):
        message = f"Backup {operation} failed for environment '{env_name}'"
        super().__init__(message, details, code=500)
        self.operation = operation
        self.env_name = env_name


class ValidationError(EnvFyError):
    """Raised when validation fails."""
    
    def __init__(self, field: str, value: Any, reason: str):
        message = f"Validation failed for {field} '{value}': {reason}"
        super().__init__(message, code=400)
        self.field = field
        self.value = value
        self.reason = reason


class PlatformNotSupportedError(EnvFyError):
    """Raised when the current platform is not supported."""
    
    def __init__(self, platform: str, details: Optional[str] = None):
        message = f"Platform '{platform}' is not supported"
        super().__init__(message, details, code=501)
        self.platform = platform


# Exception mapping for easy lookup
EXCEPTION_MAP = {
    "environment_not_found": EnvironmentNotFoundError,
    "environment_exists": EnvironmentExistsError,
    "invalid_environment_name": InvalidEnvironmentNameError,
    "python_not_found": PythonNotFoundError,
    "package_installation": PackageInstallationError,
    "configuration": ConfigurationError,
    "permission": PermissionError,
    "network": NetworkError,
    "dependency": DependencyError,
    "template": TemplateError,
    "backup": BackupError,
    "validation": ValidationError,
    "platform_not_supported": PlatformNotSupportedError,
}


def get_exception_class(exception_type: str) -> type:
    """Get exception class by type name."""
    return EXCEPTION_MAP.get(exception_type, EnvFyError) 