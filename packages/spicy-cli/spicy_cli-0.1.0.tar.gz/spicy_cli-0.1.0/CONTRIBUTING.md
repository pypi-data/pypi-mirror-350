# Developer Guide

This document provides information for developers working on the Spicy CLI project.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- [uv](https://github.com/astral-sh/uv) for Python dependency management

### Setup Process

1. Clone the repository:
   ```bash
   git clone https://github.com/darkflib/spicy-cli.git
   cd spicy-cli
   ```

2. Create and activate a virtual environment:
   ```bash
   # Using uv
   uv venv
   
   # On Linux/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

## Pre-commit Configuration

This project uses pre-commit to maintain code quality. Our setup uses local hooks that directly reference the executables in the virtual environment, which helps avoid issues with Microsoft Store Python installations.

### Windows-specific Notes

If you're using Windows with Python installed from the Microsoft Store, the standard pre-commit setup might fail due to issues with creating sub-virtualenvs. Our configuration avoids this problem by using local hooks.

If you encounter errors, try running:

```bash
# Clean pre-commit cache
.venv\Scripts\pre-commit.exe clean

# Re-install the hooks
.venv\Scripts\pre-commit.exe install
```

### Troubleshooting Pre-commit Issues

If you encounter pre-commit errors, ensure:

1. All required packages are installed in your virtual environment:
   ```bash
   uv add --dev black isort ruff mypy
   ```

2. Paths in `.pre-commit-config.yaml` match your system (Windows users need `.exe` extensions)

3. For persistent issues, try the Windows helper script:
   ```bash
   ./scripts/fix_precommit_windows.bat
   ```

## Testing

Run tests with pytest:

```bash
uv run pytest
```

## Code Style

This project follows:
- Black for code formatting
- isort for import sorting
- Ruff for linting
- mypy for type checking

These are enforced via pre-commit hooks.
