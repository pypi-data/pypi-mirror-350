#!/bin/bash
# Script to help fix pre-commit for Windows with Microsoft Store Python

echo "Fixing pre-commit configuration for Windows..."

# Clean pre-commit cache
echo "Cleaning pre-commit cache..."
if [ -f ".venv/Scripts/pre-commit.exe" ]; then
    .venv/Scripts/pre-commit.exe clean
else
    echo "ERROR: pre-commit not found in virtual environment."
    echo "Please run: uv add --dev pre-commit"
    exit 1
fi

# Create a Windows-friendly pre-commit config
echo "Creating Windows-friendly pre-commit config..."

cat > .pre-commit-config.yaml << 'EOL'
# See https://pre-commit.com for more information
# Using local hooks to avoid virtualenv issues with Microsoft Store Python
repos:
  - repo: local
    hooks:
      - id: black
        name: black
        description: "Black: The uncompromising Python code formatter"
        entry: .venv\Scripts\black.exe
        language: system
        types: [python]
        
      - id: isort
        name: isort
        description: "isort: Sort Python imports"
        entry: .venv\Scripts\isort.exe
        language: system
        types: [python]
        
      - id: ruff
        name: ruff
        description: "Ruff: An extremely fast Python linter"
        entry: .venv\Scripts\ruff.exe check --fix
        language: system
        types: [python]
        
      - id: mypy
        name: mypy
        description: "Mypy: Optional static typing for Python"
        entry: .venv\Scripts\mypy.exe --no-strict-optional --ignore-missing-imports
        language: system
        types: [python]
EOL

# Ensure all tools are installed
echo "Installing required dev dependencies..."
uv add --dev black isort ruff mypy pre-commit

# Reinstall hooks
echo "Reinstalling pre-commit hooks..."
.venv/Scripts/pre-commit.exe install

echo ""
echo "Done! Pre-commit configuration has been fixed for Windows."
echo "Try running: .venv/Scripts/pre-commit.exe run --all-files"
