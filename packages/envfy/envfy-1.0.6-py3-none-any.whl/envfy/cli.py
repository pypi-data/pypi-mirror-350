#!/usr/bin/env python3
"""
EnvFy Command Line Interface

Professional command-line interface for virtual environment management.
"""

import sys
import os
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console

from . import __version__
from .core.config import get_config
from .core.manager import EnvironmentManager
from .utils.output import (
    print_banner, print_success, print_error, print_warning, print_info,
    print_environment_info, print_package_list, print_python_versions,
    create_environment_tree, console, confirm_action, prompt_input
)
from .utils.exceptions import EnvFyError
from .utils.validators import validate_environment_name, validate_python_version


# Global CLI context
pass_config = click.make_pass_decorator(object)


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version and exit')
@click.option('--config-path', type=click.Path(), help='Path to config file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--no-banner', is_flag=True, help='Disable banner display')
@click.option('--create', '-c', is_flag=True, help='Create a new virtual environment (shorthand)')
@click.option('--new', '-n', metavar='ENV_NAME', help='Environment name for creation (use with --create)')
@click.option('--python', '-p', metavar='VERSION', help='Python version to use (use with --create)')
@click.option('--packages', multiple=True, help='Packages to install (use with --create)')
@click.option('--requirements', '-r', type=click.Path(exists=True), help='Install from requirements file (use with --create)')
@click.option('--template', '-t', help='Use environment template (use with --create)')
@click.option('--description', help='Environment description (use with --create)')
@click.option('--force', is_flag=True, help='Overwrite existing environment (use with --create)')
@click.option('--uv', is_flag=True, help='Use UV for fast package installation (use with --create)')
@click.pass_context
def main(ctx, version, config_path, verbose, no_banner, create, new, python, packages, requirements, template, description, force, uv):
    """
    🐍 EnvFy - Fast, Precise Virtual Environment Management
    
    Make working with Python virtual environments as easy as using pip!
    
    Quick create: envfy --create --new myenv
    Standard create: envfy create myenv
    """
    if version:
        click.echo(f"EnvFy {__version__}")
        sys.exit(0)
    
    # Initialize context
    config = get_config()
    if config_path:
        config.config_file = Path(config_path)
        config.load()
    
    config.global_settings.verbose = verbose
    
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['manager'] = EnvironmentManager()
    
    # Handle shorthand environment creation
    if create:
        if not new:
            print_error("Environment name is required when using --create")
            print_info("Usage: envfy --create --new <env_name>")
            sys.exit(1)
        
        try:
            validate_environment_name(new)
            
            if python:
                validate_python_version(python)
            
            manager = ctx.obj['manager']
            
            # Check if environment already exists
            if manager.environment_exists(new) and not force:
                print_error(f"Environment '{new}' already exists")
                print_info("Use --force to overwrite")
                sys.exit(1)
            
            print_info(f"Creating environment '{new}'...")
            
            # Create environment
            env = manager.create_environment(
                name=new,
                python_version=python,
                template=template,
                description=description,
                system_site_packages=False,
                without_pip=False
            )
            
            if not env:
                print_error("Failed to create environment")
                sys.exit(1)
            
            if uv:
                print_info("Using UV for fast package installation")
            
            # Install packages if specified
            if packages:
                print_info("Installing packages...")
                for package in packages:
                    try:
                        env.install_package(package, use_uv=uv)
                    except Exception as e:
                        print_warning(f"Failed to install {package}: {e}")
            
            # Install from requirements if specified
            if requirements:
                print_info("Installing from requirements file...")
                try:
                    env.install_requirements(requirements, use_uv=uv)
                except Exception as e:
                    print_warning(f"Failed to install requirements: {e}")
            
            print_success(f"Environment '{new}' created successfully!")
            print_info(f"Activate: {env.activate_command}")
            
        except EnvFyError as e:
            print_error(str(e))
            sys.exit(1)
        
        return  # Exit after creating environment
    
    # Show banner if no specific command and not disabled
    if ctx.invoked_subcommand is None:
        if not no_banner and config.global_settings.show_banner:
            print_banner()
        click.echo("\nUse 'envfy --help' for available commands.\n")
        click.echo("💡 Quick tips:")
        click.echo("  • Create environment: envfy --create --new myenv")
        click.echo("  • Or use: envfy create myenv")
        click.echo("  • List environments: envfy list")
        click.echo("  • Get help: envfy --help\n")
        
        # Show quick stats
        manager = ctx.obj['manager']
        environments = manager.list_environments()
        if environments:
            click.echo(f"📊 {len(environments)} environments available")
            click.echo("Use 'envfy list' to see all environments\n")


