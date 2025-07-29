#!/usr/bin/env python3
"""
EnvFy Environment Manager

Central manager for creating, deleting, and managing virtual environments.
"""

import os
import shutil
import tempfile
import concurrent.futures
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import virtualenv

from .config import get_config
from .environment import Environment
from ..utils.helpers import (
    find_python_executable, ensure_directory, remove_directory, 
    copy_directory, run_command, is_valid_env_name, generate_environment_name
)
from ..utils.exceptions import (
    EnvironmentNotFoundError, EnvironmentExistsError, InvalidEnvironmentNameError,
    PythonNotFoundError, EnvFyError
)
from ..utils.output import (
    print_success, print_error, print_info, print_warning, print_step, create_progress
)
from ..utils.validators import validate_environment_name, validate_python_version


class EnvironmentManager:
    """Central manager for virtual environments."""
    
    def __init__(self):
        """Initialize the environment manager."""
        self.config = get_config()
        self._ensure_directories()
        self._environments_cache = {}
        self._cache_valid = False
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        ensure_directory(self.config.environments_dir)
        ensure_directory(self.config.cache_dir)
        ensure_directory(self.config.templates_dir)
    
    def _invalidate_cache(self) -> None:
        """Invalidate the environments cache."""
        self._cache_valid = False
        self._environments_cache.clear()
    
    def _update_cache(self) -> None:
        """Update the environments cache."""
        if self._cache_valid:
            return
        
        self._environments_cache.clear()
        
        if not self.config.environments_dir.exists():
            self._cache_valid = True
            return
        
        for env_dir in self.config.environments_dir.iterdir():
            if env_dir.is_dir():
                env_name = env_dir.name
                if is_valid_env_name(env_name):
                    env = Environment(env_name, env_dir)
                    if env.exists:
                        self._environments_cache[env_name] = env
        
        self._cache_valid = True
    
    def create_environment(
        self,
        name: str,
        python_version: Optional[str] = None,
        template: Optional[str] = None,
        description: Optional[str] = None,
        packages: Optional[List[str]] = None,
        requirements_file: Optional[Union[str, Path]] = None,
        system_site_packages: bool = False,
        without_pip: bool = False,
        force: bool = False
    ) -> Optional[Environment]:
        """
        Create a new virtual environment.
        
        Args:
            name: Environment name
            python_version: Python version to use
            template: Template to use
            description: Environment description
            packages: List of packages to install
            requirements_file: Requirements file to install from
            system_site_packages: Give access to system site-packages
            without_pip: Don't install pip
            force: Overwrite existing environment
        
        Returns:
            Environment instance or None if creation failed
        """
        try:
            # Validate name
            validate_environment_name(name)
            
            # Check if environment already exists
            if self.environment_exists(name) and not force:
                raise EnvironmentExistsError(name)
            
            # Validate Python version if specified
            if python_version:
                validate_python_version(python_version)
            
            # Find Python executable
            python_exe = find_python_executable(python_version)
            print_info(f"Using Python: {python_exe}")
            
            # Prepare environment path
            env_path = self.config.environments_dir / name
            
            # Remove existing environment if force is True
            if force and env_path.exists():
                print_info("Removing existing environment...")
                remove_directory(env_path, force=True)
            
            # Create environment directory
            ensure_directory(env_path.parent)
            
            print_step(1, 3, "Creating virtual environment")
            
            # Use virtualenv to create the environment
            args = [
                str(env_path),
                f"--python={python_exe}",
            ]
            
            if system_site_packages:
                args.append("--system-site-packages")
            
            if without_pip:
                args.append("--without-pip")
            
            # Create environment using virtualenv
            virtualenv.cli_run(args)
            
            # Verify creation
            env = Environment(name, env_path)
            if not env.exists:
                print_error("Environment creation failed")
                return None
            
            print_step(2, 3, "Environment created successfully")
            
            # Install packages if specified
            if packages or requirements_file:
                print_step(3, 3, "Installing packages")
                
                if packages:
                    for package in packages:
                        try:
                            env.install_package(package)
                        except Exception as e:
                            print_warning(f"Failed to install {package}: {e}")
                
                if requirements_file:
                    try:
                        env.install_requirements(requirements_file)
                    except Exception as e:
                        print_warning(f"Failed to install requirements: {e}")
            
            # Save environment configuration if description provided
            if description:
                from .config import EnvironmentSettings
                env_settings = EnvironmentSettings(
                    name=name,
                    python_version=python_version,
                    description=description,
                    packages=packages or []
                )
                self.config.save_environment_config(env_settings)
            
            # Invalidate cache
            self._invalidate_cache()
            
            print_success(f"Environment '{name}' created successfully")
            return env
            
        except Exception as e:
            print_error(f"Failed to create environment: {e}")
            # Clean up partial creation
            if env_path.exists():
                try:
                    remove_directory(env_path, force=True)
                except Exception:
                    pass
            return None
    
    def delete_environment(self, name: str, force: bool = False) -> bool:
        """
        Delete a virtual environment.
        
        Args:
            name: Environment name
            force: Force deletion without safety checks
        
        Returns:
            True if deletion was successful
        """
        try:
            if not self.environment_exists(name):
                raise EnvironmentNotFoundError(name)
            
            env_path = self.config.environments_dir / name
            
            # Safety check
            if not force:
                from ..utils.validators import is_safe_to_delete
                if not is_safe_to_delete(env_path):
                    print_error("Environment path appears unsafe to delete")
                    return False
            
            print_info(f"Deleting environment '{name}'...")
            
            # Remove environment directory
            remove_directory(env_path, force=True)
            
            # Remove environment configuration
            try:
                self.config.delete_environment_config(name)
            except Exception:
                pass  # Config might not exist
            
            # Invalidate cache
            self._invalidate_cache()
            
            print_success(f"Environment '{name}' deleted successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to delete environment: {e}")
            return False
    
    def list_environments(self, refresh: bool = False) -> List[str]:
        """
        List all available environments.
        
        Args:
            refresh: Force refresh of environment cache
        
        Returns:
            List of environment names
        """
        if refresh:
            self._invalidate_cache()
        
        self._update_cache()
        return sorted(self._environments_cache.keys())
    
    def get_environment(self, name: str) -> Environment:
        """
        Get an environment instance.
        
        Args:
            name: Environment name
        
        Returns:
            Environment instance
        
        Raises:
            EnvironmentNotFoundError: If environment doesn't exist
        """
        if not self.environment_exists(name):
            raise EnvironmentNotFoundError(name)
        
        self._update_cache()
        
        if name in self._environments_cache:
            return self._environments_cache[name]
        
        # Create new instance
        env_path = self.config.environments_dir / name
        env = Environment(name, env_path)
        self._environments_cache[name] = env
        return env
    
    def environment_exists(self, name: str) -> bool:
        """
        Check if an environment exists.
        
        Args:
            name: Environment name
        
        Returns:
            True if environment exists
        """
        env_path = self.config.environments_dir / name
        return env_path.exists() and Environment(name, env_path).exists
    
    def clone_environment(self, source: str, destination: str, force: bool = False) -> bool:
        """
        Clone an environment.
        
        Args:
            source: Source environment name
            destination: Destination environment name
            force: Overwrite destination if exists
        
        Returns:
            True if cloning was successful
        """
        try:
            # Validate names
            validate_environment_name(destination)
            
            if not self.environment_exists(source):
                raise EnvironmentNotFoundError(source)
            
            if self.environment_exists(destination) and not force:
                raise EnvironmentExistsError(destination)
            
            source_env = self.get_environment(source)
            source_path = source_env.path
            dest_path = self.config.environments_dir / destination
            
            print_info(f"Cloning environment '{source}' to '{destination}'...")
            
            # Remove destination if it exists and force is True
            if force and dest_path.exists():
                remove_directory(dest_path, force=True)
            
            # Copy environment directory
            with create_progress() as progress:
                task = progress.add_task("Copying environment...", total=None)
                copy_directory(source_path, dest_path)
                progress.remove_task(task)
            
            # Update environment name in configuration files
            self._update_cloned_environment(dest_path, destination)
            
            # Copy environment configuration if it exists
            try:
                source_config = self.config.get_environment_config(source)
                if source_config:
                    source_config.name = destination
                    self.config.save_environment_config(source_config)
            except Exception:
                pass  # Config might not exist
            
            # Invalidate cache
            self._invalidate_cache()
            
            print_success(f"Environment cloned successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to clone environment: {e}")
            return False
    
    def _update_cloned_environment(self, env_path: Path, new_name: str) -> None:
        """Update configuration files in cloned environment."""
        try:
            # Update pyvenv.cfg
            pyvenv_cfg = env_path / "pyvenv.cfg"
            if pyvenv_cfg.exists():
                content = pyvenv_cfg.read_text()
                # Update any references to the old environment path
                content = content.replace(str(env_path.parent), str(env_path))
                pyvenv_cfg.write_text(content)
            
            # Update activation scripts
            if os.name == 'nt':  # Windows
                scripts_dir = env_path / "Scripts"
                activate_files = ["activate.bat", "Activate.ps1"]
            else:  # Unix-like
                scripts_dir = env_path / "bin"
                activate_files = ["activate", "activate.csh", "activate.fish"]
            
            for filename in activate_files:
                activate_file = scripts_dir / filename
                if activate_file.exists():
                    try:
                        content = activate_file.read_text()
                        # Update VIRTUAL_ENV path
                        old_path_pattern = str(env_path.parent / "SOURCE_ENV_NAME")
                        content = content.replace(old_path_pattern, str(env_path))
                        activate_file.write_text(content)
                    except Exception:
                        pass  # Not critical if activation script update fails
                        
        except Exception:
            pass  # Not critical if configuration update fails
    
    def rename_environment(self, old_name: str, new_name: str, force: bool = False) -> bool:
        """
        Rename an environment.
        
        Args:
            old_name: Current environment name
            new_name: New environment name
            force: Overwrite destination if exists
        
        Returns:
            True if renaming was successful
        """
        try:
            validate_environment_name(new_name)
            
            if not self.environment_exists(old_name):
                raise EnvironmentNotFoundError(old_name)
            
            if self.environment_exists(new_name) and not force:
                raise EnvironmentExistsError(new_name)
            
            old_path = self.config.environments_dir / old_name
            new_path = self.config.environments_dir / new_name
            
            print_info(f"Renaming environment '{old_name}' to '{new_name}'...")
            
            # Remove destination if it exists and force is True
            if force and new_path.exists():
                remove_directory(new_path, force=True)
            
            # Rename directory
            old_path.rename(new_path)
            
            # Update environment configuration
            self._update_cloned_environment(new_path, new_name)
            
            # Update environment configuration file
            try:
                old_config = self.config.get_environment_config(old_name)
                if old_config:
                    old_config.name = new_name
                    self.config.save_environment_config(old_config)
                    self.config.delete_environment_config(old_name)
            except Exception:
                pass
            
            # Invalidate cache
            self._invalidate_cache()
            
            print_success(f"Environment renamed successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to rename environment: {e}")
            return False
    
    def backup_environment(self, name: str, backup_path: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """
        Create a backup of an environment.
        
        Args:
            name: Environment name
            backup_path: Custom backup path
        
        Returns:
            Path to backup file or None if backup failed
        """
        try:
            if not self.environment_exists(name):
                raise EnvironmentNotFoundError(name)
            
            env_path = self.config.environments_dir / name
            
            if backup_path:
                backup_file = Path(backup_path)
            else:
                # Generate backup filename with timestamp
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = self.config.cache_dir / f"{name}_backup_{timestamp}.tar.gz"
            
            ensure_directory(backup_file.parent)
            
            print_info(f"Creating backup of environment '{name}'...")
            
            # Create tar.gz backup
            import tarfile
            with tarfile.open(backup_file, "w:gz") as tar:
                tar.add(env_path, arcname=name)
            
            print_success(f"Backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            print_error(f"Failed to create backup: {e}")
            return None
    
    def restore_environment(self, backup_path: Union[str, Path], name: Optional[str] = None, 
                           force: bool = False) -> bool:
        """
        Restore an environment from backup.
        
        Args:
            backup_path: Path to backup file
            name: Environment name (if different from backup)
            force: Overwrite existing environment
        
        Returns:
            True if restore was successful
        """
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                print_error(f"Backup file not found: {backup_file}")
                return False
            
            print_info(f"Restoring environment from backup...")
            
            # Extract backup to temporary directory first
            with tempfile.TemporaryDirectory() as temp_dir:
                import tarfile
                with tarfile.open(backup_file, "r:gz") as tar:
                    tar.extractall(temp_dir)
                
                # Find extracted environment
                temp_path = Path(temp_dir)
                extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
                
                if not extracted_dirs:
                    print_error("No environment found in backup")
                    return False
                
                source_dir = extracted_dirs[0]
                original_name = source_dir.name
                target_name = name or original_name
                
                validate_environment_name(target_name)
                
                if self.environment_exists(target_name) and not force:
                    raise EnvironmentExistsError(target_name)
                
                target_path = self.config.environments_dir / target_name
                
                # Remove existing environment if force is True
                if force and target_path.exists():
                    remove_directory(target_path, force=True)
                
                # Copy extracted environment
                copy_directory(source_dir, target_path)
                
                # Update environment configuration if name changed
                if target_name != original_name:
                    self._update_cloned_environment(target_path, target_name)
            
            # Invalidate cache
            self._invalidate_cache()
            
            print_success(f"Environment restored as '{target_name}'")
            return True
            
        except Exception as e:
            print_error(f"Failed to restore environment: {e}")
            return False
    
    def get_environment_stats(self) -> Dict[str, Any]:
        """
        Get statistics about all environments.
        
        Returns:
            Dictionary with environment statistics
        """
        self._update_cache()
        
        stats = {
            "total_environments": len(self._environments_cache),
            "total_size": 0,
            "python_versions": {},
            "package_counts": [],
            "broken_environments": 0,
        }
        
        for env_name, env in self._environments_cache.items():
            try:
                info = env.get_info()
                
                # Add size
                stats["total_size"] += info.size
                
                # Count Python versions
                if info.python_version:
                    version = info.python_version
                    stats["python_versions"][version] = stats["python_versions"].get(version, 0) + 1
                
                # Count packages
                stats["package_counts"].append(len(info.packages))
                
                # Check if environment is valid
                if not info.valid:
                    stats["broken_environments"] += 1
                    
            except Exception:
                stats["broken_environments"] += 1
        
        return stats
    
    def cleanup_broken_environments(self, dry_run: bool = False) -> List[str]:
        """
        Clean up broken environments.
        
        Args:
            dry_run: Only report what would be cleaned, don't actually clean
        
        Returns:
            List of environment names that were (or would be) cleaned
        """
        broken_envs = []
        
        for env_name in self.list_environments():
            try:
                env = self.get_environment(env_name)
                valid, issues = env.validate()
                
                if not valid:
                    broken_envs.append(env_name)
                    if not dry_run:
                        print_warning(f"Removing broken environment: {env_name}")
                        self.delete_environment(env_name, force=True)
            except Exception:
                broken_envs.append(env_name)
                if not dry_run:
                    print_warning(f"Removing broken environment: {env_name}")
                    try:
                        self.delete_environment(env_name, force=True)
                    except Exception:
                        pass
        
        if dry_run and broken_envs:
            print_info(f"Found {len(broken_envs)} broken environments:")
            for env_name in broken_envs:
                print_info(f"  - {env_name}")
        
        return broken_envs
    
    def auto_generate_name(self, base_name: str = "env") -> str:
        """
        Generate a unique environment name.
        
        Args:
            base_name: Base name to use
        
        Returns:
            Unique environment name
        """
        return generate_environment_name(base_name)
    
    def search_environments(self, query: str) -> List[str]:
        """
        Search environments by name or metadata.
        
        Args:
            query: Search query
        
        Returns:
            List of matching environment names
        """
        query = query.lower()
        matches = []
        
        for env_name in self.list_environments():
            # Check name match
            if query in env_name.lower():
                matches.append(env_name)
                continue
            
            # Check description match
            try:
                env_config = self.config.get_environment_config(env_name)
                if env_config and env_config.description:
                    if query in env_config.description.lower():
                        matches.append(env_name)
                        continue
            except Exception:
                pass
            
            # Check tags match
            try:
                env_config = self.config.get_environment_config(env_name)
                if env_config and env_config.tags:
                    if any(query in tag.lower() for tag in env_config.tags):
                        matches.append(env_name)
                        continue
            except Exception:
                pass
        
        return matches 