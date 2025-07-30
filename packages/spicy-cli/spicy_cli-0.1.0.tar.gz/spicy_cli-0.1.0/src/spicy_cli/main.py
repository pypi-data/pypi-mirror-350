"""Main entry point for the Spicy CLI application."""

import typer
from dotenv import load_dotenv
from rich.console import Console

from spicy_cli import __version__
from spicy_cli.commands import command1, command2, config, plugin, uuid
from spicy_cli.plugins import find_plugins

# Load environment variables from .env file if present
load_dotenv()

# Create a console for rich output
console = Console()

# Create the main application
app = typer.Typer(
    name="spicy",
    help="A Python CLI with multiple commands",
    add_completion=True,
    invoke_without_command=True,
)

# Register commands
app.add_typer(command1.app, name="command1")
app.add_typer(command2.app, name="command2")
app.add_typer(config.app, name="config")
app.add_typer(plugin.app, name="plugin")
app.add_typer(uuid.app, name="uuid")

# Load and register plugins
for name, plugin_class in find_plugins().items():
    try:
        app.add_typer(plugin_class.get_typer_app(), name=name)
    except Exception as e:
        console.print(f"[red]Error loading plugin {name}: {e}[/red]")


@app.command("version")
def version_command() -> None:
    """Show the application version."""
    console.print(f"[bold green]Spicy CLI[/bold green] version: [bold]{__version__}[/bold]")


@app.callback()
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show the application version and exit."),
) -> None:
    """Spicy CLI - A Python CLI with multiple commands."""
    if version:
        console.print(f"[bold green]Spicy CLI[/bold green] version: [bold]{__version__}[/bold]")
        raise typer.Exit(0)

    # If no version flag and no command provided, show help
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


if __name__ == "__main__":
    app()
