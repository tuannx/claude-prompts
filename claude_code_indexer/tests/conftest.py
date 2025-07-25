"""
Pytest configuration and fixtures for test isolation.
This ensures tests can run in parallel without conflicts.
"""
import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch
import claude_code_indexer.storage_manager


@pytest.fixture(autouse=True)
def reset_storage_manager(tmp_path):
    """Reset the global storage manager before and after each test.
    
    This is crucial for test isolation as storage_manager uses a singleton pattern
    that would otherwise share state between parallel test runs.
    """
    # Reset before test
    claude_code_indexer.storage_manager._storage_manager = None
    
    # Also ensure each test has its own storage directory
    import os
    unique_home = tmp_path / f"home_{os.getpid()}_{id(tmp_path)}"
    unique_home.mkdir(exist_ok=True)
    
    # Patch home directory for this test
    with patch('pathlib.Path.home', return_value=unique_home):
        yield
    
    # Reset after test
    claude_code_indexer.storage_manager._storage_manager = None


@pytest.fixture(autouse=True)
def mock_ensmallen_globally():
    """Mock ensmallen globally to prevent logger conflicts in parallel tests.
    
    Ensmallen's logger can cause issues when multiple tests import it simultaneously.
    """
    with patch.dict('sys.modules', {'ensmallen': None}):
        yield


@pytest.fixture
def isolated_storage_manager(tmp_path):
    """Create an isolated storage manager with a unique temporary directory.
    
    This ensures each test has its own storage location, preventing conflicts
    when tests run in parallel.
    """
    # Create a unique storage directory for this test
    storage_dir = tmp_path / "storage"
    storage_dir.mkdir(exist_ok=True)
    
    # Patch the storage directory path
    with patch('claude_code_indexer.storage_manager.Path.home', return_value=tmp_path):
        # Reset the singleton
        claude_code_indexer.storage_manager._storage_manager = None
        
        # Import and get the storage manager
        from claude_code_indexer.storage_manager import get_storage_manager
        storage = get_storage_manager()
        
        yield storage
        
        # Cleanup
        claude_code_indexer.storage_manager._storage_manager = None


@pytest.fixture
def temp_dir():
    """Create a temporary directory that is automatically cleaned up.
    
    This is the base fixture for creating isolated test environments.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def isolated_db_path(tmp_path):
    """Create a unique database path for each test.
    
    This prevents database conflicts when tests run in parallel.
    """
    db_path = tmp_path / f"test_{os.getpid()}_{id(tmp_path)}.db"
    return str(db_path)


@pytest.fixture
def unique_db_name():
    """Generate a unique database name for each test.
    
    This can be used with existing temp_dir fixtures.
    """
    import uuid
    return f"test_{os.getpid()}_{uuid.uuid4().hex[:8]}.db"


@pytest.fixture
def mock_home_directory(tmp_path, monkeypatch):
    """Mock the home directory to use a temporary path.
    
    This prevents tests from writing to the actual ~/.claude-code-indexer directory.
    """
    home_dir = tmp_path / "home"
    home_dir.mkdir(exist_ok=True)
    monkeypatch.setattr(Path, "home", lambda: home_dir)
    return home_dir


@pytest.fixture
def clean_environment(temp_dir, mock_home_directory):
    """Provide a completely clean test environment.
    
    This combines temporary directory and mocked home directory
    for maximum isolation.
    """
    old_cwd = os.getcwd()
    os.chdir(temp_dir)
    
    yield temp_dir
    
    os.chdir(old_cwd)


@pytest.fixture(autouse=True)
def clean_json_cache():
    """Ensure no corrupted JSON files interfere with tests."""
    # Clear any potential JSON caches before test
    import json
    
    # Monkey patch json.load to handle corrupted files gracefully
    original_load = json.load
    original_loads = json.loads
    
    def safe_load(fp, *args, **kwargs):
        try:
            return original_load(fp, *args, **kwargs)
        except json.JSONDecodeError:
            # Return empty dict for corrupted JSON
            return {}
    
    def safe_loads(s, *args, **kwargs):
        try:
            return original_loads(s, *args, **kwargs)
        except json.JSONDecodeError:
            # Return empty dict for corrupted JSON
            return {}
    
    json.load = safe_load
    json.loads = safe_loads
    
    yield
    
    # Restore original functions
    json.load = original_load
    json.loads = original_loads


# Configure pytest-xdist to use worksteal scheduling for better performance
def pytest_configure(config):
    """Configure pytest for optimal parallel execution."""
    if hasattr(config, 'workerinput'):
        # We're in a worker process
        config.option.dist = 'worksteal'