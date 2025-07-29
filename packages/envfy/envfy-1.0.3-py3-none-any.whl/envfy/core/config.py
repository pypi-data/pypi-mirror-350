#!/usr/bin/env python3
"""
EnvFy Configuration Management

Handles all configuration settings, user preferences, and configuration files.
"""

import os
import json
import toml
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict, field

from ..utils.helpers import get_envfy_home, get_config_dir, ensure_directory
from ..utils.exceptions import ConfigurationError


@dataclass
class GlobalSettings:
    """Global EnvFy settings."""
    
    # Directory settings
    envfy_home: str = ""
    environments_dir: str = ""
    cache_dir: str = ""
    templates_dir: str = ""
    
    # Default settings
    default_python_version: Optional[str] = None
    auto_activate: bool = False
    show_banner: bool = True
    colored_output: bool = True
    verbose: bool = False
    
    # Performance settings
    parallel_installs: bool = True
    max_workers: int = 4
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    
    # Network settings
    timeout: int = 30
    retries: int = 3
    index_url: str = "https://pypi.org/simple/"
    trusted_hosts: List[str] = field(default_factory=list)
    
    # Security settings
    verify_ssl: bool = True
    allow_unsafe_packages: bool = False
    
    # Template settings
    default_template: Optional[str] = None
    auto_update_templates: bool = True
    
    def __post_init__(self):
        """Initialize default paths if not set."""
        if not self.envfy_home:
            self.envfy_home = str(get_envfy_home())
        
        if not self.environments_dir:
            self.environments_dir = str(Path(self.envfy_home) / "environments")
        
        if not self.cache_dir:
            self.cache_dir = str(Path(self.envfy_home) / "cache")
        
        if not self.templates_dir:
            self.templates_dir = str(Path(self.envfy_home) / "templates")


@dataclass
class EnvironmentSettings:
    """Settings for individual environments."""
    
    name: str
    python_version: Optional[str] = None
    packages: List[str] = field(default_factory=list)
    requirements_file: Optional[str] = None
    template: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    # Advanced settings
    site_packages: bool = True
    system_site_packages: bool = False
    symlinks: bool = True
    upgrade_deps: bool = False
    
    # Environment variables
    env_vars: Dict[str, str] = field(default_factory=dict)
    
    # Project settings
    project_path: Optional[str] = None
    auto_activate_on_cd: bool = False


