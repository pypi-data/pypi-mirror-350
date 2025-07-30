"""Base utilities for commands."""

from pathlib import Path

from rich.console import Console

from spicy_cli.config import SpicyConfig, load_config

console = Console()


def format_success(message: str) -> None:
    """Format and print a success message."""
    console.print(f"[bold green]SUCCESS:[/bold green] {message}")


def format_error(message: str) -> None:
    """Format and print an error message."""
    console.print(f"[bold red]ERROR:[/bold red] {message}")


def format_warning(message: str) -> None:
    """Format and print a warning message."""
    console.print(f"[bold yellow]WARNING:[/bold yellow] {message}")


def format_info(message: str) -> None:
    """Format and print an info message."""
    console.print(f"[bold blue]INFO:[/bold blue] {message}")


def get_config(config_path: Path | None = None) -> SpicyConfig:
    """Get configuration from a file or environment variables.

    Args:
        config_path: Optional path to a config file

    Returns:
        SpicyConfig object
    """
    return load_config(config_path)
