.PHONY: help clean clean-build clean-pyc clean-test clean-all lint format test test-cov test-watch typecheck security dev-install build publish publish-test publish-manual bump-patch bump-minor bump-major run version

# Detect package manager
UV := $(shell command -v uv 2> /dev/null)
ifdef UV
    PIP := uv pip
    PYTHON := uv run python
    PYTEST := uv run pytest
else
    PIP := pip
    PYTHON := python
    PYTEST := pytest
endif

help:
	@echo "chuk-mcp-pptx development tasks"
	@echo ""
	@echo "Setup:"
	@echo "  dev-install    Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  run           Run the MCP server"
	@echo "  test          Run tests"
	@echo "  test-cov      Run tests with coverage report"
	@echo "  test-watch    Run tests in watch mode"
	@echo "  lint          Run linting checks"
	@echo "  format        Format code with black and isort"
	@echo "  typecheck     Run type checking with mypy"
	@echo "  security      Run security checks"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean         Remove build artifacts"
	@echo "  clean-all     Remove all generated files including presentations"
	@echo ""
	@echo "Publishing:"
	@echo "  bump-patch    Bump patch version (0.0.X)"
	@echo "  bump-minor    Bump minor version (0.X.0)"
	@echo "  bump-major    Bump major version (X.0.0)"
	@echo "  build         Build distribution packages"
	@echo "  publish       Publish to PyPI (automated)"
	@echo "  publish-test  Publish to TestPyPI"
	@echo "  publish-manual Publish to PyPI (manual)"

dev-install:
	@echo "Installing development dependencies..."
ifdef UV
	uv sync --extra dev
else
	pip install -e ".[dev]"
endif
	@echo "Development environment ready!"

run:
	@echo "Starting chuk-mcp-pptx server..."
	$(PYTHON) -m chuk_mcp_pptx.async_server

test:
	@echo "Running tests..."
	$(PYTEST) tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	$(PYTEST) tests/ --cov=src/chuk_mcp_pptx --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-watch:
	@echo "Running tests in watch mode..."
	$(PYTEST) tests/ -v --looponfail

lint:
	@echo "Running linting checks..."
	$(PYTHON) -m ruff check src/ tests/
	$(PYTHON) -m flake8 src/ tests/ --max-line-length=120 --exclude=__pycache__,.git,build,dist

format:
	@echo "Formatting code..."
	$(PYTHON) -m black src/ tests/
	$(PYTHON) -m isort src/ tests/
	@echo "Code formatted!"

typecheck:
	@echo "Running type checks..."
	$(PYTHON) -m mypy src/chuk_mcp_pptx

security:
	@echo "Running security checks..."
ifdef UV
	uv run bandit -r src/chuk_mcp_pptx
else
	bandit -r src/chuk_mcp_pptx
endif

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
	@$(PYTHON) -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])"

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
