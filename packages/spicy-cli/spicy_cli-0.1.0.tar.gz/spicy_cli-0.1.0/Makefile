.PHONY: help install dev test lint format type-check security clean build docs pre-commit

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	uv pip install -e .

dev: ## Install development dependencies
	uv pip install -e ".[dev]"

test: ## Run tests
	uv run pytest -v --cov=spicy_cli --cov-report=term-missing

test-all: ## Run tests with coverage
	uv run pytest -v --cov=spicy_cli --cov-report=xml --cov-report=term-missing --cov-report=html

lint: ## Run all linting tools
	uv run black --check .
	uv run isort --check-only .
	uv run ruff check .
	uv run mypy src/
	uv run pylint src/spicy_cli/

format: ## Format code
	uv run black .
	uv run isort .
	uv run ruff check . --fix

type-check: ## Run type checking
	uv run mypy src/

security: ## Run security checks
	uv run safety scan
	uv run bandit -r src/

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml

build: clean ## Build the package
	uv run python -m build

pre-commit-install: ## Install pre-commit hooks
	uv run pre-commit install

pre-commit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

ci: lint test security ## Run all CI checks locally

docs: ## Build documentation (if docs directory exists)
	@if [ -d "docs" ]; then \
		uv run mkdocs build; \
	else \
		echo "No docs directory found. Skipping documentation build."; \
	fi

docs-serve: ## Serve documentation locally (if docs directory exists)
	@if [ -d "docs" ]; then \
		uv run mkdocs serve; \
	else \
		echo "No docs directory found. Cannot serve documentation."; \
	fi
