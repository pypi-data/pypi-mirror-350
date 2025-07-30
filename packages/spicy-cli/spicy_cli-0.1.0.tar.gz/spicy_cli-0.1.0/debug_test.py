#!/usr/bin/env python3
"""Debug the version flag issue."""

from typer.testing import CliRunner

from spicy_cli.main import app


def main() -> None:
    """Run a CLI test to debug the version flag."""
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    # Using logger would be better in production code
    # These prints are for debugging purposes only
    print(f"Exit code: {result.exit_code}")  # noqa: T201
    print(f"stdout: {result.stdout}")  # noqa: T201
    print(f"stderr: {result.stderr}")  # noqa: T201
    print(f"exception: {result.exception}")  # noqa: T201


if __name__ == "__main__":
    main()
