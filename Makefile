# PowerPoint MCP Server - Development Makefile
# ============================================

# Variables
PYTHON := uv run python
PIP := uv pip
PROJECT := chuk_mcp_pptx
SRC_DIR := src/$(PROJECT)
TEST_DIR := tests
EXAMPLES_DIR := examples
OUTPUTS_DIR := outputs

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

# Phony targets
.PHONY: help install dev clean test lint format typecheck coverage security audit docs serve-docs build deploy all ci quality examples

## General Commands ------------------------------------------------

help: ## Show this help message
	@echo "$(BLUE)PowerPoint MCP Server - Development Commands$(NC)"
	@echo "============================================="
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Quick Start:$(NC)"
	@echo "  make install    - Install all dependencies"
	@echo "  make test      - Run tests"
	@echo "  make quality   - Run all quality checks"
	@echo "  make examples  - Run example scripts"

install: ## Install project dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@$(PIP) install -e .
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	@$(PIP) install -e ".[dev]"
	@$(PIP) install pytest pytest-asyncio pytest-mock pytest-cov
	@$(PIP) install black isort mypy pylint flake8
	@$(PIP) install bandit safety
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning up...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name ".coverage" -delete
	@rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	@rm -rf htmlcov/ .coverage coverage.xml
	@rm -rf $(OUTPUTS_DIR)/*.pptx 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

## Testing --------------------------------------------------------

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) -v --tb=short
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-fast: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) -n auto --tb=short
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR)/components -v --tb=short
	@echo "$(GREEN)✓ Unit tests complete$(NC)"

test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR)/integration -v --tb=short
	@echo "$(GREEN)✓ Integration tests complete$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) --watch

coverage: ## Generate test coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	@$(PYTHON) -m pytest $(TEST_DIR) --cov=$(PROJECT) --cov-report=html --cov-report=term --cov-report=xml
	@echo "$(GREEN)✓ Coverage report generated$(NC)"
	@echo "  HTML report: htmlcov/index.html"
	@echo "  Coverage: $$(grep -oP 'TOTAL.*\K\d+%' coverage.txt 2>/dev/null || echo 'Run to see')"

coverage-html: coverage ## Open coverage HTML report
	@echo "$(BLUE)Opening coverage report...$(NC)"
	@open htmlcov/index.html 2>/dev/null || xdg-open htmlcov/index.html 2>/dev/null || echo "Please open htmlcov/index.html manually"

## Code Quality ---------------------------------------------------

lint: ## Run linting checks (flake8, pylint)
	@echo "$(BLUE)Running linters...$(NC)"
	@echo "  Running flake8..."
	@$(PYTHON) -m flake8 $(SRC_DIR) $(TEST_DIR) --max-line-length=100 --extend-ignore=E203,W503 || true
	@echo "  Running pylint..."
	@$(PYTHON) -m pylint $(SRC_DIR) --max-line-length=100 --disable=C0111,R0903,R0801 || true
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	@echo "  Running isort..."
	@$(PYTHON) -m isort $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)
	@echo "  Running black..."
	@$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR) --line-length=100
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code format...$(NC)"
	@$(PYTHON) -m isort $(SRC_DIR) $(TEST_DIR) --check-only --diff
	@$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR) --check --line-length=100
	@echo "$(GREEN)✓ Format check complete$(NC)"

typecheck: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(NC)"
	@$(PYTHON) -m mypy $(SRC_DIR) --ignore-missing-imports --no-strict-optional || true
	@echo "$(GREEN)✓ Type checking complete$(NC)"

quality: lint format-check typecheck ## Run all quality checks
	@echo "$(GREEN)✓ All quality checks complete$(NC)"

## Security -------------------------------------------------------

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	@echo "  Running bandit..."
	@$(PYTHON) -m bandit -r $(SRC_DIR) -f json -o bandit-report.json 2>/dev/null || true
	@$(PYTHON) -m bandit -r $(SRC_DIR) || true
	@echo "  Running safety check..."
	@$(PYTHON) -m safety check || true
	@echo "$(GREEN)✓ Security checks complete$(NC)"

audit: security ## Alias for security checks
	@echo "$(GREEN)✓ Audit complete$(NC)"

## Documentation --------------------------------------------------

docs: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	@$(PYTHON) -m mkdocs build
	@echo "$(GREEN)✓ Documentation built$(NC)"

serve-docs: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation at http://localhost:8000...$(NC)"
	@$(PYTHON) -m mkdocs serve

## Examples -------------------------------------------------------

examples: ## Run all example scripts
	@echo "$(BLUE)Running example scripts...$(NC)"
	@mkdir -p $(OUTPUTS_DIR)
	@echo "  Running beautiful_chart_gallery..."
	@$(PYTHON) $(EXAMPLES_DIR)/beautiful_chart_gallery.py || true
	@echo "  Running theme_focused_showcase..."
	@$(PYTHON) $(EXAMPLES_DIR)/theme_focused_showcase.py || true
	@echo "  Running domain_focused_showcase..."
	@$(PYTHON) $(EXAMPLES_DIR)/domain_focused_showcase.py || true
	@echo "$(GREEN)✓ Examples complete$(NC)"
	@echo "  Output files in: $(OUTPUTS_DIR)/"

examples-simple: ## Run simple example only
	@echo "$(BLUE)Running simple example...$(NC)"
	@mkdir -p $(OUTPUTS_DIR)
	@$(PYTHON) $(EXAMPLES_DIR)/simple_example.py
	@echo "$(GREEN)✓ Simple example complete$(NC)"

## Build & Deploy -------------------------------------------------

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	@$(PYTHON) -m build
	@echo "$(GREEN)✓ Build complete$(NC)"

publish-test: build ## Publish to TestPyPI
	@echo "$(BLUE)Publishing to TestPyPI...$(NC)"
	@$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "$(GREEN)✓ Published to TestPyPI$(NC)"

publish: build ## Publish to PyPI
	@echo "$(BLUE)Publishing to PyPI...$(NC)"
	@echo "$(YELLOW)Warning: This will publish to the real PyPI!$(NC)"
	@read -p "Are you sure? (y/N) " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(PYTHON) -m twine upload dist/*; \
		echo "$(GREEN)✓ Published to PyPI$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

## CI/CD ----------------------------------------------------------

ci: install dev lint typecheck test coverage ## Run full CI pipeline
	@echo "$(GREEN)✓ CI pipeline complete$(NC)"

pre-commit: format lint typecheck test-fast ## Run pre-commit checks
	@echo "$(GREEN)✓ Pre-commit checks passed$(NC)"

## Development Workflow -------------------------------------------

watch: ## Watch for changes and run tests
	@echo "$(BLUE)Watching for changes...$(NC)"
	@$(PYTHON) -m pytest_watch $(TEST_DIR) --clear --wait

serve: ## Run the MCP server
	@echo "$(BLUE)Starting PowerPoint MCP Server...$(NC)"
	@$(PYTHON) -m chuk_mcp_pptx.server

debug: ## Run with debug logging
	@echo "$(BLUE)Starting server with debug logging...$(NC)"
	@DEBUG=1 $(PYTHON) -m chuk_mcp_pptx.server

## Statistics -----------------------------------------------------

stats: ## Show code statistics
	@echo "$(BLUE)Code Statistics$(NC)"
	@echo "==============="
	@echo ""
	@echo "$(YELLOW)Lines of Code:$(NC)"
	@find $(SRC_DIR) -name "*.py" -exec wc -l {} + | tail -1
	@echo ""
	@echo "$(YELLOW)Number of Files:$(NC)"
	@find $(SRC_DIR) -name "*.py" | wc -l
	@echo ""
	@echo "$(YELLOW)Test Files:$(NC)"
	@find $(TEST_DIR) -name "test_*.py" | wc -l
	@echo ""
	@echo "$(YELLOW)Test Cases:$(NC)"
	@grep -r "def test_" $(TEST_DIR) | wc -l
	@echo ""
	@echo "$(YELLOW)TODO Items:$(NC)"
	@grep -r "TODO" $(SRC_DIR) | wc -l || echo "0"

## Maintenance ----------------------------------------------------

update-deps: ## Update all dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	@$(PIP) install --upgrade pip
	@$(PIP) list --outdated
	@echo "$(YELLOW)Run 'uv pip install --upgrade <package>' to update specific packages$(NC)"

check-deps: ## Check for outdated dependencies
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@$(PIP) list --outdated

freeze: ## Freeze current dependencies
	@echo "$(BLUE)Freezing dependencies...$(NC)"
	@$(PIP) freeze > requirements.txt
	@echo "$(GREEN)✓ Dependencies frozen to requirements.txt$(NC)"

## Shortcuts ------------------------------------------------------

t: test ## Shortcut for test
c: coverage ## Shortcut for coverage
f: format ## Shortcut for format
l: lint ## Shortcut for lint
q: quality ## Shortcut for quality
e: examples ## Shortcut for examples

# Special targets
all: clean install dev quality test coverage examples ## Run everything
	@echo "$(GREEN)✓ All tasks complete!$(NC)"

.PHONY: t c f l q e