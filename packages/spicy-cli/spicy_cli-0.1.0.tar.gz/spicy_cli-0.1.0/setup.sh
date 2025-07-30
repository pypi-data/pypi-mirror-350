#!/usr/bin/env bash
# Setup script for Spicy CLI

set -e

# Check if we have uv installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing..."
    curl -sSf https://install.python-poetry.org | python3 -
fi

# Create a virtual environment
echo "Creating virtual environment..."
uv venv .venv

# Activate the virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install the package in development mode
echo "Installing package in development mode..."
uv pip install -e '.[dev]'

# Run the tests
echo "Running tests..."
pytest

echo "Setup complete! You can now use the Spicy CLI."
echo "Try running: spicy --help"
