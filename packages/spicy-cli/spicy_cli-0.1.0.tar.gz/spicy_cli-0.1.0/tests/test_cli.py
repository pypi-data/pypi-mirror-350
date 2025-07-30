"""Tests for the Spicy CLI application."""

from pathlib import Path
from tempfile import NamedTemporaryFile

from typer.testing import CliRunner

from spicy_cli import __version__
from spicy_cli.config import SpicyConfig, save_config
from spicy_cli.main import app

runner = CliRunner()


def test_app_version() -> None:
    """Test that the version flag works correctly."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_version_command() -> None:
    """Test that the version command works correctly."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_command1_run() -> None:
    """Test that command1 run works correctly."""
    result = runner.invoke(app, ["command1", "run", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout


def test_command1_status() -> None:
    """Test that command1 status works correctly."""
    result = runner.invoke(app, ["command1", "status"])
    assert result.exit_code == 0
    assert "Status" in result.stdout


def test_command2_list() -> None:
    """Test that command2 list works correctly."""
    result = runner.invoke(app, ["command2", "list", "--limit", "5"])
    assert result.exit_code == 0
    assert "Command 2 Items" in result.stdout


def test_config_show() -> None:
    """Test that config show works correctly."""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "Configuration" in result.stdout


def test_config_set() -> None:
    """Test that config set works correctly."""
    with NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    try:
        # Create a default config
        config = SpicyConfig()
        save_config(config, temp_path)

        # Test setting a value
        result = runner.invoke(app, ["config", "set", "timeout", "60", "--config", str(temp_path)])  # noqa: E501
        assert result.exit_code == 0
        assert "Updated timeout" in result.stdout

        # Test showing the updated config
        result = runner.invoke(app, ["config", "show", "--config", str(temp_path)])
        assert result.exit_code == 0
        assert "timeout" in result.stdout
        assert "60" in result.stdout
    finally:
        # Clean up the temporary file
        if temp_path.exists():
            temp_path.unlink()