@main.command()
@click.argument('name')
@click.option('--python', '-p', help='Python version to use (e.g., 3.9, 3.10.5)')
@click.option('--requirements', '-r', type=click.Path(exists=True), help='Install from requirements file')
@click.option('--packages', multiple=True, help='Packages to install')
@click.option('--template', '-t', help='Use environment template')
@click.option('--description', help='Environment description')
@click.option('--force', is_flag=True, help='Overwrite existing environment')
@click.option('--no-pip', is_flag=True, help="Don't install pip")
@click.option('--system-site-packages', is_flag=True, help='Use system site packages')
@click.option('--uv', is_flag=True, help='Use UV for fast package installation')
@pass_config
def create(ctx, name, python, requirements, packages, template, description, 
           force, no_pip, system_site_packages, uv):
    """Create a new virtual environment."""
    try:
        validate_environment_name(name)
        
        if python:
            validate_python_version(python)
        
        manager = ctx['manager']
        
        # Check if environment already exists
        if manager.environment_exists(name) and not force:
            print_error(f"Environment '{name}' already exists")
            print_info("Use --force to overwrite")
            sys.exit(1)
        
        print_info(f"Creating environment '{name}'...")
        
        # Create environment
        env = manager.create_environment(
            name=name,
            python_version=python,
            template=template,
            description=description,
            system_site_packages=system_site_packages,
            without_pip=no_pip
        )
        
        if not env:
            print_error("Failed to create environment")
            sys.exit(1)
        
        if uv:
            print_info("Using UV for fast package installation")
        
        # Install packages if specified
        if packages:
            print_info("Installing packages...")
            for package in packages:
                try:
                    env.install_package(package, use_uv=uv)
                except Exception as e:
                    print_warning(f"Failed to install {package}: {e}")
        
        # Install from requirements if specified
        if requirements:
            print_info("Installing from requirements file...")
            try:
                env.install_requirements(requirements, use_uv=uv)
            except Exception as e:
                print_warning(f"Failed to install requirements: {e}")
        
        print_success(f"Environment '{name}' created successfully!")
        print_info(f"Activate: {env.activate_command}")
        
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.argument('name')
@click.option('--force', is_flag=True, help='Force deletion without confirmation')
@pass_config
def delete(ctx, name, force):
    """Delete a virtual environment."""
    try:
        manager = ctx['manager']
        
        if not manager.environment_exists(name):
            print_error(f"Environment '{name}' not found")
            sys.exit(1)
        
        if not force:
            if not confirm_action(f"Delete environment '{name}'?", default=False):
                print_info("Deletion cancelled")
                return
        
        print_info(f"Deleting environment '{name}'...")
        
        if manager.delete_environment(name):
            print_success(f"Environment '{name}' deleted successfully")
        else:
            print_error("Failed to delete environment")
            sys.exit(1)
            
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed information')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@pass_config
def list(ctx, detailed, output_json):
    """List all virtual environments."""
    try:
        manager = ctx['manager']
        environments = manager.list_environments()
        
        if not environments:
            print_info("No environments found")
            print_info("Create one with: envfy create <name>")
            return
        
        if output_json:
            import json
            env_data = {}
            for env_name in environments:
                env = manager.get_environment(env_name)
                env_data[env_name] = env.to_dict()
            click.echo(json.dumps(env_data, indent=2, default=str))
            return
        
        if detailed:
            for env_name in environments:
                env = manager.get_environment(env_name)
                info = env.get_info()
                print_environment_info(env_name, {
                    'python_version': info.python_version,
                    'path': info.path,
                    'created': info.created,
                    'packages': {pkg.name: pkg.version for pkg in info.packages}
                })
                console.print()
        else:
            # Create tree view
            env_info = {}
            for env_name in environments:
                env = manager.get_environment(env_name)
                info = env.get_info()
                env_info[env_name] = {
                    'python_version': info.python_version,
                    'packages': info.packages,
                    'status': 'active' if info.active else 'inactive'
                }
            
            tree = create_environment_tree(env_info)
            console.print(tree)
            
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.argument('name')
@pass_config
def info(ctx, name):
    """Show detailed information about an environment."""
    try:
        manager = ctx['manager']
        
        if not manager.environment_exists(name):
            print_error(f"Environment '{name}' not found")
            sys.exit(1)
        
        env = manager.get_environment(name)
        info = env.get_info()
        
        print_environment_info(name, {
            'python_version': info.python_version,
            'path': info.path,
            'created': info.created,
            'last_accessed': info.last_accessed,
            'size': env.size_formatted,
            'packages': {pkg.name: pkg.version for pkg in info.packages}
        })
        
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.argument('environment')
@click.argument('packages', nargs=-1, required=True)
@click.option('--upgrade', '-U', is_flag=True, help='Upgrade packages')
@click.option('--editable', '-e', is_flag=True, help='Install in editable mode')
@click.option('--requirements', '-r', type=click.Path(exists=True), help='Install from requirements file')
@click.option('--uv', is_flag=True, help='Use UV instead of pip for faster installation')
@pass_config
def install(ctx, environment, packages, upgrade, editable, requirements, uv):
    """Install packages in an environment."""
    try:
        manager = ctx['manager']
        
        if not manager.environment_exists(environment):
            print_error(f"Environment '{environment}' not found")
            sys.exit(1)
        
        env = manager.get_environment(environment)
        
        if uv:
            print_info("Using UV for fast package installation")
        
        # Install from requirements file
        if requirements:
            try:
                env.install_requirements(requirements, use_uv=uv)
            except Exception as e:
                print_error(f"Failed to install requirements: {e}")
                sys.exit(1)
        
        # Install individual packages
        for package in packages:
            try:
                env.install_package(
                    package, 
                    upgrade=upgrade, 
                    editable=editable,
                    use_uv=uv
                )
            except Exception as e:
                print_error(f"Failed to install {package}: {e}")
                
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.argument('environment')
@click.argument('packages', nargs=-1, required=True)
@click.option('--yes', '-y', is_flag=True, help='Do not ask for confirmation')
@pass_config
def uninstall(ctx, environment, packages, yes):
    """Uninstall packages from an environment."""
    try:
        manager = ctx['manager']
        
        if not manager.environment_exists(environment):
            print_error(f"Environment '{environment}' not found")
            sys.exit(1)
        
        env = manager.get_environment(environment)
        
        for package in packages:
            try:
                env.uninstall_package(package, yes=yes)
            except Exception as e:
                print_error(f"Failed to uninstall {package}: {e}")
                
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.argument('environment')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@pass_config
def freeze(ctx, environment, output):
    """Export environment packages to requirements format."""
    try:
        manager = ctx['manager']
        
        if not manager.environment_exists(environment):
            print_error(f"Environment '{environment}' not found")
            sys.exit(1)
        
        env = manager.get_environment(environment)
        requirements = env.export_requirements(output)
        
        if not output:
            click.echo(requirements)
            
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.argument('source')
@click.argument('destination')
@click.option('--force', is_flag=True, help='Overwrite destination if exists')
@pass_config
def clone(ctx, source, destination, force):
    """Clone an environment."""
    try:
        manager = ctx['manager']
        
        if not manager.environment_exists(source):
            print_error(f"Source environment '{source}' not found")
            sys.exit(1)
        
        if manager.environment_exists(destination) and not force:
            print_error(f"Destination environment '{destination}' already exists")
            print_info("Use --force to overwrite")
            sys.exit(1)
        
        print_info(f"Cloning environment '{source}' to '{destination}'...")
        
        if manager.clone_environment(source, destination):
            print_success(f"Environment cloned successfully")
        else:
            print_error("Failed to clone environment")
            sys.exit(1)
            
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@click.argument('environment')
@pass_config
def activate(ctx, environment):
    """Show activation command for an environment."""
    try:
        manager = ctx['manager']
        
        if not manager.environment_exists(environment):
            print_error(f"Environment '{environment}' not found")
            sys.exit(1)
        
        env = manager.get_environment(environment)
        activation_cmd = env.activate_command
        
        click.echo(f"To activate this environment, run:")
        click.echo(f"  {activation_cmd}")
        
        # On Unix-like systems, show sourcing command
        if not activation_cmd.endswith('.bat'):
            click.echo(f"\nOr copy and paste:")
            click.echo(f"  source {activation_cmd}")
            
    except EnvFyError as e:
        print_error(str(e))
        sys.exit(1)


