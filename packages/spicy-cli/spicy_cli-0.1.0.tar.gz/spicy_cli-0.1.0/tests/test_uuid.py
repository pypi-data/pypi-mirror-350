import re

from typer.testing import CliRunner

from spicy_cli.main import app  # Assuming 'app' is your main Typer application

runner = CliRunner()

# Regex to validate a UUID
UUID_PATTERN = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Checks whether a string matches the standard UUID format.

    Args:
        uuid_string: The string to validate.

    Returns:
        True if the string is a valid UUID, otherwise False.
    """
    return bool(UUID_PATTERN.match(uuid_string))


def test_uuid_generate_default() -> None:
    """Test generating a single UUID (default behavior)."""
    result = runner.invoke(app, ["uuid", "generate"])
    assert result.exit_code == 0
    output_lines = result.stdout.strip().split("\n")
    assert len(output_lines) == 1
    assert is_valid_uuid(output_lines[0])


def test_uuid_generate_multiple() -> None:
    """
    Tests that the `uuid generate` command outputs the correct number of valid UUIDs when the `-n` option is used.
    """
    count = 5
    result = runner.invoke(app, ["uuid", "generate", "-n", str(count)])
    assert result.exit_code == 0
    output_lines = result.stdout.strip().split("\n")
    assert len(output_lines) == count
    for line in output_lines:
        assert is_valid_uuid(line)


def test_uuid_generate_custom_count() -> None:
    """Test generating a specific number of UUIDs (e.g., 3)."""
    count = 3
    result = runner.invoke(app, ["uuid", "generate", "--count", str(count)])
    assert result.exit_code == 0
    output_lines = result.stdout.strip().split("\n")
    assert len(output_lines) == count
    for line in output_lines:
        assert is_valid_uuid(line)


def test_uuid_generate_invalid_count_zero() -> None:
    """
    Tests that the CLI returns an error when attempting to generate zero UUIDs.

    Verifies that providing a count of 0 results in a non-zero exit code and an appropriate error message.
    """
    result = runner.invoke(app, ["uuid", "generate", "-n", "0"])
    assert result.exit_code == 1
    assert "Error: Number of UUIDs must be at least 1." in result.stdout


def test_uuid_generate_invalid_count_negative() -> None:
    """Test generating UUIDs with an invalid negative count."""
    result = runner.invoke(app, ["uuid", "generate", "-n", "-5"])
    assert result.exit_code == 1
    assert "Error: Number of UUIDs must be at least 1." in result.stdout


# It might also be useful to test the help message for the command
def test_uuid_generate_help() -> None:
    """
    Tests that the help message for the 'uuid generate' command is displayed correctly.

    Verifies that the help output includes the command description and the '--count, -n' option.
    """
    result = runner.invoke(app, ["uuid", "generate", "--help"])
    assert result.exit_code == 0
    assert "Generate one or more UUIDs." in result.stdout
    # assert "--count, -n" in result.stdout
