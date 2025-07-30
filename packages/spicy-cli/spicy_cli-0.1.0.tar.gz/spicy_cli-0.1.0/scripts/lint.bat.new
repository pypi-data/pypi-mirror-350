@echo off
REM Run all linting and formatting tools

REM Get the directory of this script and the project root
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."

REM Change to the project root directory
cd /d "%ROOT_DIR%"

REM Check if virtual environment exists, if not create one
set "VENV_DIR=.venv"
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    where uv >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo uv is not installed. Please install it.
        exit /b 1
    )
    
    call uv venv "%VENV_DIR%"
    
    REM Install dev dependencies
    echo Installing development dependencies...
    call "%VENV_DIR%\Scripts\activate.bat"
    call uv pip install -e .[dev]
)

REM Activate the virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

REM Debug information
echo Using Python at:
where python
echo Python version:
python --version
echo Virtual environment path: %VIRTUAL_ENV%

REM Function to ensure development tools are installed
:ensure_tool_installed
where %1 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %1 not found. Installing development dependencies...
    where uv >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo Using uv to install dependencies...
        call uv pip install -e .[dev]
    ) else (
        echo uv not found. Falling back to pip...
        python -m ensurepip --upgrade
        if %ERRORLEVEL% neq 0 (
            echo Failed to ensure pip is installed.
            echo You might need to manually install development dependencies with:
            echo   cd %ROOT_DIR% ^&^& uv pip install -e .[dev]
            exit /b 1
        )
        python -m pip install -e .[dev]
    )
    
    REM Verify installation was successful
    where %1 >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Failed to install %1. Please check your environment.
        exit /b 1
    )
)
goto :eof

REM Now run the linting tools
echo Running black...
call :ensure_tool_installed black
black .

echo Running isort...
call :ensure_tool_installed isort
isort .

echo Running mypy...
call :ensure_tool_installed mypy
mypy .

echo Running ruff...
call :ensure_tool_installed ruff
ruff check .

echo Running pylint...
call :ensure_tool_installed pylint
pylint src\ tests\

echo All checks passed!
