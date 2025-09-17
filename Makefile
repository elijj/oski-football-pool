.PHONY: install install-dev lint test run clean format type-check

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install all dependencies including dev"
	@echo "  lint        - Run linting with ruff"
	@echo "  format      - Format code with ruff"
	@echo "  type-check  - Run type checking with mypy"
	@echo "  test        - Run tests with pytest"
	@echo "  run         - Run the CLI application"
	@echo "  clean       - Clean up generated files"

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

# Code quality targets
lint:
	ruff check .

format:
	ruff format .

type-check:
	mypy football_pool/

# Testing
test:
	pytest

test-cov:
	pytest --cov=football_pool --cov-report=html --cov-report=term-missing

# Running the application
run:
	python -m football_pool.cli

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
