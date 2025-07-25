# Test Isolation Fix for Parallel Execution

## Problem Summary

The test suite had isolation issues preventing parallel test execution due to:

1. **Global Singleton Storage Manager**: The `get_storage_manager()` function returns a global singleton instance that all tests share, causing conflicts when tests run in parallel.

2. **Shared Database Paths**: Tests were using hardcoded database paths like 'test.db' that could conflict when multiple tests run simultaneously.

3. **Shared App Home Directory**: All tests were using the same ~/.claude-code-indexer directory for storage.

4. **No Test-Level Cleanup**: The global storage manager instance wasn't being reset between tests.

## Solution Implemented

### 1. Created `tests/conftest.py`

A comprehensive pytest configuration file that provides:

- **`reset_storage_manager` fixture** (autouse=True): Automatically resets the global storage manager before and after each test
- **`isolated_storage_manager` fixture**: Creates a storage manager with a unique temporary directory for each test
- **`isolated_db_path` fixture**: Provides unique database paths for tests
- **Global ensmallen mocking**: Prevents logger conflicts across all tests
- **Test markers**: Categories for better test organization

### 2. Fixed Hardcoded Database Paths in `test_cli.py`

Changed all instances of hardcoded 'test.db' to use unique paths:
- `test_query.db` → `Path(temp_dir) / 'test_query.db'`
- `test_search.db` → `Path(temp_dir) / 'test_search.db'`
- `test_stats.db` → `Path(temp_dir) / 'test_stats.db'`

### 3. Created `pytest.ini`

Configuration file for pytest that:
- Defines test markers (cli, indexer, mcp, background)
- Sets timeout to 300 seconds
- Configures coverage options
- Enables colored output and verbose mode

### 4. Created Test Script

`run_parallel_tests.sh` - A script to verify the fixes work with parallel execution.

## How to Use

### Running Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run all tests with 4 parallel workers
pytest -n 4

# Run specific test files in parallel
pytest -n 4 tests/test_cli.py tests/test_indexer.py

# Run with the provided script
./run_parallel_tests.sh
```

### Using Isolated Fixtures in New Tests

```python
def test_my_new_test(isolated_storage_manager, temp_dir):
    """Example test using isolated storage"""
    # isolated_storage_manager is automatically patched
    # and will use a unique temporary directory
    
    indexer = CodeGraphIndexer()
    # This will use the isolated storage manager
    
def test_with_custom_db(isolated_db_path):
    """Example test with isolated database"""
    indexer = CodeGraphIndexer(db_path=isolated_db_path)
    # Database will be in a unique temporary location
```

## Benefits

1. **Parallel Execution**: Tests can now run in parallel without conflicts
2. **True Isolation**: Each test gets its own storage directory and database
3. **Automatic Cleanup**: Temporary directories are cleaned up after tests
4. **No Manual Mocking**: The conftest.py handles common mocking needs
5. **Consistent Environment**: All tests start with a clean state

## Future Improvements

1. Consider refactoring the storage manager to support dependency injection instead of a global singleton
2. Add more granular fixtures for specific test scenarios
3. Create test utilities for common test data setup
4. Add performance benchmarks for parallel vs sequential execution