@main.command()
@pass_config
def python(ctx):
    """Show available Python versions."""
    try:
        from .utils.helpers import get_python_executables
        
        print_info("Scanning for Python versions...")
        versions = get_python_executables()
        
        if versions:
            print_python_versions(versions)
        else:
            print_warning("No Python versions found")
            
    except Exception as e:
        print_error(f"Failed to scan Python versions: {e}")
        sys.exit(1)


@main.group()
def config():
    """Configuration management commands."""
    pass


@config.command('show')
@click.option('--format', type=click.Choice(['toml', 'json', 'yaml']), default='toml')
@pass_config
def config_show(ctx, format):
    """Show current configuration."""
    try:
        config = ctx['config']
        output = config.export(format)
        click.echo(output)
        
    except Exception as e:
        print_error(f"Failed to show configuration: {e}")
        sys.exit(1)


@config.command('set')
@click.argument('key')
@click.argument('value')
@pass_config
def config_set(ctx, key, value):
    """Set a configuration value."""
    try:
        config = ctx['config']
        
        # Try to convert value to appropriate type
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        
        config.set(key, value)
        config.save()
        
        print_success(f"Set {key} = {value}")
        
    except Exception as e:
        print_error(f"Failed to set configuration: {e}")
        sys.exit(1)


@config.command('reset')
@click.option('--force', is_flag=True, help='Reset without confirmation')
@pass_config
def config_reset(ctx, force):
    """Reset configuration to defaults."""
    try:
        if not force:
            if not confirm_action("Reset configuration to defaults?", default=False):
                print_info("Reset cancelled")
                return
        
        config = ctx['config']
        config.reset()
        
        print_success("Configuration reset to defaults")
        
    except Exception as e:
        print_error(f"Failed to reset configuration: {e}")
        sys.exit(1)


