"""Plugin system for the Spicy CLI."""

import importlib
import importlib.util
import os
import sys
from pathlib import Path

import typer
from rich.console import Console

from spicy_cli.commands.base import format_error

console = Console()


class PluginBase:
    """Base class for Spicy CLI plugins."""

    name: str = "plugin"
    help: str = "A Spicy CLI plugin"

    @classmethod
    def get_typer_app(cls) -> typer.Typer:
        """Get the Typer app for this plugin.

        Returns:
            A Typer app for this plugin
        """
        raise NotImplementedError("Plugins must implement get_typer_app()")


def get_plugin_dirs() -> list[Path]:
    """Get the directories to search for plugins.

    Returns:
        List of directories to search for plugins
    """
    plugin_dirs = []  # User plugins directory
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        user_plugin_dir = Path(xdg_data_home) / "spicy-cli" / "plugins"
    else:
        user_plugin_dir = Path.home() / ".local" / "share" / "spicy-cli" / "plugins"

    if user_plugin_dir.exists():
        plugin_dirs.append(user_plugin_dir)

    # System plugins directory on Unix-like systems
    sys_plugin_dir = Path("/usr/share/spicy-cli/plugins")
    if sys_plugin_dir.exists():
        plugin_dirs.append(sys_plugin_dir)

    # Add any directories from SPICY_PLUGIN_PATH
    plugin_path = os.environ.get("SPICY_PLUGIN_PATH", "")
    if plugin_path:
        for path_str in plugin_path.split(os.pathsep):
            path = Path(path_str.strip())
            if path.exists():
                plugin_dirs.append(path)

    return plugin_dirs


def find_plugins() -> dict[str, type[PluginBase]]:
    """Find and load all available plugins.

    Returns:
        Dictionary mapping plugin names to plugin classes
    """
    plugins: dict[str, type[PluginBase]] = {}

    for plugin_dir in get_plugin_dirs():
        for plugin_file in plugin_dir.glob("*.py"):
            try:
                module_name = f"spicy_cli_plugin_{plugin_file.stem}"
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                if spec is None or spec.loader is None:
                    continue

                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # Look for plugin classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, PluginBase) and attr is not PluginBase:
                        plugins[attr.name] = attr

            except Exception as e:
                format_error(f"Failed to load plugin {plugin_file}: {e}")

    return plugins


def load_plugin(plugin_path: Path) -> tuple[str, type[PluginBase]] | None:
    """Load a plugin from a file.

    Args:
        plugin_path: Path to the plugin file

    Returns:
        Tuple of (plugin_name, plugin_class) if successful, None otherwise
    """
    try:
        module_name = f"spicy_cli_plugin_{plugin_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        if spec is None or spec.loader is None:
            error_msg = f"Failed to load plugin {plugin_path}: Invalid module specification"
            format_error(error_msg)
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Look for plugin classes
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, PluginBase) and attr is not PluginBase:
                return attr.name, attr

        format_error(f"No plugin class found in {plugin_path}")
        return None

    except Exception as e:
        format_error(f"Failed to load plugin {plugin_path}: {e}")
        return None
