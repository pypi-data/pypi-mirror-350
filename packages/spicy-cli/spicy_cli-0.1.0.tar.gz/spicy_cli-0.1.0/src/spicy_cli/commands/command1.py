"""Command 1 implementation."""

import typer
from rich.console import Console

from spicy_cli.commands.base import format_info, format_success

app = typer.Typer(help="Command 1 related operations")
console = Console()


@app.command("run")
def run_command(
    name: str = typer.Argument(..., help="Name to greet"),
    count: int = typer.Option(1, "--count", "-c", help="Number of greetings"),
    formal: bool = typer.Option(False, "--formal", "-f", help="Use formal greeting"),
) -> None:
    """Run command 1 with the given options."""
    greeting = "Hello" if not formal else "Good day"

    for _ in range(count):
        console.print(f"[bold green]{greeting}, {name}![/bold green]")

    format_success(f"Greeted {name} {count} time(s)")


@app.command("status")
def status_command(verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose output")) -> None:
    """Show the status of command 1."""
    if verbose:
        format_info("Retrieving detailed status information...")
        console.print("[bold blue]Command 1 Status:[/bold blue] [green]All systems operational[/green]")
        console.print("[dim]Details: Running version 1.0, no issues detected[/dim]")
    else:
        format_info("Status check completed")
        console.print("[bold blue]Command 1 Status:[/bold blue] [green]OK[/green]")
