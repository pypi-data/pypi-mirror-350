#!/usr/bin/env python3
"""
EnvFy Environment Management

Represents and manages individual virtual environments.
"""

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict

from ..utils.helpers import (
    get_python_version, get_environment_python, activate_environment_command,
    run_command, is_virtual_environment, format_size, get_directory_size,
    parse_requirements_file
)
from ..utils.exceptions import (
    EnvironmentNotFoundError, PackageInstallationError, PythonNotFoundError,
    EnvFyError
)
from ..utils.output import print_success, print_error, print_info, create_progress
from .config import get_config


@dataclass
class PackageInfo:
    """Information about an installed package."""
    name: str
    version: str
    location: str
    editable: bool = False
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class EnvironmentInfo:
    """Complete information about an environment."""
    name: str
    path: str
    python_version: Optional[str]
    python_executable: Optional[str]
    packages: List[PackageInfo]
    size: int
    created: Optional[datetime]
    last_accessed: Optional[datetime]
    active: bool = False
    valid: bool = True
    description: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class Environment:
    """Represents a virtual environment and provides management operations."""
    
    def __init__(self, name: str, path: Optional[Union[str, Path]] = None):
        """Initialize environment instance."""
        self.name = name
        self.config = get_config()
        
        if path:
            self.path = Path(path)
        else:
            self.path = self.config.environments_dir / name
        
        self._info = None
        self._packages_cache = None
        self._cache_time = 0
    
    @property
    def exists(self) -> bool:
        """Check if environment exists."""
        return self.path.exists() and is_virtual_environment(self.path)
    
    @property
    def python_executable(self) -> Optional[str]:
        """Get Python executable path."""
        return get_environment_python(self.path)
    
    @property
    def python_version(self) -> Optional[str]:
        """Get Python version of the environment."""
        python_exe = self.python_executable
        if python_exe:
            return get_python_version(python_exe)
        return None
    
    @property
    def activate_command(self) -> str:
        """Get the command to activate this environment."""
        return activate_environment_command(self.path)
    
    @property
    def site_packages_dir(self) -> Optional[Path]:
        """Get site-packages directory."""
        if not self.exists:
            return None
        
        # Find site-packages directory
        lib_dir = self.path / "lib"
        if lib_dir.exists():
            for python_dir in lib_dir.iterdir():
                if python_dir.name.startswith("python"):
                    site_packages = python_dir / "site-packages"
                    if site_packages.exists():
                        return site_packages
        
        # Windows
        lib_dir = self.path / "Lib" / "site-packages"
        if lib_dir.exists():
            return lib_dir
        
        return None
    
    @property
    def size(self) -> int:
        """Get total size of environment in bytes."""
        return get_directory_size(self.path) if self.exists else 0
    
    @property
    def size_formatted(self) -> str:
        """Get formatted size string."""
        return format_size(self.size)
    
    def get_info(self, refresh: bool = False) -> EnvironmentInfo:
        """Get complete environment information."""
        if self._info is None or refresh:
            self._info = self._collect_info()
        return self._info
    
    def _collect_info(self) -> EnvironmentInfo:
        """Collect environment information."""
        if not self.exists:
            return EnvironmentInfo(
                name=self.name,
                path=str(self.path),
                python_version=None,
                python_executable=None,
                packages=[],
                size=0,
                created=None,
                last_accessed=None,
                valid=False
            )
        
        # Get creation time
        created = None
        try:
            stat = self.path.stat()
            created = datetime.fromtimestamp(stat.st_ctime)
        except (OSError, ValueError):
            pass
        
        # Get last access time
        last_accessed = None
        try:
            stat = self.path.stat()
            last_accessed = datetime.fromtimestamp(stat.st_atime)
        except (OSError, ValueError):
            pass
        
        return EnvironmentInfo(
            name=self.name,
            path=str(self.path),
            python_version=self.python_version,
            python_executable=self.python_executable,
            packages=self.get_packages(),
            size=self.size,
            created=created,
            last_accessed=last_accessed,
            valid=True
        )
    
    def get_packages(self, refresh: bool = False) -> List[PackageInfo]:
        """Get list of installed packages."""
        current_time = time.time()
        
        # Use cache if recent and not forced refresh
        if (not refresh and self._packages_cache is not None and 
            current_time - self._cache_time < 60):  # 1 minute cache
            return self._packages_cache
        
        if not self.exists:
            return []
        
        python_exe = self.python_executable
        if not python_exe:
            return []
        
        packages = []
        
        try:
            # Use pip list to get packages
            result = run_command(
                [python_exe, "-m", "pip", "list", "--format=json"],
                timeout=30
            )
            
            if result.returncode == 0:
                package_data = json.loads(result.stdout)
                for pkg_info in package_data:
                    packages.append(PackageInfo(
                        name=pkg_info["name"],
                        version=pkg_info["version"],
                        location="",  # Will be filled if needed
                        editable=False  # Will be detected if needed
                    ))
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
            # Fallback: scan site-packages manually
            site_packages = self.site_packages_dir
            if site_packages and site_packages.exists():
                for item in site_packages.iterdir():
                    if item.name.endswith('.egg-info') or item.name.endswith('.dist-info'):
                        # Extract package name
                        pkg_name = item.name.split('-')[0]
                        
                        # Try to get version from metadata
                        version = "unknown"
                        metadata_file = item / "METADATA"
                        if not metadata_file.exists():
                            metadata_file = item / "PKG-INFO"
                        
                        if metadata_file.exists():
                            try:
                                with open(metadata_file, 'r', encoding='utf-8') as f:
                                    for line in f:
                                        if line.startswith('Version:'):
                                            version = line.split(':', 1)[1].strip()
                                            break
                            except Exception:
                                pass
                        
                        packages.append(PackageInfo(
                            name=pkg_name,
                            version=version,
                            location=str(item),
                            editable=False
                        ))
        
        # Cache the results
        self._packages_cache = packages
        self._cache_time = current_time
        
        return packages
    
    def install_package(self, package: str, upgrade: bool = False, 
                       user: bool = False, editable: bool = False,
                       index_url: Optional[str] = None, use_uv: bool = False) -> bool:
        """Install a package in the environment."""
        if not self.exists:
            raise EnvironmentNotFoundError(self.name)
        
        python_exe = self.python_executable
        if not python_exe:
            raise PythonNotFoundError()
        
        # Choose package manager
        if use_uv:
            cmd = ["uv", "pip", "install"]
            
            # UV specific options
            if upgrade:
                cmd.append("--upgrade")
            
            if editable:
                cmd.append("--editable")
            
            if index_url:
                cmd.extend(["--index-url", index_url])
            
            # Set target environment for UV
            cmd.extend(["--python", python_exe])
            cmd.append(package)
        else:
            # Standard pip installation
            cmd = [python_exe, "-m", "pip", "install"]
            
            if upgrade:
                cmd.append("--upgrade")
            
            if user:
                cmd.append("--user")
            
            if editable:
                cmd.append("--editable")
            
            if index_url:
                cmd.extend(["--index-url", index_url])
            
            cmd.append(package)
        
        try:
            with create_progress() as progress:
                task = progress.add_task(f"Installing {package}...", total=None)
                
                result = run_command(cmd, timeout=300)
                
                progress.remove_task(task)
            
            if result.returncode == 0:
                manager_name = "UV" if use_uv else "pip"
                print_success(f"Successfully installed {package} using {manager_name}")
                # Clear cache
                self._packages_cache = None
                return True
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                print_error(f"Failed to install {package}", error_msg)
                raise PackageInstallationError(package, self.name, error_msg)
                
        except subprocess.TimeoutExpired:
            raise PackageInstallationError(package, self.name, "Installation timed out")
        except Exception as e:
            raise PackageInstallationError(package, self.name, str(e))
    
    def uninstall_package(self, package: str, yes: bool = False) -> bool:
        """Uninstall a package from the environment."""
        if not self.exists:
            raise EnvironmentNotFoundError(self.name)
        
        python_exe = self.python_executable
        if not python_exe:
            raise PythonNotFoundError()
        
        cmd = [python_exe, "-m", "pip", "uninstall"]
        
        if yes:
            cmd.append("--yes")
        
        cmd.append(package)
        
        try:
            result = run_command(cmd, timeout=60)
            
            if result.returncode == 0:
                print_success(f"Successfully uninstalled {package}")
                # Clear cache
                self._packages_cache = None
                return True
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                print_error(f"Failed to uninstall {package}", error_msg)
                return False
                
        except Exception as e:
            print_error(f"Failed to uninstall {package}", str(e))
            return False
    
    def install_requirements(self, requirements_file: Union[str, Path], use_uv: bool = False) -> bool:
        """Install packages from requirements file."""
        requirements_file = Path(requirements_file)
        
        if not requirements_file.exists():
            raise FileNotFoundError(f"Requirements file not found: {requirements_file}")
        
        if not self.exists:
            raise EnvironmentNotFoundError(self.name)
        
        python_exe = self.python_executable
        if not python_exe:
            raise PythonNotFoundError()
        
        # Choose package manager
        if use_uv:
            cmd = ["uv", "pip", "install", "-r", str(requirements_file), "--python", python_exe]
        else:
            cmd = [python_exe, "-m", "pip", "install", "-r", str(requirements_file)]
        
        try:
            with create_progress() as progress:
                task = progress.add_task("Installing requirements...", total=None)
                
                result = run_command(cmd, timeout=600)  # 10 minutes
                
                progress.remove_task(task)
            
            if result.returncode == 0:
                manager_name = "UV" if use_uv else "pip"
                print_success(f"Successfully installed requirements using {manager_name}")
                # Clear cache
                self._packages_cache = None
                return True
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                print_error("Failed to install requirements", error_msg)
                return False
                
        except subprocess.TimeoutExpired:
            print_error("Installation timed out")
            return False
        except Exception as e:
            print_error("Failed to install requirements", str(e))
            return False
    
    def export_requirements(self, output_file: Optional[Union[str, Path]] = None,
                          include_editable: bool = True) -> str:
        """Export installed packages to requirements format."""
        if not self.exists:
            raise EnvironmentNotFoundError(self.name)
        
        python_exe = self.python_executable
        if not python_exe:
            raise PythonNotFoundError()
        
        cmd = [python_exe, "-m", "pip", "freeze"]
        if not include_editable:
            cmd.append("--exclude-editable")
        
        try:
            result = run_command(cmd, timeout=30)
            
            if result.returncode == 0:
                requirements_content = result.stdout
                
                if output_file:
                    output_path = Path(output_file)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(requirements_content)
                    print_success(f"Requirements exported to {output_path}")
                
                return requirements_content
            else:
                error_msg = result.stderr or "Unknown error"
                raise EnvFyError(f"Failed to export requirements: {error_msg}")
                
        except Exception as e:
            raise EnvFyError(f"Failed to export requirements: {e}")
    
    def run_command(self, command: List[str], **kwargs) -> subprocess.CompletedProcess:
        """Run a command in the environment's Python."""
        if not self.exists:
            raise EnvironmentNotFoundError(self.name)
        
        python_exe = self.python_executable
        if not python_exe:
            raise PythonNotFoundError()
        
        # Prepare environment variables
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(self.path)
        env["PATH"] = f"{self.path / 'bin'}:{env['PATH']}"
        
        # Use the environment's Python
        if command[0] == "python":
            command[0] = python_exe
        
        return run_command(command, env=env, **kwargs)
    
    def activate(self) -> Dict[str, str]:
        """Get environment variables needed to activate this environment."""
        if not self.exists:
            raise EnvironmentNotFoundError(self.name)
        
        env_vars = {
            "VIRTUAL_ENV": str(self.path),
            "VIRTUAL_ENV_PROMPT": f"({self.name})",
        }
        
        # Update PATH
        if os.name == 'nt':  # Windows
            scripts_dir = self.path / "Scripts"
            env_vars["PATH"] = f"{scripts_dir};{os.environ.get('PATH', '')}"
        else:  # Unix-like
            bin_dir = self.path / "bin"
            env_vars["PATH"] = f"{bin_dir}:{os.environ.get('PATH', '')}"
        
        return env_vars
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the environment and return status and issues."""
        issues = []
        
        if not self.path.exists():
            issues.append("Environment directory does not exist")
            return False, issues
        
        if not is_virtual_environment(self.path):
            issues.append("Directory is not a valid virtual environment")
            return False, issues
        
        python_exe = self.python_executable
        if not python_exe:
            issues.append("Python executable not found")
        else:
            if not Path(python_exe).exists():
                issues.append("Python executable file does not exist")
            elif not os.access(python_exe, os.X_OK):
                issues.append("Python executable is not executable")
        
        # Check if pip is available
        if python_exe:
            try:
                result = run_command([python_exe, "-m", "pip", "--version"], timeout=10)
                if result.returncode != 0:
                    issues.append("pip is not available or not working")
            except Exception:
                issues.append("pip is not available")
        
        return len(issues) == 0, issues
    
    def repair(self) -> bool:
        """Attempt to repair the environment."""
        print_info(f"Attempting to repair environment '{self.name}'")
        
        valid, issues = self.validate()
        if valid:
            print_success("Environment is already valid")
            return True
        
        # Try to reinstall pip if it's missing
        python_exe = self.python_executable
        if python_exe and Path(python_exe).exists():
            try:
                print_info("Reinstalling pip...")
                result = run_command([
                    python_exe, "-m", "ensurepip", "--upgrade"
                ], timeout=60)
                
                if result.returncode == 0:
                    print_success("Successfully repaired environment")
                    return True
                else:
                    print_error("Failed to repair environment")
                    return False
            except Exception as e:
                print_error("Failed to repair environment", str(e))
                return False
        
        print_error("Cannot repair environment - too many issues")
        return False
    
    def clean_cache(self) -> bool:
        """Clean pip cache for this environment."""
        if not self.exists:
            return False
        
        python_exe = self.python_executable
        if not python_exe:
            return False
        
        try:
            result = run_command([
                python_exe, "-m", "pip", "cache", "purge"
            ], timeout=30)
            
            return result.returncode == 0
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert environment info to dictionary."""
        info = self.get_info()
        return asdict(info)
    
    def __str__(self) -> str:
        """String representation of environment."""
        return f"Environment('{self.name}' at '{self.path}')"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Environment(name='{self.name}', path='{self.path}', exists={self.exists})" 