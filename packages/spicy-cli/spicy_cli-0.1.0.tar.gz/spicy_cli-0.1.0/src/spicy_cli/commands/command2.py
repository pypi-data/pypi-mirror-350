"""Command 2 implementation."""

import typer
from rich.console import Console
from rich.table import Table

from spicy_cli.commands.base import (
    format_error,
    format_info,
    format_success,
    format_warning,
    get_config,
)

app = typer.Typer(help="Command 2 related operations")
console = Console()


@app.command("process")
def process_command(
    files: list[str] = typer.Argument(..., help="Files to process"),
    output: str | None = typer.Option(None, "--output", "-o", help="Output file"),
    force: bool = typer.Option(False, "--force", "-f", help="Force processing"),
) -> None:
    """Process files with command 2."""
    format_info(f"Processing {len(files)} file(s)...")

    config = get_config()
    timeout = getattr(config, "timeout", 30)

    for file in files:
        console.print(f"Processing: [cyan]{file}[/cyan]")  # Check if file exists (mock implementation)
        if file.endswith(".invalid"):
            format_error(f"Invalid file: {file}")
            if not force:
                format_warning("Processing stopped. Use --force to continue despite errors.")
                return

    if output:
        console.print(f"Output will be saved to: [green]{output}[/green]")

    if force:
        format_warning("Force mode enabled - processing all files regardless of errors")

    success_msg = f"Processing complete! Processed {len(files)} files with timeout {timeout}s"
    format_success(success_msg)


@app.command("list")
def list_command(
    limit: int = typer.Option(10, "--limit", "-l", help="Limit the number of items"),
    show_all: bool = typer.Option(False, "--all", "-a", help="Show all details"),
) -> None:
    """List items with command 2."""
    format_info(f"Listing up to {limit} items...")

    table = Table(title="Command 2 Items")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")

    if show_all:
        table.add_column("Description")
        table.add_column("Status")

    for i in range(min(limit, 15)):
        if show_all:
            table.add_row(
                f"{i + 1}",
                f"Item {i + 1}",
                f"Description for item {i + 1}",
                "Active" if i % 3 != 0 else "Inactive",
            )
        else:
            table.add_row(f"{i + 1}", f"Item {i + 1}")

    console.print(table)
    format_success(f"Successfully listed {min(limit, 15)} items")
