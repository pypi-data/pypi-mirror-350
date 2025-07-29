#!/bin/bash

# Exit on error
set -e

echo "Running pre-commit hooks..."
pre-commit run --all-files

echo "Running tests with coverage..."
python -m pytest --cov=graph_reader --cov-report=term-missing

echo "All checks passed! You can now push your changes."
