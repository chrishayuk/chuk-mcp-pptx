.PHONY: help clean clean-build clean-pyc clean-test clean-all lint format test test-cov test-watch typecheck security dev-install build publish publish-test publish-manual bump-patch bump-minor bump-major run version check coverage-report release info

# Default target
help:
	@echo "chuk-mcp-pptx - PowerPoint MCP Server"
	@echo ""
	@echo "Setup:"
	@echo "  dev-install     Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  run            Run the MCP server"
	@echo "  test           Run tests"
	@echo "  test-cov       Run tests with coverage report"
	@echo "  coverage-report Show current coverage report"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with ruff"
	@echo "  typecheck      Run type checking with mypy"
	@echo "  security       Run security checks"
	@echo "  check          Run all checks (lint, typecheck, security, test)"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean          Remove build artifacts"
	@echo "  clean-all      Remove all generated files"
	@echo ""
	@echo "Publishing:"
	@echo "  version        Show current version"
	@echo "  bump-patch     Bump patch version (0.0.X)"
	@echo "  bump-minor     Bump minor version (0.X.0)"
	@echo "  bump-major     Bump major version (X.0.0)"
	@echo "  build          Build distribution packages"
	@echo "  publish        Create tag and trigger automated release"
	@echo "  publish-test   Publish to TestPyPI"
	@echo "  publish-manual Manually publish to PyPI"
	@echo "  release        Alias for publish"
	@echo "  info           Show project information"

dev-install:
	@echo "Installing development dependencies..."
	@if command -v uv >/dev/null 2>&1; then \
		uv sync --dev; \
	else \
		pip install -e ".[dev]"; \
	fi
	@echo ""
	@echo "✓ Development environment ready!"
	@echo ""
	@echo "Available commands:"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make check      - Run all checks (lint, typecheck, security, test)"

run:
	@echo "Starting chuk-mcp-pptx server..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run python -m chuk_mcp_pptx.server; \
	else \
		python -m chuk_mcp_pptx.server; \
	fi

test:
	@echo "Running tests..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest; \
	elif command -v pytest >/dev/null 2>&1; then \
		pytest; \
	else \
		python -m pytest; \
	fi

coverage coverage-report:
	@echo "Coverage Report:"
	@echo "================"
	@if command -v uv >/dev/null 2>&1; then \
		uv run coverage report --omit="tests/*" || echo "No coverage data found. Run 'make test-cov' first."; \
	else \
		coverage report --omit="tests/*" || echo "No coverage data found. Run 'make test-cov' first."; \
	fi

test-cov:
	@echo "Running tests with coverage..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run pytest --cov=src --cov-report=html --cov-report=term --cov-report=term-missing:skip-covered; \
		exit_code=$$?; \
		echo ""; \
		echo "=========================="; \
		echo "Coverage Summary:"; \
		echo "=========================="; \
		uv run coverage report --omit="tests/*" | tail -5; \
		echo ""; \
		echo "HTML coverage report saved to: htmlcov/index.html"; \
		exit $$exit_code; \
	else \
		pytest --cov=src --cov-report=html --cov-report=term --cov-report=term-missing:skip-covered; \
		exit_code=$$?; \
		echo ""; \
		echo "=========================="; \
		echo "Coverage Summary:"; \
		echo "=========================="; \
		coverage report --omit="tests/*" | tail -5; \
		echo ""; \
		echo "HTML coverage report saved to: htmlcov/index.html"; \
		exit $$exit_code; \
	fi

lint:
	@echo "Running linters..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run ruff check .; \
		uv run ruff format --check .; \
	elif command -v ruff >/dev/null 2>&1; then \
		ruff check .; \
		ruff format --check .; \
	else \
		echo "Ruff not found. Install with: pip install ruff"; \
	fi

format:
	@echo "Formatting code..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run ruff format .; \
		uv run ruff check --fix .; \
	elif command -v ruff >/dev/null 2>&1; then \
		ruff format .; \
		ruff check --fix .; \
	else \
		echo "Ruff not found. Install with: pip install ruff"; \
	fi

typecheck:
	@echo "Running type checker..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run mypy src --ignore-missing-imports; \
	elif command -v mypy >/dev/null 2>&1; then \
		mypy src --ignore-missing-imports; \
	else \
		echo "MyPy not found. Install with: pip install mypy"; \
	fi

security:
	@echo "Running security checks..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run bandit -r src -ll; \
	elif command -v bandit >/dev/null 2>&1; then \
		bandit -r src -ll; \
	else \
		echo "Bandit not found. Install with: pip install bandit"; \
	fi

check: lint typecheck security test
	@echo "All checks completed."

clean: clean-build clean-pyc clean-test

clean-build:
	@echo "Cleaning build artifacts..."
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	@echo "Cleaning Python file artifacts..."
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	@echo "Cleaning test artifacts..."
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-all: clean
	@echo "Cleaning all generated files..."
	rm -rf presentations/
	rm -rf *.pptx

version:
	@if command -v uv >/dev/null 2>&1; then \
		uv run python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])"; \
	else \
		python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])"; \
	fi

bump-patch:
	@echo "Bumping patch version..."
ifdef UV
	uv run bump2version patch
else
	bump2version patch
endif
	@echo "New version: $$(make version)"

bump-minor:
	@echo "Bumping minor version..."
ifdef UV
	uv run bump2version minor
else
	bump2version minor
endif
	@echo "New version: $$(make version)"

bump-major:
	@echo "Bumping major version..."
ifdef UV
	uv run bump2version major
else
	bump2version major
endif
	@echo "New version: $$(make version)"

build: clean
	@echo "Building distribution packages..."
ifdef UV
	uv build
else
	$(PYTHON) -m build
endif
	@echo "Build complete! Check dist/ directory"

publish: build
	@echo "Publishing to PyPI..."
	@echo "Version: $$(make version)"
	@echo "Are you sure? This will publish to PyPI."
	@read -p "Press Enter to continue or Ctrl+C to cancel..."
ifdef UV
	uv publish
else
	$(PYTHON) -m twine upload dist/*
endif
	@echo "Published to PyPI!"
	@echo "Visit: https://pypi.org/project/chuk-mcp-pptx/"

publish-test: build
	@echo "Publishing to TestPyPI..."
ifdef UV
	uv publish --index https://test.pypi.org/legacy/
else
	$(PYTHON) -m twine upload --repository testpypi dist/*
endif
	@echo "Published to TestPyPI!"
	@echo "Visit: https://test.pypi.org/project/chuk-mcp-pptx/"

publish-manual: build
	@echo "Manual publish to PyPI..."
	@echo "Version: $$(make version)"
ifdef UV
	uv publish
else
	$(PYTHON) -m twine upload dist/*
endif
	@echo "Published!"