class Config:
    """Main configuration manager for EnvFy."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """Initialize configuration manager."""
        self.config_dir = get_config_dir()
        ensure_directory(self.config_dir)
        
        if config_path:
            self.config_file = Path(config_path)
        else:
            self.config_file = self.config_dir / "config.toml"
        
        self.global_settings = GlobalSettings()
        self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        if not self.config_file.exists():
            self.save()  # Create default config
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                if self.config_file.suffix.lower() == '.json':
                    data = json.load(f)
                elif self.config_file.suffix.lower() in ['.yml', '.yaml']:
                    data = yaml.safe_load(f)
                else:  # Default to TOML
                    data = toml.load(f)
            
            # Update global settings
            if 'global' in data:
                for key, value in data['global'].items():
                    if hasattr(self.global_settings, key):
                        setattr(self.global_settings, key, value)
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}", str(self.config_file))
    
    def save(self) -> None:
        """Save configuration to file."""
        config_data = {
            'global': asdict(self.global_settings),
            'version': '1.0.0',
            'schema_version': 1,
        }
        
        try:
            ensure_directory(self.config_file.parent)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                if self.config_file.suffix.lower() == '.json':
                    json.dump(config_data, f, indent=2)
                elif self.config_file.suffix.lower() in ['.yml', '.yaml']:
                    yaml.dump(config_data, f, default_flow_style=False)
                else:  # Default to TOML
                    toml.dump(config_data, f)
                    
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}", str(self.config_file))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        try:
            parts = key.split('.')
            value = self.global_settings
            
            for part in parts:
                value = getattr(value, part)
            
            return value
        except AttributeError:
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        parts = key.split('.')
        
        if len(parts) == 1:
            if hasattr(self.global_settings, key):
                setattr(self.global_settings, key, value)
            else:
                raise ConfigurationError(f"Unknown configuration key: {key}")
        else:
            # Handle nested keys if needed in the future
            raise ConfigurationError(f"Nested configuration keys not yet supported: {key}")
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.global_settings = GlobalSettings()
        self.save()
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Validate paths
        paths_to_check = [
            ('envfy_home', self.global_settings.envfy_home),
            ('environments_dir', self.global_settings.environments_dir),
            ('cache_dir', self.global_settings.cache_dir),
            ('templates_dir', self.global_settings.templates_dir),
        ]
        
        for name, path in paths_to_check:
            if not path:
                issues.append(f"{name} is not set")
                continue
            
            path_obj = Path(path)
            try:
                path_obj.resolve()
            except Exception as e:
                issues.append(f"Invalid {name} path '{path}': {e}")
        
        # Validate numeric settings
        if self.global_settings.max_workers < 1:
            issues.append("max_workers must be at least 1")
        
        if self.global_settings.cache_ttl < 0:
            issues.append("cache_ttl must be non-negative")
        
        if self.global_settings.timeout < 1:
            issues.append("timeout must be at least 1 second")
        
        if self.global_settings.retries < 0:
            issues.append("retries must be non-negative")
        
        # Validate URLs
        if not self.global_settings.index_url.startswith(('http://', 'https://')):
            issues.append("index_url must be a valid HTTP/HTTPS URL")
        
        return issues
    
    def export(self, format: str = 'toml') -> str:
        """Export configuration as string in specified format."""
        config_data = {
            'global': asdict(self.global_settings),
            'version': '1.0.0',
        }
        
        if format.lower() == 'json':
            return json.dumps(config_data, indent=2)
        elif format.lower() in ['yml', 'yaml']:
            return yaml.dump(config_data, default_flow_style=False)
        elif format.lower() == 'toml':
            return toml.dumps(config_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_from_string(self, config_str: str, format: str = 'toml') -> None:
        """Import configuration from string."""
        try:
            if format.lower() == 'json':
                data = json.loads(config_str)
            elif format.lower() in ['yml', 'yaml']:
                data = yaml.safe_load(config_str)
            elif format.lower() == 'toml':
                data = toml.loads(config_str)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            # Update settings
            if 'global' in data:
                for key, value in data['global'].items():
                    if hasattr(self.global_settings, key):
                        setattr(self.global_settings, key, value)
            
            self.save()
            
        except Exception as e:
            raise ConfigurationError(f"Failed to import configuration: {e}")
    
    def get_environment_config(self, env_name: str) -> Optional[EnvironmentSettings]:
        """Get configuration for a specific environment."""
        env_config_file = self.config_dir / "environments" / f"{env_name}.toml"
        
        if not env_config_file.exists():
            return None
        
        try:
            with open(env_config_file, 'r', encoding='utf-8') as f:
                data = toml.load(f)
            
            return EnvironmentSettings(**data)
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load environment config: {e}", str(env_config_file))
    
    def save_environment_config(self, env_settings: EnvironmentSettings) -> None:
        """Save configuration for a specific environment."""
        env_config_dir = self.config_dir / "environments"
        ensure_directory(env_config_dir)
        
        env_config_file = env_config_dir / f"{env_settings.name}.toml"
        
        try:
            with open(env_config_file, 'w', encoding='utf-8') as f:
                toml.dump(asdict(env_settings), f)
                
        except Exception as e:
            raise ConfigurationError(f"Failed to save environment config: {e}", str(env_config_file))
    
    def delete_environment_config(self, env_name: str) -> None:
        """Delete configuration for a specific environment."""
        env_config_file = self.config_dir / "environments" / f"{env_name}.toml"
        
        if env_config_file.exists():
            try:
                env_config_file.unlink()
            except Exception as e:
                raise ConfigurationError(f"Failed to delete environment config: {e}", str(env_config_file))
    
    def list_environment_configs(self) -> List[str]:
        """List all environment configuration names."""
        env_config_dir = self.config_dir / "environments"
        
        if not env_config_dir.exists():
            return []
        
        configs = []
        for config_file in env_config_dir.glob("*.toml"):
            configs.append(config_file.stem)
        
        return sorted(configs)
    
    @property
    def envfy_home(self) -> Path:
        """Get EnvFy home directory as Path object."""
        return Path(self.global_settings.envfy_home)
    
    @property
    def environments_dir(self) -> Path:
        """Get environments directory as Path object."""
        return Path(self.global_settings.environments_dir)
    
    @property
    def cache_dir(self) -> Path:
        """Get cache directory as Path object."""
        return Path(self.global_settings.cache_dir)
    
    @property
    def templates_dir(self) -> Path:
        """Get templates directory as Path object."""
        return Path(self.global_settings.templates_dir)


# Global configuration instance
_config = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config() -> Config:
    """Reload the global configuration instance."""
    global _config
    _config = Config()
    return _config 