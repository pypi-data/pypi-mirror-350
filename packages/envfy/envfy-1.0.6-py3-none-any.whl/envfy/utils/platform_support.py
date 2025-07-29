#!/usr/bin/env python3
"""
EnvFy Cross-Platform Support

Handles platform-specific functionality for Windows, macOS, and Linux.
"""

import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from .exceptions import PlatformNotSupportedError, PythonNotFoundError


class PlatformInfo:
    """Platform information and utilities."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.version = platform.version()
        self.python_version = platform.python_version()
        
    @property
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return self.system == "windows"
    
    @property
    def is_macos(self) -> bool:
        """Check if running on macOS."""
        return self.system == "darwin"
    
    @property
    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return self.system == "linux"
    
    @property
    def is_unix_like(self) -> bool:
        """Check if running on Unix-like system (macOS/Linux)."""
        return self.is_macos or self.is_linux
    
    @property
    def shell_type(self) -> str:
        """Detect the current shell type."""
        if self.is_windows:
            # Check for PowerShell vs Command Prompt
            if os.environ.get("PSModulePath"):
                return "powershell"
            else:
                return "cmd"
        else:
            # Unix-like systems
            shell = os.environ.get("SHELL", "/bin/bash")
            if "zsh" in shell:
                return "zsh"
            elif "fish" in shell:
                return "fish"
            elif "csh" in shell or "tcsh" in shell:
                return "csh"
            else:
                return "bash"
    
    @property
    def executable_extension(self) -> str:
        """Get executable file extension for the platform."""
        return ".exe" if self.is_windows else ""
    
    @property
    def script_extension(self) -> str:
        """Get script file extension for the platform."""
        if self.is_windows:
            shell = self.shell_type
            if shell == "powershell":
                return ".ps1"
            else:
                return ".bat"
        return ".sh"
    
    @property
    def path_separator(self) -> str:
        """Get path separator for the platform."""
        return ";" if self.is_windows else ":"
    
    def get_home_directory(self) -> Path:
        """Get user home directory."""
        return Path.home()
    
    def get_config_directory(self) -> Path:
        """Get user configuration directory."""
        if self.is_windows:
            # Use AppData/Roaming on Windows
            return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif self.is_macos:
            # Use ~/Library/Application Support on macOS
            return Path.home() / "Library" / "Application Support"
        else:
            # Use ~/.config on Linux
            return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    
    def get_cache_directory(self) -> Path:
        """Get user cache directory."""
        if self.is_windows:
            # Use AppData/Local on Windows
            return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        elif self.is_macos:
            # Use ~/Library/Caches on macOS
            return Path.home() / "Library" / "Caches"
        else:
            # Use ~/.cache on Linux
            return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))


class PythonDetector:
    """Cross-platform Python detection and management."""
    
    def __init__(self, platform_info: PlatformInfo):
        self.platform = platform_info
    
    def get_python_search_paths(self) -> List[Path]:
        """Get platform-specific Python search paths."""
        paths = []
        
        if self.platform.is_windows:
            # Windows Python search paths
            paths.extend([
                Path("C:\\Python*"),
                Path("C:\\Program Files\\Python*"),
                Path("C:\\Program Files (x86)\\Python*"),
                Path(os.environ.get("USERPROFILE", "")) / "AppData" / "Local" / "Programs" / "Python" / "Python*",
                Path(os.environ.get("PROGRAMFILES", "")) / "Python*",
                Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Python*",
            ])
        elif self.platform.is_macos:
            # macOS Python search paths
            paths.extend([
                Path("/usr/bin"),
                Path("/usr/local/bin"),
                Path("/opt/homebrew/bin"),
                Path("/System/Library/Frameworks/Python.framework/Versions/*/bin"),
                Path("/Library/Frameworks/Python.framework/Versions/*/bin"),
                Path.home() / ".pyenv" / "versions" / "*" / "bin",
            ])
        else:
            # Linux Python search paths
            paths.extend([
                Path("/usr/bin"),
                Path("/usr/local/bin"),
                Path("/opt/python*/bin"),
                Path.home() / ".pyenv" / "versions" / "*" / "bin",
                Path.home() / ".local" / "bin",
            ])
        
        return paths
    
    def get_python_executable_names(self) -> List[str]:
        """Get platform-specific Python executable names."""
        names = []
        
        # Common Python executable names
        base_names = [
            "python3.12", "python3.11", "python3.10", "python3.9",
            "python3.8", "python3.7", "python3", "python"
        ]
        
        if self.platform.is_windows:
            # Add .exe extension for Windows
            names.extend([f"{name}.exe" for name in base_names])
            names.extend(base_names)  # Some Windows installations don't use .exe
        else:
            names.extend(base_names)
        
        return names
    
    def find_python_installations(self) -> List[Dict[str, str]]:
        """Find all Python installations on the system."""
        installations = []
        found_paths = set()
        
        # Search in PATH first
        for name in self.get_python_executable_names():
            executable = shutil.which(name)
            if executable and executable not in found_paths:
                version = self._get_python_version(executable)
                if version:
                    installations.append({
                        "name": name,
                        "executable": executable,
                        "version": version,
                        "source": "PATH"
                    })
                    found_paths.add(executable)
        
        # Search in platform-specific locations
        for search_path in self.get_python_search_paths():
            if search_path.exists():
                for executable_name in self.get_python_executable_names():
                    for python_path in search_path.rglob(executable_name):
                        if python_path.is_file() and os.access(python_path, os.X_OK):
                            executable = str(python_path)
                            if executable not in found_paths:
                                version = self._get_python_version(executable)
                                if version:
                                    installations.append({
                                        "name": python_path.name,
                                        "executable": executable,
                                        "version": version,
                                        "source": "filesystem"
                                    })
                                    found_paths.add(executable)
        
        # Sort by version (newest first)
        try:
            from packaging.version import parse
            installations.sort(key=lambda x: parse(x["version"]), reverse=True)
        except ImportError:
            # Fallback to string sorting
            installations.sort(key=lambda x: x["version"], reverse=True)
        
        return installations
    
    def _get_python_version(self, executable: str) -> Optional[str]:
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
                import re
                match = re.search(r"Python (\d+\.\d+\.\d+)", result.stdout)
                if match:
                    return match.group(1)
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        return None


class ActivationHandler:
    """Handle environment activation for different platforms and shells."""
    
    def __init__(self, platform_info: PlatformInfo):
        self.platform = platform_info
    
    def get_activation_script_path(self, env_path: Path) -> Path:
        """Get path to activation script for the platform."""
        if self.platform.is_windows:
            return env_path / "Scripts" / "activate.bat"
        else:
            return env_path / "bin" / "activate"
    
    def get_activation_command(self, env_path: Path) -> str:
        """Get platform and shell-specific activation command."""
        if self.platform.is_windows:
            if self.platform.shell_type == "powershell":
                return f"{env_path}\\Scripts\\Activate.ps1"
            else:
                return f"{env_path}\\Scripts\\activate.bat"
        else:
            return f"source {env_path}/bin/activate"
    
    def get_deactivation_command(self) -> str:
        """Get deactivation command for the platform."""
        return "deactivate"
    
    def get_python_executable_path(self, env_path: Path) -> Path:
        """Get Python executable path in virtual environment."""
        if self.platform.is_windows:
            return env_path / "Scripts" / "python.exe"
        else:
            return env_path / "bin" / "python"
    
    def get_pip_executable_path(self, env_path: Path) -> Path:
        """Get pip executable path in virtual environment."""
        if self.platform.is_windows:
            return env_path / "Scripts" / "pip.exe"
        else:
            return env_path / "bin" / "pip"
    
    def get_environment_variables(self, env_path: Path) -> Dict[str, str]:
        """Get environment variables for activation."""
        env_vars = {
            "VIRTUAL_ENV": str(env_path),
            "VIRTUAL_ENV_PROMPT": f"({env_path.name})",
        }
        
        # Update PATH
        if self.platform.is_windows:
            scripts_dir = env_path / "Scripts"
            current_path = os.environ.get("PATH", "")
            env_vars["PATH"] = f"{scripts_dir}{self.platform.path_separator}{current_path}"
        else:
            bin_dir = env_path / "bin"
            current_path = os.environ.get("PATH", "")
            env_vars["PATH"] = f"{bin_dir}{self.platform.path_separator}{current_path}"
        
        return env_vars


class InstallationHelper:
    """Help with cross-platform installation and setup."""
    
    def __init__(self, platform_info: PlatformInfo):
        self.platform = platform_info
    
    def get_installation_methods(self) -> Dict[str, List[str]]:
        """Get platform-specific installation methods."""
        methods = {
            "pip": ["pip install envfy", "pip install envfy[uv]", "pip install envfy[all]"],
            "pipx": ["pipx install envfy", "pipx install envfy[uv]"],
        }
        
        if self.platform.is_windows:
            methods.update({
                "winget": ["winget install envfy"],
                "chocolatey": ["choco install envfy"],
                "scoop": ["scoop install envfy"],
            })
        elif self.platform.is_macos:
            methods.update({
                "homebrew": ["brew install envfy"],
                "macports": ["sudo port install py-envfy"],
            })
        else:  # Linux
            methods.update({
                "apt": ["sudo apt install python3-envfy"],
                "yum": ["sudo yum install python3-envfy"],
                "dnf": ["sudo dnf install python3-envfy"],
                "pacman": ["sudo pacman -S python-envfy"],
                "snap": ["sudo snap install envfy"],
            })
        
        return methods
    
    def get_shell_completion_setup(self) -> Dict[str, str]:
        """Get shell completion setup commands."""
        shell = self.platform.shell_type
        
        completions = {
            "bash": "eval \"$(_ENVFY_COMPLETE=bash_source envfy)\" >> ~/.bashrc",
            "zsh": "eval \"$(_ENVFY_COMPLETE=zsh_source envfy)\" >> ~/.zshrc",
            "fish": "_ENVFY_COMPLETE=fish_source envfy | source",
            "powershell": "Register-ArgumentCompleter -Native -CommandName envfy -ScriptBlock { ... }",
            "cmd": "# Tab completion not available for CMD",
        }
        
        return {shell: completions.get(shell, "# Completion not available for this shell")}
    
    def get_path_setup_instructions(self) -> List[str]:
        """Get instructions for adding EnvFy to PATH."""
        if self.platform.is_windows:
            return [
                "Add EnvFy to PATH in Windows:",
                "1. Open System Properties > Environment Variables",
                "2. Add the EnvFy installation directory to PATH",
                "3. Restart your terminal/command prompt",
                "",
                "Or use PowerShell:",
                r'$env:PATH += ";" + (pip show envfy | Select-String "Location").ToString().Split()[-1] + "\Scripts"'
            ]
        else:
            shell = self.platform.shell_type
            if shell == "zsh":
                config_file = "~/.zshrc"
            elif shell == "fish":
                config_file = "~/.config/fish/config.fish"
            else:
                config_file = "~/.bashrc"
            
            return [
                f"Add EnvFy to PATH in {shell}:",
                f'echo \'export PATH="$HOME/.local/bin:$PATH"\' >> {config_file}',
                "source " + config_file,
                "",
                "Or for system-wide installation:",
                "sudo ln -s $(which envfy) /usr/local/bin/envfy"
            ]


# Global platform instance
_platform_info = None
_python_detector = None
_activation_handler = None
_installation_helper = None


def get_platform_info() -> PlatformInfo:
    """Get global platform information instance."""
    global _platform_info
    if _platform_info is None:
        _platform_info = PlatformInfo()
    return _platform_info


def get_python_detector() -> PythonDetector:
    """Get global Python detector instance."""
    global _python_detector
    if _python_detector is None:
        _python_detector = PythonDetector(get_platform_info())
    return _python_detector


def get_activation_handler() -> ActivationHandler:
    """Get global activation handler instance."""
    global _activation_handler
    if _activation_handler is None:
        _activation_handler = ActivationHandler(get_platform_info())
    return _activation_handler


def get_installation_helper() -> InstallationHelper:
    """Get global installation helper instance."""
    global _installation_helper
    if _installation_helper is None:
        _installation_helper = InstallationHelper(get_platform_info())
    return _installation_helper


def check_platform_compatibility() -> Tuple[bool, List[str]]:
    """Check if the current platform is supported."""
    platform_info = get_platform_info()
    issues = []
    
    # Check Python version
    import sys
    if sys.version_info < (3, 7):
        issues.append(f"Python {sys.version} is not supported. Python 3.7+ is required.")
    
    # Check platform support
    if not (platform_info.is_windows or platform_info.is_macos or platform_info.is_linux):
        issues.append(f"Platform {platform_info.system} is not officially supported.")
    
    # Check required tools
    required_tools = ["pip"]
    for tool in required_tools:
        if not shutil.which(tool):
            issues.append(f"Required tool '{tool}' is not available.")
    
    return len(issues) == 0, issues 