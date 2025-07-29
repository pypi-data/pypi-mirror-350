#!/bin/bash

# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type d -name "test_graph_fixture" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Remove test outputs
rm -rf test_output/*

# Remove build artifacts
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Remove coverage files
rm -f .coverage
rm -rf htmlcov/

# Remove pytest cache
rm -rf .pytest_cache/

# Remove SQLite databases
find . -type f -name "*.db" -delete
find . -type f -name "*.sqlite" -delete
find . -type f -name "*.sqlite3" -delete
