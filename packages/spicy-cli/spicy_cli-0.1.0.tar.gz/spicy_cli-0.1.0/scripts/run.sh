#!/usr/bin/env bash
# Development tools for Spicy CLI

set -e

# Directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Project root directory
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project root directory
cd "$ROOT_DIR"

# Check if virtual environment exists, if not create one
ensure_venv() {
    VENV_DIR=".venv"
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        if command -v uv &> /dev/null; then
            uv venv "$VENV_DIR"
        else
            echo "uv is not installed. Please install it with:"
            echo "curl -sSf https://install.uv.tools | sh"
            exit 1
        fi
        
        # Install dev dependencies
        echo "Installing development dependencies..."
        if [ -f "$VENV_DIR/bin/activate" ]; then
            source "$VENV_DIR/bin/activate"
        elif [ -f "$VENV_DIR/Scripts/activate" ]; then
            source "$VENV_DIR/Scripts/activate"
        else
            echo "Could not find activation script in $VENV_DIR"
            exit 1
        fi
        
        uv pip install -e '.[dev]'
    fi

    # Activate the virtual environment
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    elif [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate"
    else
        echo "Could not find activation script in $VENV_DIR"
        exit 1
    fi
}

# Show help
show_help() {
    echo "Usage: $0 COMMAND"
    echo ""
    echo "Commands:"
    echo "  lint        Run all linting tools"
    echo "  format      Run formatting tools (black, isort)"
    echo "  test        Run pytest with coverage"
    echo "  clean       Clean build artifacts"
    echo "  build       Build the package"
    echo "  install     Install the package in development mode"
    echo "  run         Run the CLI (e.g. './run.sh run --help')"
    echo "  help        Show this help message"
    echo ""
}

# Run linting
run_lint() {
    ensure_venv
    
    echo "Running black..."
    black .

    echo "Running isort..."
    isort .

    echo "Running mypy..."
    mypy .

    echo "Running ruff..."
    ruff check .

    echo "Running pylint..."
    pylint src/ tests/

    echo "All checks passed!"
}

# Run formatting only
run_format() {
    ensure_venv
    
    echo "Running black..."
    black .

    echo "Running isort..."
    isort .

    echo "Format complete!"
}

# Run tests
run_tests() {
    ensure_venv
    
    echo "Running pytest with coverage..."
    pytest
}

# Clean build artifacts
run_clean() {
    echo "Cleaning build artifacts..."
    rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    
    echo "Clean complete!"
}

# Build the package
run_build() {
    ensure_venv
    
    echo "Building package..."
    python -m build
    
    echo "Build complete!"
}

# Install the package in development mode
run_install() {
    ensure_venv
    
    echo "Installing package in development mode..."
    uv pip install -e .
    
    echo "Installation complete!"
}

# Run the CLI
run_cli() {
    ensure_venv
    
    if [ $# -eq 0 ]; then
        python -m spicy_cli.main --help
    else
        python -m spicy_cli.main "$@"
    fi
}

# Parse command
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

COMMAND="$1"
shift

case "$COMMAND" in
    lint)
        run_lint
        ;;
    format)
        run_format
        ;;
    test)
        run_tests
        ;;
    clean)
        run_clean
        ;;
    build)
        run_build
        ;;
    install)
        run_install
        ;;
    run)
        run_cli "$@"
        ;;
    help)
        show_help
        ;;
    *)
        echo "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac
