@echo off
echo Fixing pre-commit configuration for Windows...

:: Clean pre-commit cache
echo Cleaning pre-commit cache...
if exist .venv\Scripts\pre-commit.exe (
    .venv\Scripts\pre-commit.exe clean
) else (
    echo ERROR: pre-commit not found in virtual environment.
    echo Please run: uv add --dev pre-commit
    exit /b 1
)

:: Create a Windows-friendly pre-commit config
echo Creating Windows-friendly pre-commit config...

(
echo # See https://pre-commit.com for more information
echo # Using local hooks to avoid virtualenv issues with Microsoft Store Python
echo repos:
echo   - repo: local
echo     hooks:
echo       - id: black
echo         name: black
echo         description: "Black: The uncompromising Python code formatter"
echo         entry: .venv\Scripts\black.exe
echo         language: system
echo         types: [python]
echo         
echo       - id: isort
echo         name: isort
echo         description: "isort: Sort Python imports"
echo         entry: .venv\Scripts\isort.exe
echo         language: system
echo         types: [python]
echo         
echo       - id: ruff
echo         name: ruff
echo         description: "Ruff: An extremely fast Python linter"
echo         entry: .venv\Scripts\ruff.exe check --fix
echo         language: system
echo         types: [python]
echo         
echo       - id: mypy
echo         name: mypy
echo         description: "Mypy: Optional static typing for Python"
echo         entry: .venv\Scripts\mypy.exe --no-strict-optional --ignore-missing-imports
echo         language: system
echo         types: [python]
) > .pre-commit-config.yaml

:: Ensure all tools are installed
echo Installing required dev dependencies...
uv add --dev black isort ruff mypy pre-commit

:: Reinstall hooks
echo Reinstalling pre-commit hooks...
.venv\Scripts\pre-commit.exe install

echo.
echo Done! Pre-commit configuration has been fixed for Windows.
echo Try running: .venv\Scripts\pre-commit.exe run --all-files
