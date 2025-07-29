#!/usr/bin/env python3
"""
EnvFy Template Management

Handles environment templates for quick environment creation.
"""

import json
import toml
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field

from .config import get_config
from ..utils.helpers import ensure_directory
from ..utils.exceptions import TemplateError, ConfigurationError
from ..utils.validators import validate_environment_config


@dataclass
class Template:
    """Environment template definition."""
    
    name: str
    description: str
    python_version: Optional[str] = None
    packages: List[str] = field(default_factory=list)
    requirements_file: Optional[str] = None
    system_site_packages: bool = False
    without_pip: bool = False
    env_vars: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Template metadata
    author: Optional[str] = None
    version: str = "1.0.0"
    created: Optional[str] = None
    updated: Optional[str] = None


class TemplateManager:
    """Manages environment templates."""
    
    def __init__(self):
        """Initialize template manager."""
        self.config = get_config()
        self.templates_dir = self.config.templates_dir
        ensure_directory(self.templates_dir)
        self._templates_cache = {}
        self._cache_valid = False
    
    def _invalidate_cache(self) -> None:
        """Invalidate templates cache."""
        self._cache_valid = False
        self._templates_cache.clear()
    
    def _update_cache(self) -> None:
        """Update templates cache."""
        if self._cache_valid:
            return
        
        self._templates_cache.clear()
        
        if not self.templates_dir.exists():
            self._cache_valid = True
            return
        
        # Load templates from files
        for template_file in self.templates_dir.glob("*.toml"):
            try:
                template = self._load_template_file(template_file)
                if template:
                    self._templates_cache[template.name] = template
            except Exception:
                pass  # Skip invalid templates
        
        # Load built-in templates
        self._load_builtin_templates()
        
        self._cache_valid = True
    
    def _load_template_file(self, template_file: Path) -> Optional[Template]:
        """Load template from file."""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                if template_file.suffix.lower() == '.json':
                    data = json.load(f)
                elif template_file.suffix.lower() in ['.yml', '.yaml']:
                    data = yaml.safe_load(f)
                else:  # Default to TOML
                    data = toml.load(f)
            
            # Extract template data
            if 'template' in data:
                template_data = data['template']
            else:
                template_data = data
            
            # Set name from filename if not specified
            if 'name' not in template_data:
                template_data['name'] = template_file.stem
            
            return Template(**template_data)
            
        except Exception as e:
            raise TemplateError(template_file.stem, f"Failed to load template: {e}")
    
    def _load_builtin_templates(self) -> None:
        """Load built-in templates."""
        builtin_templates = [
            Template(
                name="basic",
                description="Basic Python environment",
                packages=["pip", "setuptools", "wheel"]
            ),
            Template(
                name="web",
                description="Web development environment",
                packages=[
                    "flask>=2.0.0",
                    "requests>=2.25.0", 
                    "beautifulsoup4",
                    "pytest",
                    "black",
                    "flake8"
                ]
            ),
            Template(
                name="data",
                description="Data science environment",
                packages=[
                    "numpy",
                    "pandas", 
                    "matplotlib",
                    "jupyter",
                    "scikit-learn",
                    "seaborn"
                ]
            ),
            Template(
                name="ml",
                description="Machine learning environment",
                packages=[
                    "numpy",
                    "pandas",
                    "scikit-learn",
                    "tensorflow",
                    "torch",
                    "matplotlib",
                    "jupyter"
                ]
            ),
            Template(
                name="testing",
                description="Testing environment",
                packages=[
                    "pytest",
                    "pytest-cov",
                    "pytest-mock",
                    "tox",
                    "black",
                    "flake8",
                    "mypy"
                ]
            ),
            Template(
                name="api",
                description="API development environment", 
                packages=[
                    "fastapi",
                    "uvicorn",
                    "requests",
                    "pydantic",
                    "pytest",
                    "httpx"
                ]
            )
        ]
        
        for template in builtin_templates:
            if template.name not in self._templates_cache:
                self._templates_cache[template.name] = template
    
    def list_templates(self, refresh: bool = False) -> List[str]:
        """
        List all available templates.
        
        Args:
            refresh: Force refresh of template cache
        
        Returns:
            List of template names
        """
        if refresh:
            self._invalidate_cache()
        
        self._update_cache()
        return sorted(self._templates_cache.keys())
    
    def get_template(self, name: str) -> Optional[Template]:
        """
        Get a template by name.
        
        Args:
            name: Template name
        
        Returns:
            Template instance or None if not found
        """
        self._update_cache()
        return self._templates_cache.get(name)
    
    def template_exists(self, name: str) -> bool:
        """
        Check if a template exists.
        
        Args:
            name: Template name
        
        Returns:
            True if template exists
        """
        return self.get_template(name) is not None
    
    def create_template(self, template: Template, overwrite: bool = False) -> bool:
        """
        Create a new template.
        
        Args:
            template: Template to create
            overwrite: Overwrite existing template
        
        Returns:
            True if template was created successfully
        """
        try:
            if self.template_exists(template.name) and not overwrite:
                raise TemplateError(template.name, "Template already exists")
            
            # Validate template
            template_data = asdict(template)
            valid, issues = validate_environment_config(template_data)
            if not valid:
                raise TemplateError(template.name, f"Invalid template: {', '.join(issues)}")
            
            # Save template file
            template_file = self.templates_dir / f"{template.name}.toml"
            
            # Add timestamps
            from datetime import datetime
            now = datetime.now().isoformat()
            if not template.created:
                template.created = now
            template.updated = now
            
            template_data = {
                'template': asdict(template)
            }
            
            with open(template_file, 'w', encoding='utf-8') as f:
                toml.dump(template_data, f)
            
            # Invalidate cache
            self._invalidate_cache()
            
            return True
            
        except Exception as e:
            raise TemplateError(template.name, f"Failed to create template: {e}")
    
    def delete_template(self, name: str) -> bool:
        """
        Delete a template.
        
        Args:
            name: Template name
        
        Returns:
            True if template was deleted successfully
        """
        try:
            template_file = self.templates_dir / f"{name}.toml"
            
            if not template_file.exists():
                raise TemplateError(name, "Template file not found")
            
            template_file.unlink()
            
            # Invalidate cache
            self._invalidate_cache()
            
            return True
            
        except Exception as e:
            raise TemplateError(name, f"Failed to delete template: {e}")
    
    def update_template(self, template: Template) -> bool:
        """
        Update an existing template.
        
        Args:
            template: Updated template
        
        Returns:
            True if template was updated successfully
        """
        return self.create_template(template, overwrite=True)
    
    def import_template(self, template_file: Union[str, Path], name: Optional[str] = None) -> bool:
        """
        Import a template from file.
        
        Args:
            template_file: Path to template file
            name: Optional name override
        
        Returns:
            True if template was imported successfully
        """
        try:
            template_path = Path(template_file)
            if not template_path.exists():
                raise TemplateError(name or "unknown", f"Template file not found: {template_path}")
            
            template = self._load_template_file(template_path)
            if not template:
                raise TemplateError(name or "unknown", "Failed to load template")
            
            if name:
                template.name = name
            
            return self.create_template(template, overwrite=True)
            
        except Exception as e:
            raise TemplateError(name or "unknown", f"Failed to import template: {e}")
    
    def export_template(self, name: str, output_file: Union[str, Path], 
                       format: str = 'toml') -> bool:
        """
        Export a template to file.
        
        Args:
            name: Template name
            output_file: Output file path
            format: Output format (toml, json, yaml)
        
        Returns:
            True if template was exported successfully
        """
        try:
            template = self.get_template(name)
            if not template:
                raise TemplateError(name, "Template not found")
            
            output_path = Path(output_file)
            ensure_directory(output_path.parent)
            
            template_data = {
                'template': asdict(template)
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                if format.lower() == 'json':
                    json.dump(template_data, f, indent=2)
                elif format.lower() in ['yml', 'yaml']:
                    yaml.dump(template_data, f, default_flow_style=False)
                else:  # Default to TOML
                    toml.dump(template_data, f)
            
            return True
            
        except Exception as e:
            raise TemplateError(name, f"Failed to export template: {e}")
    
    def get_template_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed template information.
        
        Args:
            name: Template name
        
        Returns:
            Template information dictionary
        """
        template = self.get_template(name)
        if not template:
            return None
        
        info = asdict(template)
        info['is_builtin'] = name in [
            'basic', 'web', 'data', 'ml', 'testing', 'api'
        ]
        
        return info
    
    def search_templates(self, query: str) -> List[str]:
        """
        Search templates by name or description.
        
        Args:
            query: Search query
        
        Returns:
            List of matching template names
        """
        query = query.lower()
        matches = []
        
        for template_name in self.list_templates():
            template = self.get_template(template_name)
            if not template:
                continue
            
            # Check name match
            if query in template_name.lower():
                matches.append(template_name)
                continue
            
            # Check description match
            if template.description and query in template.description.lower():
                matches.append(template_name)
                continue
            
            # Check tags match
            if template.tags and any(query in tag.lower() for tag in template.tags):
                matches.append(template_name)
                continue
        
        return matches
    
    def validate_template(self, name: str) -> tuple[bool, List[str]]:
        """
        Validate a template.
        
        Args:
            name: Template name
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        template = self.get_template(name)
        if not template:
            return False, ["Template not found"]
        
        # Convert to environment config format for validation
        template_data = asdict(template)
        return validate_environment_config(template_data)
    
    def apply_template(self, template_name: str, env_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply template to environment configuration.
        
        Args:
            template_name: Template name
            env_config: Environment configuration
        
        Returns:
            Updated environment configuration
        """
        template = self.get_template(template_name)
        if not template:
            raise TemplateError(template_name, "Template not found")
        
        # Merge template settings with environment config
        merged_config = env_config.copy()
        
        # Apply template values (environment config takes precedence)
        if template.python_version and 'python_version' not in merged_config:
            merged_config['python_version'] = template.python_version
        
        if template.packages:
            existing_packages = merged_config.get('packages', [])
            # Combine packages, avoiding duplicates
            all_packages = list(template.packages) + existing_packages
            merged_config['packages'] = list(dict.fromkeys(all_packages))
        
        if template.env_vars:
            existing_vars = merged_config.get('env_vars', {})
            merged_vars = template.env_vars.copy()
            merged_vars.update(existing_vars)  # Environment vars take precedence
            merged_config['env_vars'] = merged_vars
        
        if template.system_site_packages and 'system_site_packages' not in merged_config:
            merged_config['system_site_packages'] = template.system_site_packages
        
        if template.without_pip and 'without_pip' not in merged_config:
            merged_config['without_pip'] = template.without_pip
        
        return merged_config 