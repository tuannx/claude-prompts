#!/bin/bash
# Script to run tests with parallel execution to verify isolation fixes

echo "Running tests with parallel execution..."
echo "=================================="

# Install pytest-xdist if not already installed
pip install pytest-xdist &>/dev/null

# Run tests with 4 parallel workers
echo "Running with 4 parallel workers..."
pytest -n 4 --verbose tests/test_cli.py tests/test_indexer.py

echo ""
echo "=================================="
echo "Test execution completed."
echo ""
echo "If tests pass, the isolation issues have been fixed."
echo "If tests fail with database/file conflicts, more work is needed."