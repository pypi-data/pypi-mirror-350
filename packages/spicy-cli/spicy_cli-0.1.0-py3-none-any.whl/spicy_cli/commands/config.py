"""Config command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from spicy_cli.commands.base import format_error, format_info, format_success
from spicy_cli.config import SpicyConfig, get_config_path, load_config, save_config

app = typer.Typer(help="Configuration related operations")
console = Console()


@app.command("show")
def show_config(
    config_path: str | None = typer.Option(None, "--config", "-c", help="Path to a config file"),
) -> None:
    path = get_config_path() if config_path is None else Path(config_path)
    config = load_config(path)
    config = load_config(path)

    format_info(f"Configuration loaded from: {path}")

    table = Table(title="Spicy CLI Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    for field_name, field_value in config.model_dump().items():
        table.add_row(field_name, str(field_value))

    console.print(table)


@app.command("set")
def set_config(
    setting: str = typer.Argument(..., help="The setting to change"),
    value: str = typer.Argument(..., help="The new value"),
    config_path: str | None = typer.Option(None, "--config", "-c", help="Path to a config file"),
) -> None:
    path = get_config_path() if config_path is None else Path(config_path)
    config = load_config(path)
    config = load_config(path)

    if not hasattr(config, setting):
        format_error(f"Unknown setting: {setting}")
        return  # Convert value to the appropriate type
    old_value = getattr(config, setting)

    # Initialize new_value with None to help type checking
    new_value: bool | int | str | None = None

    if isinstance(old_value, bool):
        if value.lower() in ("true", "yes", "1", "on"):
            new_value = True
        elif value.lower() in ("false", "no", "0", "off"):
            new_value = False
        else:
            format_error(f"Invalid boolean value: {value}")
            return
    elif isinstance(old_value, int):
        try:
            # Convert string to int but store as int
            new_value = int(value)
        except ValueError:
            format_error(f"Invalid integer value: {value}")
            return
    else:  # For string values
        new_value = str(value)  # Update and save the config
    if isinstance(old_value, bool) and isinstance(new_value, bool):
        setattr(config, setting, new_value)
    elif isinstance(old_value, int) and isinstance(new_value, int):
        setattr(config, setting, new_value)
    elif isinstance(old_value, str) and isinstance(new_value, str):
        setattr(config, setting, new_value)
    else:
        format_error(f"Type mismatch: Cannot set {setting} to {new_value} (type {type(new_value).__name__})")
        return
    save_config(config, path)

    format_success(f"Updated {setting} from {old_value} to {new_value}")
    format_info(f"Configuration saved to: {path}")


@app.command("reset")
def reset_config(
    config_path: str | None = typer.Option(None, "--config", "-c", help="Path to a config file"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
) -> None:
    """Reset the configuration to defaults."""
    if not confirm:
        should_reset = typer.confirm("Are you sure you want to reset the configuration?")
        if not should_reset:
            format_info("Reset cancelled")
            return
    path = get_config_path() if config_path is None else Path(config_path)
    save_config(SpicyConfig(), path)

    format_success("Configuration reset to defaults")
    format_info(f"Configuration saved to: {path}")
