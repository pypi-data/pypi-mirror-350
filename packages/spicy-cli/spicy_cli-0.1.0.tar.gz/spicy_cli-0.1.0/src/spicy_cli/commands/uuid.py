import uuid as uuid_module

import typer
from rich.console import Console

app = typer.Typer(help="Generate UUIDs.")
console = Console()


@app.command("generate", help="Generate one or more UUIDs.")
def generate_uuid(count: int = typer.Option(1, "--count", "-n", help="Number of UUIDs to generate.")) -> None:
    """
    Generate one or more UUIDs.

    # ...
    Args:
        --count, -n: The number of UUIDs to generate. Must be at least 1.

    Raises:
        typer.Exit: If count is less than 1.
    """
    if count < 1:
        console.print("[bold red]Error: Number of UUIDs must be at least 1.[/bold red]")
        raise typer.Exit(code=1)
    for _ in range(count):
        console.print(str(uuid_module.uuid4()))
