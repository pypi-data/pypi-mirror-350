#!/usr/bin/env bash
# Run all linting and formatting tools

set -e

# Directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Project root directory
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project root directory
cd "$ROOT_DIR"

# Check if virtual environment exists, if not create one
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    if command -v uv &> /dev/null; then
        uv venv "$VENV_DIR"
    else
        echo "uv is not installed. Please install it with:"
        echo "curl -sSf https://install.python-poetry.org | python3 -"
        exit 1
    fi
    
    # Install dev dependencies
    echo "Installing development dependencies..."
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    elif [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate"
    elif [ -f "$VENV_DIR/Scripts/activate.bat" ]; then
        # If we're running in Git Bash on Windows, we need to use MSYS path conversion
        ACTIVATE_PATH=$(cygpath -u "$VENV_DIR/Scripts/activate")
        source "$ACTIVATE_PATH"
    else
        echo "Could not find activation script in $VENV_DIR"
        exit 1
    fi
    
    # Install using uv if available
    if command -v uv &> /dev/null; then
        uv pip install -e '.[dev]'
    else
        python -m pip install -e '.[dev]'
    fi
fi

# Activate the virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
elif [ -f "$VENV_DIR/Scripts/activate.bat" ]; then
    # If we're running in Git Bash on Windows, we need to use MSYS path conversion
    # to properly source the activate script
    ACTIVATE_PATH=$(cygpath -u "$VENV_DIR/Scripts/activate")
    source "$ACTIVATE_PATH"
else
    echo "Could not find activation script in $VENV_DIR"
    exit 1
fi

# Debug information
echo "Using Python at: $(which python || echo 'python not found')"
echo "Python version: $(python --version 2>&1 || echo 'python not found')"
echo "Virtual environment path: $VIRTUAL_ENV"

# Function to ensure development tools are installed
ensure_tool_installed() {
    local tool_name="$1"
    if ! command -v "$tool_name" &> /dev/null; then
        echo "$tool_name not found. Installing development dependencies..."
        # Try using uv for package installation
        if command -v uv &> /dev/null; then
            echo "Using uv to install dependencies..."
            uv pip install -e '.[dev]'
        else
            # Fallback to pip if uv is not available
            echo "uv not found. Falling back to pip..."
            # Ensure pip is available in the virtual environment
            python -m ensurepip --upgrade || {
                echo "Failed to ensure pip is installed. Trying to download pip..."
                curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
                python get-pip.py
                rm get-pip.py
            }
            python -m pip install -e '.[dev]'
        fi
        
        # Verify installation was successful
        if ! command -v "$tool_name" &> /dev/null; then
            echo "Failed to install $tool_name. Please check your environment."
            echo "You might need to manually install development dependencies with:"
            echo "  cd $ROOT_DIR && uv pip install -e '.[dev]'"
            exit 1
        fi
    fi
}

# Now run the linting tools
echo "Running black..."
ensure_tool_installed "black"
black .

echo "Running isort..."
ensure_tool_installed "isort"
isort .

echo "Running mypy..."
ensure_tool_installed "mypy"
mypy .

echo "Running ruff..."
ensure_tool_installed "ruff"
ruff check .

echo "Running pylint..."
ensure_tool_installed "pylint"
pylint src/ tests/

echo "All checks passed!"
