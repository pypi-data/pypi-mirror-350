#!/usr/bin/env python3
"""
EnvFy Output Utilities

Beautiful console output using Rich for colorful and attractive displays.
"""

import sys
from typing import Any, Optional, Union, Dict, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.columns import Columns
from rich.align import Align
from rich import box
from rich.emoji import Emoji

# Global console instance
console = Console()


def print_success(message: str, details: Optional[str] = None) -> None:
    """Print a success message with green checkmark."""
    text = Text()
    text.append("✅ ", style="green")
    text.append(message, style="green bold")
    console.print(text)
    
    if details:
        console.print(f"   {details}", style="dim")


def print_error(message: str, details: Optional[str] = None) -> None:
    """Print an error message with red cross."""
    text = Text()
    text.append("❌ ", style="red")
    text.append(message, style="red bold")
    console.print(text)
    
    if details:
        console.print(f"   {details}", style="dim red")


def print_warning(message: str, details: Optional[str] = None) -> None:
    """Print a warning message with yellow warning sign."""
    text = Text()
    text.append("⚠️  ", style="yellow")
    text.append(message, style="yellow bold")
    console.print(text)
    
    if details:
        console.print(f"   {details}", style="dim yellow")


def print_info(message: str, details: Optional[str] = None) -> None:
    """Print an info message with blue info icon."""
    text = Text()
    text.append("ℹ️  ", style="blue")
    text.append(message, style="blue bold")
    console.print(text)
    
    if details:
        console.print(f"   {details}", style="dim blue")


def print_step(step: int, total: int, message: str) -> None:
    """Print a step in a process."""
    text = Text()
    text.append(f"[{step}/{total}] ", style="cyan bold")
    text.append(message, style="white")
    console.print(text)


def create_progress() -> Progress:
    """Create a beautiful progress bar."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    )


def create_table(title: str, headers: List[str]) -> Table:
    """Create a beautiful table with the given title and headers."""
    table = Table(
        title=title,
        box=box.ROUNDED,
        title_style="bold magenta",
        header_style="bold cyan",
        border_style="blue",
    )
    
    for header in headers:
        table.add_column(header, style="white")
    
    return table


def create_panel(content: str, title: str, style: str = "blue") -> Panel:
    """Create a beautiful panel with border."""
    return Panel(
        content,
        title=title,
        border_style=style,
        title_align="left",
        box=box.ROUNDED,
    )


def create_environment_tree(environments: Dict[str, Dict[str, Any]]) -> Tree:
    """Create a tree view of environments."""
    tree = Tree("🐍 EnvFy Environments", style="bold blue")
    
    for env_name, env_info in environments.items():
        env_node = tree.add(f"📁 {env_name}", style="green bold")
        
        # Add Python version
        if "python_version" in env_info:
            env_node.add(f"🐍 Python {env_info['python_version']}", style="yellow")
        
        # Add packages count
        if "packages" in env_info:
            count = len(env_info["packages"])
            env_node.add(f"📦 {count} packages", style="blue")
        
        # Add status
        if "status" in env_info:
            status_style = "green" if env_info["status"] == "active" else "dim"
            env_node.add(f"🔘 {env_info['status']}", style=status_style)
    
    return tree


def print_environment_info(env_name: str, env_info: Dict[str, Any]) -> None:
    """Print detailed environment information."""
    # Create main panel
    content_lines = []
    
    # Basic info
    content_lines.append(f"Name: {env_name}")
    if "python_version" in env_info:
        content_lines.append(f"Python: {env_info['python_version']}")
    if "path" in env_info:
        content_lines.append(f"Path: {env_info['path']}")
    if "created" in env_info:
        content_lines.append(f"Created: {env_info['created']}")
    
    panel = create_panel(
        "\n".join(content_lines),
        f"🐍 Environment: {env_name}",
        "green"
    )
    console.print(panel)
    
    # Packages table
    if "packages" in env_info and env_info["packages"]:
        table = create_table("📦 Installed Packages", ["Package", "Version"])
        for pkg_name, pkg_version in env_info["packages"].items():
            table.add_row(pkg_name, pkg_version)
        console.print(table)


def print_package_list(packages: List[Dict[str, str]]) -> None:
    """Print a list of packages in a table."""
    if not packages:
        print_info("No packages installed")
        return
    
    table = create_table("📦 Installed Packages", ["Package", "Version", "Location"])
    
    for pkg in packages:
        table.add_row(
            pkg.get("name", "Unknown"),
            pkg.get("version", "Unknown"),
            pkg.get("location", "Unknown")
        )
    
    console.print(table)


def print_python_versions(versions: List[Dict[str, str]]) -> None:
    """Print available Python versions."""
    if not versions:
        print_warning("No Python versions found")
        return
    
    table = create_table("🐍 Available Python Versions", ["Version", "Executable", "Status"])
    
    for version in versions:
        status_style = "green" if version.get("available", False) else "red"
        status = "✅ Available" if version.get("available", False) else "❌ Not Found"
        
        table.add_row(
            version.get("version", "Unknown"),
            version.get("executable", "Unknown"),
            status,
            style=status_style if not version.get("available", False) else None
        )
    
    console.print(table)


def print_banner() -> None:
    """Print the EnvFy banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ███████╗███╗   ██╗██╗   ██╗███████╗██╗   ██╗               ║
║    ██╔════╝████╗  ██║██║   ██║██╔════╝╚██╗ ██╔╝               ║
║    █████╗  ██╔██╗ ██║██║   ██║█████╗   ╚████╔╝                ║
║    ██╔══╝  ██║╚██╗██║╚██╗ ██╔╝██╔══╝    ╚██╔╝                 ║
║    ███████╗██║ ╚████║ ╚████╔╝ ██║        ██║                  ║
║    ╚══════╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝        ╚═╝                  ║
║                                                               ║
║        Fast, Precise Virtual Environment Management           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold blue")


def confirm_action(message: str, default: bool = False) -> bool:
    """Ask for user confirmation."""
    return Confirm.ask(message, default=default, console=console)


def prompt_input(message: str, default: Optional[str] = None) -> str:
    """Prompt for user input."""
    return Prompt.ask(message, default=default, console=console)


def print_command_help(command: str, description: str, examples: List[str]) -> None:
    """Print help for a specific command."""
    # Command header
    header = Text()
    header.append("Command: ", style="bold blue")
    header.append(command, style="bold green")
    console.print(header)
    console.print()
    
    # Description
    console.print(f"Description: {description}", style="white")
    console.print()
    
    # Examples
    if examples:
        console.print("Examples:", style="bold yellow")
        for example in examples:
            console.print(f"  $ {example}", style="dim cyan")
        console.print()


def print_loading(message: str) -> None:
    """Print a loading message with spinner."""
    with console.status(f"[bold blue]{message}..."):
        pass


def clear_screen() -> None:
    """Clear the console screen."""
    console.clear()


def print_separator(char: str = "─", length: int = 60, style: str = "blue") -> None:
    """Print a separator line."""
    console.print(char * length, style=style)


def print_centered(text: str, style: str = "bold") -> None:
    """Print centered text."""
    console.print(Align.center(text, style=style))


def print_columns(items: List[str], column_count: int = 3) -> None:
    """Print items in columns."""
    renderables = [Panel(item, expand=True) for item in items]
    console.print(Columns(renderables, equal=True, expand=True)) 