# 🐍 EnvFy - Professional Virtual Environment Manager

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/envfy.svg)](https://pypi.org/project/envfy/)

**EnvFy** is a fast, precise, and user-friendly Python virtual environment management tool that makes working with virtual environments as easy as using pip! 

## ✨ Features

- 🚀 **Lightning-fast** environment creation and management
- 🎨 **Beautiful CLI** with rich output and progress bars
- 🔍 **Smart Python detection** - automatically finds all Python versions
- 📦 **Package management** - install, uninstall, and manage packages effortlessly
- 🎯 **Environment templates** - quickly create environments from predefined templates
- 🔄 **Environment cloning** - duplicate environments with all packages
- 💾 **Backup & restore** - safely backup and restore environments
- 🔧 **Advanced configuration** - customize everything to your needs
- 🌍 **Cross-platform** - works on Windows, macOS, and Linux
- ⚡ **Performance optimized** - smart caching for faster operations

## 🚀 Quick Start

### Installation

#### 🌍 Cross-Platform Installation (Recommended)

**One-Line Installation:**

```bash
# Unix-like systems (macOS/Linux)
<<<<<<< HEAD
curl -fsSL https://raw.githubusercontent.com/Pymmdrza/envfy/main/install.sh | bash

# Windows PowerShell
iwr -useb https://raw.githubusercontent.com/Pymmdrza/envfy/main/install.ps1 | iex
=======
curl -fsSL https://raw.githubusercontent.com/Pymmdrza/Package_envFy/main/install.sh | bash

# Windows PowerShell
iwr -useb https://raw.githubusercontent.com/Pymmdrza/Package_envFy/main/install.ps1 | iex
>>>>>>> 69685c97194c7ea6dacfcbf23ab95ac6c5a66fab
```

#### 📦 Package Manager Installation

**🐧 Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3-pip
pip install envfy[uv]

# Fedora/RHEL/CentOS
sudo dnf install python3-pip
pip install envfy[uv]

# Arch Linux
sudo pacman -S python-pip
pip install envfy[uv]

# openSUSE
sudo zypper install python3-pip
pip install envfy[uv]
```

**🍎 macOS:**
```bash
# Homebrew (recommended)
brew install python3
pip3 install envfy[uv]

# MacPorts
sudo port install py311-pip
pip install envfy[uv]

# Direct Python installation
pip3 install envfy[uv]
```

**🪟 Windows:**
```powershell
# Using winget (Windows Package Manager)
winget install Python.Python.3.11
pip install envfy[uv]

# Using Chocolatey
choco install python3
pip install envfy[uv]

# Using Scoop
scoop install python
pip install envfy[uv]

# Direct pip installation
pip install envfy[uv]
```

#### 🚀 Manual Installation

```bash
# Basic installation
pip install envfy

# With UV support (ultra-fast package installation)
pip install envfy[uv]

# Development version with all features
pip install envfy[all]

# From source
<<<<<<< HEAD
git clone https://github.com/Pymmdrza/envfy.git
=======
git clone https://github.com/Pymmdrza/Package_envFy.git
>>>>>>> 69685c97194c7ea6dacfcbf23ab95ac6c5a66fab
cd envfy
pip install -e .[uv]
```

#### ✅ Verify Installation

```bash
# Check installation
envfy --version

# Show platform information
envfy platform

# Test basic functionality
envfy create test-env --packages requests
envfy list
envfy delete test-env --force
```

### Basic Usage

```bash
# Create a new environment
envfy create myproject

# Create with shorthand syntax
envfy --create --new myproject
envfy -c -n myproject

# Create with specific Python version
envfy create myproject --python 3.9
envfy --create --new myproject --python 3.9

# Create with packages
envfy create myproject --packages requests pandas numpy
envfy -c -n myproject --packages requests pandas

# Create with UV for ultra-fast installation
envfy create myproject --packages "fastapi uvicorn" --uv
envfy -c -n myproject --packages "django redis" --uv

# Create from requirements file
envfy create myproject --requirements requirements.txt
envfy --create --new myproject --requirements requirements.txt

# Create from requirements with UV
envfy create myproject --requirements requirements.txt --uv

# List all environments
envfy list

# Activate an environment (shows activation command)
envfy activate myproject

# Install packages in an environment
envfy install myproject requests beautifulsoup4

# Install packages with UV (ultra-fast!)
envfy install myproject --packages "numpy scipy matplotlib" --uv

# Clone an environment
envfy clone myproject myproject-backup

# Delete an environment
envfy delete myproject
```

## 📖 Documentation

### Environment Management

#### Creating Environments

```bash
# Basic environment
envfy create webproject

# Basic environment (shorthand)
envfy --create --new webproject
envfy -c -n webproject

# With specific Python version
envfy create webproject --python 3.10
envfy -c -n webproject --python 3.10

# With description
envfy create webproject --description "Web scraping project"
envfy -c -n webproject --description "Web scraping project"

# With template
envfy create webproject --template web
envfy -c -n webproject --template web

# With packages and requirements
envfy create webproject \
    --packages flask requests \
    --requirements requirements.txt \
    --python 3.9

# Shorthand with packages and requirements
envfy -c -n webproject \
    --packages flask requests \
    --requirements requirements.txt \
    --python 3.9
```

#### Environment Information

```bash
# List all environments
envfy list

# Detailed listing
envfy list --detailed

# JSON output
envfy list --json

# Show specific environment info
envfy info webproject
```

#### Environment Operations

```bash
# Clone environment
envfy clone webproject webproject-v2

# Backup environment
envfy backup webproject

# Restore from backup
envfy restore backup.tar.gz newproject

# Delete environment
envfy delete webproject

# Rename environment
envfy rename oldname newname
```

### Package Management

```bash
# Install packages
envfy install myproject requests pandas

# Install with options
envfy install myproject --upgrade requests
envfy install myproject --editable ./my-package

# Install from requirements
envfy install myproject --requirements requirements.txt

# Uninstall packages
envfy uninstall myproject requests

# Export requirements
envfy freeze myproject > requirements.txt
envfy freeze myproject --output requirements.txt
```

### Python Version Management

```bash
# Show available Python versions
envfy python

# Create environment with specific version
envfy create project39 --python 3.9.7
envfy create project310 --python python3.10
```

### Configuration

```bash
# Show current configuration
envfy config show

# Set configuration values
envfy config set default_python_version 3.9
envfy config set show_banner false

# Reset configuration
envfy config reset
```

### Maintenance

```bash
# Diagnose issues
envfy doctor

# Clean caches
envfy clean

# Clean specific caches
envfy clean --environments
envfy clean --downloads
```

## 🎯 Advanced Usage

### Environment Templates

Create reusable environment templates:

```toml
# ~/.envfy/templates/web.toml
[template]
name = "web"
description = "Web development environment"
python_version = "3.9"

[packages]
base = [
    "flask>=2.0.0",
    "requests>=2.25.0",
    "beautifulsoup4",
    "pytest",
    "black",
    "flake8"
]

[optional]
database = ["sqlalchemy", "alembic"]
async = ["aiohttp", "asyncio"]
```

Use template:
```bash
envfy create mywebapp --template web
```

### Configuration File

Customize EnvFy behavior:

```toml
# ~/.envfy/config/config.toml
[global]
default_python_version = "3.9"
auto_activate = false
show_banner = true
colored_output = true
parallel_installs = true
max_workers = 4

[network]
timeout = 30
retries = 3
index_url = "https://pypi.org/simple/"

[cache]
enabled = true
ttl = 3600
```

### Programmatic Usage

Use EnvFy in your Python scripts:

```python
from envfy import EnvironmentManager, Environment

# Create manager
manager = EnvironmentManager()

# Create environment
env = manager.create_environment(
    name="myproject",
    python_version="3.9",
    packages=["requests", "pandas"]
)

# Use environment
if env:
    env.install_package("numpy")
    packages = env.get_packages()
    print(f"Installed packages: {len(packages)}")

# List environments
environments = manager.list_environments()
for env_name in environments:
    env = manager.get_environment(env_name)
    info = env.get_info()
    print(f"{env_name}: {info.python_version}")
```

## 🛠️ Commands Reference

### Core Commands

| Command | Description | Cross-Platform |
|---------|-------------|----------------|
| `create` | Create a new virtual environment | ✅ All platforms |
| `delete` | Delete a virtual environment | ✅ All platforms |
| `list` | List all environments | ✅ All platforms |
| `info` | Show detailed environment information | ✅ All platforms |
| `activate` | Show activation command | ✅ All platforms |
| `clone` | Clone an environment | ✅ All platforms |

### Package Commands

| Command | Description | Cross-Platform |
|---------|-------------|----------------|
| `install` | Install packages in environment | ✅ All platforms |
| `uninstall` | Uninstall packages from environment | ✅ All platforms |
| `freeze` | Export environment packages | ✅ All platforms |

### System Commands

| Command | Description | Cross-Platform |
|---------|-------------|----------------|
| `python` | Show available Python versions | ✅ All platforms |
| `platform` | Show platform info and installation methods | ✅ All platforms |
| `config` | Configuration management | ✅ All platforms |
| `clean` | Clean caches and temporary files | ✅ All platforms |
| `doctor` | Diagnose and fix issues | ✅ All platforms |

### Platform-Specific Features

**Windows:**
- PowerShell and Command Prompt support
- Windows Terminal integration
- Automatic PATH configuration
- UAC-aware installation

**macOS:**
- Homebrew integration
- Apple Silicon (M1/M2) support
- Xcode command line tools detection
- Framework Python support

**Linux:**
- Distribution package manager integration
- Snap/Flatpak support
- pyenv compatibility
- SELinux compatibility

### Command Options

Most commands support these common options:

| Option | Description |
|--------|-------------|
| `--force` | Force operation without confirmation |
| `--verbose` | Enable verbose output |
| `--help` | Show command help |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVFY_HOME` | EnvFy home directory | `~/.envfy` |
| `ENVFY_CONFIG` | Configuration file path | `~/.envfy/config/config.toml` |

### Directory Structure

```
~/.envfy/
├── config/
│   ├── config.toml          # Global configuration
│   └── environments/        # Environment-specific configs
├── environments/            # Virtual environments
├── templates/              # Environment templates
└── cache/                 # Cache and temporary files
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
<<<<<<< HEAD
git clone https://github.com/pymmdrza/envfy.git
=======
git clone https://github.com/Pymmdrza/Package_envFy.git
>>>>>>> 69685c97194c7ea6dacfcbf23ab95ac6c5a66fab
cd envfy

# Create development environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black envfy/
isort envfy/

# Lint code
flake8 envfy/
mypy envfy/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

- 📖 [Documentation](https://envfy.readthedocs.io/)
<<<<<<< HEAD
- 🐛 [Issue Tracker](https://github.com/pymmdrza/envfy/issues)
- 💬 [Discussions](https://github.com/pymmdrza/envfy/discussions)
=======
- 🐛 [Issue Tracker](https://github.com/Pymmdrza/Package_envFy/issues)
- 💬 [Discussions](https://github.com/Pymmdrza/Package_envFy/discussions)
>>>>>>> 69685c97194c7ea6dacfcbf23ab95ac6c5a66fab
- 📧 [Email Support](mailto:pymmdrza@gmail.com)

## 🌟 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for the CLI
- Beautiful output powered by [Rich](https://rich.readthedocs.io/)
- Virtual environments created with [virtualenv](https://virtualenv.pypa.io/)
- Configuration management using [TOML](https://toml.io/)

## ⚡ UV Integration - Ultra-Fast Package Installation

EnvFy integrates seamlessly with [UV](https://github.com/astral-sh/uv), the ultra-fast Python package installer and resolver written in Rust. UV can be **10-100x faster** than pip for package installation!

### 🚀 Why Use UV with EnvFy?

- **🔥 Blazing Fast**: 10-100x faster than pip
- **🧠 Smart Caching**: Intelligent dependency resolution
- **🔒 Reliable**: Production-ready with excellent compatibility
- **🪶 Lightweight**: Minimal overhead, maximum performance

### 📦 Installation

```bash
# Install EnvFy with UV support
pip install envfy[uv]

# Or install UV separately
pip install uv

# Or use UV to install EnvFy itself!
uv pip install envfy
```

### 🎯 Usage Examples

#### Environment Creation with UV

```bash
# Create environment and install packages with UV
envfy create myproject --packages "fastapi uvicorn" --uv

# Shorthand with UV
envfy -c -n myproject --packages "django psycopg2-binary" --uv

# From requirements file with UV
envfy create webapp --requirements requirements.txt --uv
```

#### Package Management with UV

```bash
# Install packages using UV (ultra-fast!)
envfy install myproject --packages "numpy pandas matplotlib" --uv

# Upgrade packages with UV
envfy install myproject --upgrade "requests aiohttp" --uv

# Install from requirements with UV
envfy install myproject --requirements requirements.txt --uv
```

### ⚡ Performance Comparison

| Operation | pip | UV | Speedup |
|-----------|-----|----| --------|
| Install numpy | 8.2s | 0.9s | **9.1x** |
| Install Django | 12.4s | 1.2s | **10.3x** |
| Install 50 packages | 3m 21s | 24s | **8.4x** |
| Cold dependency resolution | 45s | 3s | **15x** |

### 🔧 Configuration

You can set UV as the default package manager:

```bash
# Set UV as default for new environments
envfy config set default_package_manager uv

# Always use UV for installations
envfy config set always_use_uv true
```

### 💡 Pro Tips

1. **First-time setup**: Install UV globally for maximum benefit
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Hybrid approach**: Use UV for fast installs, pip for compatibility
   ```bash
   envfy install myproject --packages "common-package" --uv
   envfy install myproject --packages "edge-case-package"  # uses pip
   ```

3. **CI/CD optimization**: UV dramatically speeds up CI pipelines
   ```yaml
   # .github/workflows/test.yml
   - name: Create test environment
     run: envfy create test-env --requirements requirements.txt --uv
   ```

### 🤝 UV + EnvFy Integration Features

- **🔄 Automatic fallback**: Falls back to pip if UV is not available
- **🎯 Selective usage**: Choose UV per command with `--uv` flag
- **📊 Performance monitoring**: Track installation speeds
- **🔧 Full compatibility**: All EnvFy features work with UV
- **⚙️ Configuration**: Set UV as default in global config

### 🛠️ Advanced UV Usage

```bash
# Create environment with UV and specific Python version
envfy -c -n ml-project --python 3.11 --packages "torch tensorflow" --uv

# Clone environment and upgrade all packages with UV
envfy clone old-env new-env
envfy install new-env --upgrade-all --uv

# Export and recreate with UV for faster setup
envfy freeze old-env > requirements.txt
envfy create fast-env --requirements requirements.txt --uv
```

---

**Made with ❤️ by the EnvFy team**

*Fast, Precise, Professional Virtual Environment Management* 
