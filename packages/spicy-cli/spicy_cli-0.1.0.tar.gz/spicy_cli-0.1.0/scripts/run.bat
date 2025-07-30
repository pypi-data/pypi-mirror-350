@echo off
REM Development tools for Spicy CLI

REM Get the directory of this script and the project root
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."

REM Change to the project root directory
cd /d "%ROOT_DIR%"

REM Check if virtual environment exists, if not create one
:ensure_venv
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
goto :end_ensure_venv
:end_ensure_venv

REM Show help
:show_help
echo Usage: %0 COMMAND
echo.
echo Commands:
echo   lint        Run all linting tools
echo   format      Run formatting tools (black, isort)
echo   test        Run pytest with coverage
echo   clean       Clean build artifacts
echo   build       Build the package
echo   install     Install the package in development mode
echo   run         Run the CLI (e.g. 'run.bat run --help')
echo   help        Show this help message
echo.
goto :eof

REM Run linting
:run_lint
call :ensure_venv
    
echo Running black...
black .

echo Running isort...
isort .

echo Running mypy...
mypy .

echo Running ruff...
ruff check .

echo Running pylint...
pylint src\ tests\

echo All checks passed!
goto :eof

REM Run formatting only
:run_format
call :ensure_venv
    
echo Running black...
black .

echo Running isort...
isort .

echo Format complete!
goto :eof

REM Run tests
:run_tests
call :ensure_venv
    
echo Running pytest with coverage...
pytest
goto :eof

REM Clean build artifacts
:run_clean
echo Cleaning build artifacts...
if exist build\ rd /s /q build\
if exist dist\ rd /s /q dist\
if exist *.egg-info\ rd /s /q *.egg-info\
if exist .coverage del /f .coverage
if exist htmlcov\ rd /s /q htmlcov\
if exist .pytest_cache\ rd /s /q .pytest_cache\
if exist .mypy_cache\ rd /s /q .mypy_cache\
if exist .ruff_cache\ rd /s /q .ruff_cache\

REM Clean __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    
echo Clean complete!
goto :eof

REM Build the package
:run_build
call :ensure_venv
    
echo Building package...
python -m build
    
echo Build complete!
goto :eof

REM Install the package in development mode
:run_install
call :ensure_venv
    
echo Installing package in development mode...
uv pip install -e .
    
echo Installation complete!
goto :eof

REM Run the CLI
:run_cli
call :ensure_venv

python -m spicy_cli.main %*
goto :eof

REM Parse command
if "%~1"=="" (
    call :show_help
    exit /b 0
)

set "COMMAND=%~1"
shift

if "%COMMAND%"=="lint" (
    call :run_lint
) else if "%COMMAND%"=="format" (
    call :run_format
) else if "%COMMAND%"=="test" (
    call :run_tests
) else if "%COMMAND%"=="clean" (
    call :run_clean
) else if "%COMMAND%"=="build" (
    call :run_build
) else if "%COMMAND%"=="install" (
    call :run_install
) else if "%COMMAND%"=="run" (
    call :run_cli %*
) else if "%COMMAND%"=="help" (
    call :show_help
) else (
    echo Unknown command: %COMMAND%
    call :show_help
    exit /b 1
)
