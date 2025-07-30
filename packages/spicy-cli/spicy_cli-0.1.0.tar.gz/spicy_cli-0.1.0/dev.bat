@echo off
REM Development commands script for Windows
REM Usage: dev.bat [command]

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="dev" goto dev
if "%1"=="test" goto test
if "%1"=="test-all" goto test-all
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="type-check" goto type-check
if "%1"=="security" goto security
if "%1"=="clean" goto clean
if "%1"=="build" goto build
if "%1"=="pre-commit" goto pre-commit
if "%1"=="ci" goto ci

goto help

:help
echo Available commands:
echo   install      - Install the package
echo   dev          - Install development dependencies
echo   test         - Run tests
echo   test-all     - Run tests with coverage
echo   lint         - Run all linting tools
echo   format       - Format code
echo   type-check   - Run type checking
echo   security     - Run security checks
echo   clean        - Clean up build artifacts
echo   build        - Build the package
echo   pre-commit   - Run pre-commit on all files
echo   ci           - Run all CI checks locally
goto end

:install
uv pip install -e .
goto end

:dev
uv pip install -e ".[dev]"
goto end

:test
uv run pytest -v --cov=spicy_cli --cov-report=term-missing
goto end

:test-all
uv run pytest -v --cov=spicy_cli --cov-report=xml --cov-report=term-missing --cov-report=html
goto end

:lint
uv run black --check .
uv run isort --check-only .
uv run ruff check .
uv run mypy src/
uv run pylint src/spicy_cli/
goto end

:format
uv run black .
uv run isort .
uv run ruff check . --fix
goto end

:type-check
uv run mypy src/
goto end

:security
uv run safety scan
uv run bandit -r src/
goto end

:clean
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
for /d %%i in (*.egg-info) do rmdir /s /q "%%i" 2>nul
rmdir /s /q .pytest_cache 2>nul
rmdir /s /q .mypy_cache 2>nul
rmdir /s /q .ruff_cache 2>nul
rmdir /s /q htmlcov 2>nul
del .coverage 2>nul
del coverage.xml 2>nul
goto end

:build
call :clean
uv run python -m build
goto end

:pre-commit
uv run pre-commit run --all-files
goto end

:ci
call :lint
call :test
call :security
goto end

:end
