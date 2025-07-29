#!/usr/bin/env python3
"""
EnvFy Helper Utilities

Utility functions for filesystem operations, Python discovery, and other common tasks.
"""

import os
import sys
import shutil
import subprocess
import platform
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Union, Any
from packaging.version import Version, parse
import psutil

from .exceptions import PythonNotFoundError, PermissionError as EnvFyPermissionError


def get_envfy_home() -> Path:
    """Get the EnvFy home directory."""
    home_dir = os.environ.get("ENVFY_HOME")
    if home_dir:
        return Path(home_dir)
    
    # Default to ~/.envfy
    return Path.home() / ".envfy"


def get_environments_dir() -> Path:
    """Get the directory where environments are stored."""
    return get_envfy_home() / "environments"


def get_cache_dir() -> Path:
    """Get the cache directory."""
    return get_envfy_home() / "cache"


def get_config_dir() -> Path:
    """Get the configuration directory."""
    return get_envfy_home() / "config"


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure a directory exists, create if it doesn't."""
    path = Path(path)
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except PermissionError as e:
        raise EnvFyPermissionError("create directory", str(path)) from e


def create_directory(path: Union[str, Path]) -> Path:
    """Create a directory."""
    return ensure_directory(path)


def remove_directory(path: Union[str, Path], force: bool = False) -> None:
    """Remove a directory and all its contents."""
    path = Path(path)
    if not path.exists():
        return
    
    try:
        if force and platform.system() == "Windows":
            # Handle Windows readonly files
            def handle_remove_readonly(func, path, exc):
                os.chmod(path, 0o777)
                func(path)
            shutil.rmtree(path, onerror=handle_remove_readonly)
        else:
            shutil.rmtree(path)
    except PermissionError as e:
        raise EnvFyPermissionError("remove directory", str(path)) from e


def copy_directory(src: Union[str, Path], dst: Union[str, Path]) -> None:
    """Copy a directory and all its contents."""
    src, dst = Path(src), Path(dst)
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
    except PermissionError as e:
        raise EnvFyPermissionError("copy directory", str(src)) from e


def get_file_hash(file_path: Union[str, Path]) -> str:
    """Get SHA256 hash of a file."""
    file_path = Path(file_path)
    if not file_path.exists():
        return ""
    
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def is_valid_env_name(name: str) -> bool:
    """Check if environment name is valid."""
    if not name:
        return False
    
    # Must start with letter or underscore
    if not (name[0].isalpha() or name[0] == "_"):
        return False
    
    # Can contain letters, numbers, underscores, hyphens
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_-]*$"
    return bool(re.match(pattern, name))


def get_python_executables() -> List[Dict[str, str]]:
    """Find all available Python executables on the system."""
    executables = []
    
    # Common Python executable names
    python_names = [
        "python3.12", "python3.11", "python3.10", "python3.9", 
        "python3.8", "python3.7", "python3", "python"
    ]
    
    # Check system PATH
    for name in python_names:
        executable = shutil.which(name)
        if executable:
            version = get_python_version(executable)
            if version:
                executables.append({
                    "name": name,
                    "executable": executable,
                    "version": version,
                    "available": True
                })
    
    # Check common installation directories
    if platform.system() == "Windows":
        # Windows Python installations
        python_dirs = [
            "C:\\Python*",
            "C:\\Program Files\\Python*",
            "C:\\Program Files (x86)\\Python*",
            f"{os.environ.get('USERPROFILE', '')}\\AppData\\Local\\Programs\\Python\\Python*"
        ]
        
        for pattern in python_dirs:
            for path in Path().glob(pattern):
                python_exe = path / "python.exe"
                if python_exe.exists():
                    version = get_python_version(str(python_exe))
                    if version:
                        executables.append({
                            "name": f"python{version}",
                            "executable": str(python_exe),
                            "version": version,
                            "available": True
                        })
    
    elif platform.system() == "Darwin":
        # macOS Python installations
        mac_dirs = [
            "/usr/bin/python*",
            "/usr/local/bin/python*",
            "/opt/homebrew/bin/python*",
            "/System/Library/Frameworks/Python.framework/Versions/*/bin/python*"
        ]
        
        for pattern in mac_dirs:
            for path in Path().glob(pattern):
                if path.is_file() and os.access(path, os.X_OK):
                    version = get_python_version(str(path))
                    if version:
                        executables.append({
                            "name": path.name,
                            "executable": str(path),
                            "version": version,
                            "available": True
                        })
    
    else:
        # Linux Python installations
        linux_dirs = [
            "/usr/bin/python*",
            "/usr/local/bin/python*",
            "/opt/python*/bin/python*"
        ]
        
        for pattern in linux_dirs:
            for path in Path().glob(pattern):
                if path.is_file() and os.access(path, os.X_OK):
                    version = get_python_version(str(path))
                    if version:
                        executables.append({
                            "name": path.name,
                            "executable": str(path),
                            "version": version,
                            "available": True
                        })
    
    # Remove duplicates and sort by version
    unique_executables = {}
    for exe in executables:
        key = exe["version"]
        if key not in unique_executables or len(exe["executable"]) < len(unique_executables[key]["executable"]):
            unique_executables[key] = exe
    
    sorted_executables = sorted(
        unique_executables.values(),
        key=lambda x: parse(x["version"]),
        reverse=True
    )
    
    return sorted_executables