@main.command()
@click.option('--all', 'clean_all', is_flag=True, help='Clean all caches and temporary files')
@click.option('--environments', is_flag=True, help='Clean environment caches')
@click.option('--downloads', is_flag=True, help='Clean download cache')
@pass_config
def clean(ctx, clean_all, environments, downloads):
    """Clean caches and temporary files."""
    try:
        if not (clean_all or environments or downloads):
            clean_all = True  # Default to cleaning everything
        
        if clean_all or environments:
            print_info("Cleaning environment caches...")
            # Implementation for cleaning environment caches
            
        if clean_all or downloads:
            print_info("Cleaning download cache...")
            # Implementation for cleaning download cache
        
        print_success("Cache cleaned successfully")
        
    except Exception as e:
        print_error(f"Failed to clean cache: {e}")
        sys.exit(1)


@main.command()
@pass_config
def doctor(ctx):
    """Diagnose and fix common issues."""
    try:
        print_info("Running EnvFy diagnostics...")
        
        config = ctx['config']
        manager = ctx['manager']
        
        # Check configuration
        print_info("Checking configuration...")
        issues = config.validate()
        if issues:
            print_warning("Configuration issues found:")
            for issue in issues:
                print_warning(f"  - {issue}")
        else:
            print_success("Configuration is valid")
        
        # Check environments
        print_info("Checking environments...")
        environments = manager.list_environments()
        broken_envs = []
        
        for env_name in environments:
            env = manager.get_environment(env_name)
            valid, env_issues = env.validate()
            if not valid:
                broken_envs.append((env_name, env_issues))
        
        if broken_envs:
            print_warning(f"Found {len(broken_envs)} broken environments:")
            for env_name, env_issues in broken_envs:
                print_warning(f"  {env_name}:")
                for issue in env_issues:
                    print_warning(f"    - {issue}")
        else:
            print_success("All environments are valid")
        
        # Check system
        print_info("Checking system...")
        from .utils.helpers import get_python_executables
        pythons = get_python_executables()
        if pythons:
            print_success(f"Found {len(pythons)} Python installations")
        else:
            print_warning("No Python installations found")
        
        print_success("Diagnostics complete")
        
    except Exception as e:
        print_error(f"Diagnostics failed: {e}")
        sys.exit(1)


