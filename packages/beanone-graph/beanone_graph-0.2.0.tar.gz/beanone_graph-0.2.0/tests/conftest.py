"""Configure test environment."""

import os
import shutil
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Create test output directory if it doesn't exist
test_output_dir = Path(project_root) / "test_output"
test_output_dir.mkdir(exist_ok=True)


def pytest_sessionstart(session):
    """Clean up test output directory before running tests."""
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)
    test_output_dir.mkdir(exist_ok=True)