def get_python_version(executable: str) -> Optional[str]:
    """Get Python version from executable."""
    try:
        result = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse version from output like "Python 3.9.7"
            match = re.search(r"Python (\d+\.\d+\.\d+)", result.stdout)
            if match:
                return match.group(1)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    
    return None


def find_python_executable(version: Optional[str] = None) -> str:
    """Find Python executable for the specified version."""
    executables = get_python_executables()
    
    if not executables:
        raise PythonNotFoundError()
    
    if version:
        # Find exact version match
        for exe in executables:
            if exe["version"] == version:
                return exe["executable"]
        
        # Find compatible version (same major.minor)
        target_parts = version.split(".")
        for exe in executables:
            exe_parts = exe["version"].split(".")
            if (len(target_parts) >= 2 and len(exe_parts) >= 2 and
                target_parts[0] == exe_parts[0] and 
                target_parts[1] == exe_parts[1]):
                return exe["executable"]
        
        raise PythonNotFoundError(version)
    
    # Return the latest available Python
    return executables[0]["executable"]


def run_command(
    command: List[str],
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    capture_output: bool = True,
    timeout: Optional[int] = None
) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            check=False
        )
    except subprocess.TimeoutExpired as e:
        raise subprocess.TimeoutExpired(e.cmd, e.timeout, e.output, e.stderr)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Command not found: {command[0]}") from e


def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "disk_usage": psutil.disk_usage("/").total if platform.system() != "Windows" else psutil.disk_usage("C:").total,
    }


def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def get_directory_size(path: Union[str, Path]) -> int:
    """Get total size of directory in bytes."""
    path = Path(path)
    total_size = 0
    
    try:
        for file_path in path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
    except (PermissionError, OSError):
        pass
    
    return total_size


def is_virtual_environment(path: Union[str, Path]) -> bool:
    """Check if a directory is a virtual environment."""
    path = Path(path)
    
    # Check for common virtual environment indicators
    indicators = [
        "pyvenv.cfg",
        "Scripts/activate" if platform.system() == "Windows" else "bin/activate",
        "Scripts/python.exe" if platform.system() == "Windows" else "bin/python",
    ]
    
    return any((path / indicator).exists() for indicator in indicators)


def get_environment_python(env_path: Union[str, Path]) -> Optional[str]:
    """Get Python executable path for an environment."""
    env_path = Path(env_path)
    
    if platform.system() == "Windows":
        python_exe = env_path / "Scripts" / "python.exe"
    else:
        python_exe = env_path / "bin" / "python"
    
    return str(python_exe) if python_exe.exists() else None


def activate_environment_command(env_path: Union[str, Path]) -> str:
    """Get the command to activate an environment."""
    env_path = Path(env_path)
    
    if platform.system() == "Windows":
        activate_script = env_path / "Scripts" / "activate.bat"
        return str(activate_script)
    else:
        activate_script = env_path / "bin" / "activate"
        return f"source {activate_script}"


def parse_requirements_file(requirements_file: Union[str, Path]) -> List[str]:
    """Parse a requirements.txt file and return list of packages."""
    requirements_file = Path(requirements_file)
    packages = []
    
    if not requirements_file.exists():
        return packages
    
    try:
        with open(requirements_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    # Handle -r includes
                    if line.startswith('-r '):
                        include_file = requirements_file.parent / line[3:].strip()
                        packages.extend(parse_requirements_file(include_file))
                    else:
                        packages.append(line)
    except Exception:
        pass
    
    return packages


def generate_environment_name(base_name: str = "env") -> str:
    """Generate a unique environment name."""
    envs_dir = get_environments_dir()
    counter = 1
    
    while True:
        if counter == 1:
            name = base_name
        else:
            name = f"{base_name}-{counter}"
        
        if not (envs_dir / name).exists():
            return name
        
        counter += 1


def is_port_available(port: int, host: str = "localhost") -> bool:
    """Check if a port is available."""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            return result != 0
    except Exception:
        return False


def get_available_port(start_port: int = 8000, end_port: int = 9000) -> Optional[int]:
    """Find an available port in the given range."""
    for port in range(start_port, end_port + 1):
        if is_port_available(port):
            return port
    return None 