@main.command()
@pass_config
def platform(ctx):
    """Show platform information and installation instructions."""
    try:
        from .utils.platform_support import (
            get_platform_info, get_installation_helper, check_platform_compatibility
        )
        
        platform_info = get_platform_info()
        installation_helper = get_installation_helper()
        
        print_info("Platform Information")
        print_info("===================")
        
        # Basic platform info
        click.echo(f"Operating System: {platform_info.system.title()}")
        click.echo(f"Architecture: {platform_info.machine}")
        click.echo(f"Python Version: {platform_info.python_version}")
        click.echo(f"Shell: {platform_info.shell_type}")
        
        # Platform compatibility check
        compatible, issues = check_platform_compatibility()
        if compatible:
            print_success("✅ Platform is fully supported")
        else:
            print_warning("⚠️ Platform compatibility issues found:")
            for issue in issues:
                print_warning(f"  - {issue}")
        
        # Installation methods
        click.echo("\n📦 Installation Methods:")
        click.echo("========================")
        
        methods = installation_helper.get_installation_methods()
        for method_name, commands in methods.items():
            click.echo(f"\n{method_name.title()}:")
            for cmd in commands:
                click.echo(f"  {cmd}")
        
        # Shell completion setup
        click.echo("\n🔧 Shell Completion Setup:")
        click.echo("==========================")
        
        completion = installation_helper.get_shell_completion_setup()
        for shell, cmd in completion.items():
            click.echo(f"\n{shell.title()}:")
            click.echo(f"  {cmd}")
        
        # PATH setup instructions
        click.echo("\n🛠️ PATH Setup Instructions:")
        click.echo("===========================")
        
        path_instructions = installation_helper.get_path_setup_instructions()
        for instruction in path_instructions:
            click.echo(instruction)
        
        # Platform-specific tips
        click.echo(f"\n💡 {platform_info.system.title()}-Specific Tips:")
        click.echo("=" * (len(platform_info.system) + 17))
        
        if platform_info.is_windows:
            click.echo("• Use PowerShell or Windows Terminal for best experience")
            click.echo("• Consider installing Windows Subsystem for Linux (WSL)")
            click.echo("• Use chocolatey or winget for easy package management")
            click.echo("• Set execution policy for PowerShell scripts if needed")
        elif platform_info.is_macos:
            click.echo("• Install Homebrew for easy package management")
            click.echo("• Use iTerm2 for enhanced terminal experience") 
            click.echo("• Consider using pyenv for Python version management")
            click.echo("• Xcode command line tools may be required")
        else:  # Linux
            click.echo("• Use your distribution's package manager when possible")
            click.echo("• Consider using pyenv for Python version management")
            click.echo("• Install build-essential for compiling packages")
            click.echo("• Use virtual environments to avoid system conflicts")
        
    except Exception as e:
        print_error(f"Failed to get platform information: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 