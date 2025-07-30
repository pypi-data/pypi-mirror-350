"""Plugin command implementation."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from spicy_cli.commands.base import format_error, format_info, format_success
from spicy_cli.plugins import find_plugins, get_plugin_dirs, load_plugin

app = typer.Typer(help="Plugin management")
console = Console()


@app.command("list")
def list_plugins() -> None:
    """List available plugins."""
    format_info("Searching for plugins...")

    plugins = find_plugins()

    if not plugins:
        console.print("[yellow]No plugins found[/yellow]")
        console.print("\nPlugin directories searched:")
        for plugin_dir in get_plugin_dirs():
            console.print(f"- {plugin_dir}")
        return

    table = Table(title="Available Plugins")
    table.add_column("Name", style="green")
    table.add_column("Description", style="cyan")

    for name, plugin_class in plugins.items():
        table.add_row(name, plugin_class.help)

    console.print(table)
    format_success(f"Found {len(plugins)} plugin(s)")


@app.command("install")
def install_plugin(
    plugin_file: Path = typer.Argument(..., help="Path to the plugin file"),
    user: bool = typer.Option(True, "--user/--system", help="Install for the current user or system-wide"),
) -> None:
    """Install a plugin from a file."""
    if not plugin_file.exists():
        format_error(f"Plugin file not found: {plugin_file}")
        return  # Load the plugin to validate it
    plugin_info = load_plugin(plugin_file)
    if plugin_info is None:
        return

    plugin_name, _ = plugin_info  # plugin_class not used here

    # Determine the installation directory
    if user:
        install_dir = Path.home() / ".local" / "share" / "spicy-cli" / "plugins"
    else:
        # This will usually require root/admin permissions
        install_dir = Path("/usr/share/spicy-cli/plugins")

    install_dir.mkdir(parents=True, exist_ok=True)

    # Copy the plugin file
    dest_file = install_dir / plugin_file.name

    try:
        with open(plugin_file, "rb") as src, open(dest_file, "wb") as dst:
            dst.write(src.read())

        format_success(f"Installed plugin {plugin_name} to {dest_file}")
    except Exception as e:
        format_error(f"Failed to install plugin: {e}")


@app.command("uninstall")
def uninstall_plugin(plugin_name: str = typer.Argument(..., help="Name of the plugin to uninstall")) -> None:
    """Uninstall a plugin."""
    format_info(f"Searching for plugin {plugin_name}...")

    plugins = find_plugins()
    if plugin_name not in plugins:
        format_error(f"Plugin not found: {plugin_name}")
        return

    found = False

    # Find the plugin file and remove it
    for plugin_dir in get_plugin_dirs():
        for plugin_file in plugin_dir.glob("*.py"):
            try:
                plugin_info = load_plugin(plugin_file)
                if plugin_info is not None and plugin_info[0] == plugin_name:
                    plugin_file.unlink()
                    format_success(f"Uninstalled plugin {plugin_name} from {plugin_file}")
                    found = True
            except Exception as e:
                format_error(f"Error checking plugin {plugin_file}: {e}")

    if not found:
        format_error(f"Failed to locate plugin file for {plugin_name}")


@app.command("create")
def create_plugin(
    name: str = typer.Argument(..., help="Name of the plugin"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output file path"),
) -> None:
    """Create a new plugin template."""
    if output is None:
        output = Path(f"{name.lower().replace(' ', '_')}_plugin.py")

    template = f'''"""Spicy CLI plugin: {name}"""

import typer
from rich.console import Console
from spicy_cli.plugins import PluginBase
from spicy_cli.commands.base import format_success, format_info

class {name.title().replace(" ", "")}Plugin(PluginBase):
    """Plugin for {name}."""

    name = "{name.lower().replace(" ", "-")}"
    help = "A plugin for {name}"

    @classmethod
    def get_typer_app(cls):
        """Get the Typer app for this plugin."""
        app = typer.Typer(help=cls.help)
        console = Console()

        @app.command("run")
        def run_command(
            param: str = typer.Argument(..., help="A parameter"),
            flag: bool = typer.Option(False, "--flag", "-f", help="A flag"),
        ):
            """Run the {name} plugin."""
            console.print(f"[green]Running {name} plugin with param: [bold]{{param}}[/bold][/green]")

            if flag:
                console.print("[yellow]Flag is enabled[/yellow]")

            format_success("Plugin command completed")

        return app

# This is required for the plugin to be loaded correctly
plugin_class = {name.title().replace(" ", "")}Plugin
'''

    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(template)

        format_success(f"Created plugin template at {output}")
        console.print(f"\nTo use this plugin, install it with:\n\n[cyan]spicy plugin install {output}[/cyan]")
    except Exception as e:
        format_error(f"Failed to create plugin template: {e}")
