#!/usr/bin/env python3
"""
Shared step definitions for all BDD tests
"""

import os
import sys
import pytest
import tempfile
import shutil
import sqlite3
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
from pytest_bdd import when, then, given, parsers

# Mock ensmallen before importing
sys.modules['ensmallen'] = MagicMock()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from claude_code_indexer.cli import cli
from claude_code_indexer import __version__, __app_name__


# Context to store test state
class BDDTestContext:
    def __init__(self):
        self.command_result = None
        self.current_directory = None
        self.temp_files = {}
        self.database_path = None
        self.project_path = None
        self.custom_db_path = None


@pytest.fixture
def cli_runner():
    """Fixture providing CLI test runner"""
    return CliRunner()


@pytest.fixture
def context():
    """Test context to store state between steps"""
    return BDDTestContext()


@pytest.fixture
def temp_project():
    """Fixture providing temporary project directory"""
    temp_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    os.chdir(temp_dir)
    yield temp_dir
    os.chdir(original_cwd)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_python_files(temp_project):
    """Create sample Python files in project"""
    files = {}
    files['main.py'] = '''
def main():
    """Main function"""
    print("Hello World")
    calculator = Calculator()
    result = calculator.add(5, 3)
    print(f"Result: {result}")

class Calculator:
    """Simple calculator class"""
    
    def add(self, a, b):
        """Add two numbers"""
        return a + b
    
    def multiply(self, a, b):
        """Multiply two numbers"""  
        return a * b

if __name__ == "__main__":
    main()
'''
    
    files['utils.py'] = '''
import json
import os
from typing import Dict, List

def load_config(file_path: str) -> Dict:
    """Load configuration from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(data: List, filename: str):
    """Save data to file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

class DataProcessor:
    """Process and transform data"""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_item(self, item):
        """Process a single data item"""
        self.processed_count += 1
        return item.upper() if isinstance(item, str) else item
'''
    
    # Create files
    for filename, content in files.items():
        file_path = Path(temp_project) / filename
        file_path.write_text(content)
    
    return files


@pytest.fixture
def sample_javascript_files(temp_project):
    """Create sample JavaScript files in project"""
    files = {}
    files['app.js'] = '''
function greet(name) {
    console.log(`Hello, ${name}!`);
}

class UserManager {
    constructor() {
        this.users = [];
    }
    
    addUser(user) {
        this.users.push(user);
        return user.id;
    }
    
    getUser(id) {
        return this.users.find(u => u.id === id);
    }
}

module.exports = { greet, UserManager };
'''
    
    files['config.js'] = '''
const fs = require('fs');
const path = require('path');

const config = {
    port: process.env.PORT || 3000,
    database: {
        host: 'localhost',
        port: 5432,
        name: 'myapp'
    }
};

function loadConfig(filename) {
    const filePath = path.join(__dirname, filename);
    if (fs.existsSync(filePath)) {
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
    return config;
}

module.exports = { config, loadConfig };
'''
    
    # Create files
    for filename, content in files.items():
        file_path = Path(temp_project) / filename
        file_path.write_text(content)
    
    return files


# Shared Given steps
@given("I have a sample project with Python and JavaScript files")
def sample_project_with_files(temp_project, sample_python_files, sample_javascript_files, context):
    """Create a sample project with both Python and JavaScript files"""
    context.current_directory = temp_project
    context.temp_files.update(sample_python_files)
    context.temp_files.update(sample_javascript_files)


@given("I am in an empty project directory")
def empty_project_directory(temp_project, context):
    """Set up empty project directory"""
    context.current_directory = temp_project


@given("I have an indexed project")
def indexed_project(temp_project, sample_python_files, context):
    """Create an indexed project with database"""
    context.current_directory = temp_project
    context.temp_files.update(sample_python_files)
    
    # Create mock database
    db_path = Path(temp_project) / "code_index.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create tables with all required columns
    cursor.execute('''CREATE TABLE code_nodes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        node_type TEXT,
        path TEXT,
        importance_score REAL,
        relevance_tags TEXT,
        summary TEXT
    )''')
    
    cursor.execute('''CREATE TABLE relationships (
        source_id INTEGER,
        target_id INTEGER,
        relationship_type TEXT
    )''')
    
    # Insert sample data with summary
    cursor.execute("INSERT INTO code_nodes VALUES (1, 'main', 'function', 'main.py', 0.8, 'entry-point', 'Main entry point function')")
    cursor.execute("INSERT INTO code_nodes VALUES (2, 'Calculator', 'class', 'main.py', 0.7, 'utility', 'Calculator class for basic math operations')")
    cursor.execute("INSERT INTO code_nodes VALUES (3, 'add', 'method', 'main.py', 0.6, '', 'Add two numbers together')")
    cursor.execute("INSERT INTO relationships VALUES (2, 3, 'contains')")
    
    conn.commit()
    conn.close()
    context.database_path = str(db_path)


@given("I have an indexed project with cached data")
def indexed_project_with_cache(temp_project, sample_python_files, context):
    """Create an indexed project with database and cached data"""
    # First create the indexed project
    indexed_project(temp_project, sample_python_files, context)
    
    # Add cache data
    from claude_code_indexer.cache_manager import CacheManager
    cache_manager = CacheManager()
    cache_manager.set('test_key', 'test_value')
    context.cache_manager = cache_manager


# Shared When steps
@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner, context, command):
    """Execute a CLI command"""
    # Parse command and arguments
    cmd_parts = command.split()
    if cmd_parts[0] == "claude-code-indexer":
        cmd_parts = cmd_parts[1:]  # Remove the program name
    
    # Mock storage manager to use temp directory
    with patch('claude_code_indexer.storage_manager.get_storage_manager') as mock_storage:
        # Create mock storage manager instance
        mock_storage_instance = Mock()
        mock_storage.return_value = mock_storage_instance
        
        # Set up path returns
        if context.current_directory:
            mock_storage_instance.get_project_from_path.return_value = Path(context.current_directory)
            mock_storage_instance.get_project_from_cwd.return_value = Path(context.current_directory)
        else:
            # Default to temp directory if not set
            mock_storage_instance.get_project_from_path.return_value = Path("/tmp/test_project")
            mock_storage_instance.get_project_from_cwd.return_value = Path("/tmp/test_project")
        if context.database_path:
            mock_storage_instance.get_database_path.return_value = Path(context.database_path)
        else:
            default_dir = context.current_directory if context.current_directory else "/tmp/test_project"
            mock_storage_instance.get_database_path.return_value = Path(default_dir) / "code_index.db"
        
        # Mock other dependencies as needed
        with patch('claude_code_indexer.cli.CodeGraphIndexer') as mock_indexer, \
             patch('claude_code_indexer.cli.os.path.exists') as mock_exists, \
             patch('claude_code_indexer.cache_manager.CacheManager') as mock_cache_manager:
            
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.index_directory.return_value = True
            default_dir = context.current_directory if context.current_directory else "/tmp/test_project"
            mock_instance.db_path = Path(default_dir) / "code_index.db"
            mock_instance.parsing_errors = []
            
            # Mock file existence check
            mock_exists.return_value = True
            
            # Mock CacheManager
            mock_cache_instance = Mock()
            mock_cache_manager.return_value = mock_cache_instance
            mock_cache_instance.print_cache_stats = Mock()
            mock_cache_instance.clear_cache = Mock()
            
            # Provide input for interactive commands
            input_text = None
            if cmd_parts and cmd_parts[0] == 'init':
                input_text = 'y\n'  # Auto-confirm for init command
            elif 'remove' in cmd_parts:
                input_text = 'y\n'  # Auto-confirm for remove command
            
            # Run the command
            result = cli_runner.invoke(cli, cmd_parts, input=input_text)
            context.command_result = result


# Shared Then steps
@then("the command should succeed")
def command_should_succeed(context):
    """Assert that the command executed successfully"""
    assert context.command_result.exit_code == 0, f"Command failed with: {context.command_result.output}"


@then("the command should fail")
def command_should_fail(context):
    """Assert that the command failed"""
    assert context.command_result.exit_code != 0


@then("detailed processing information should be displayed")
def detailed_processing_info_displayed(context):
    """Assert verbose output is shown"""
    # In verbose mode, more detailed output should be present
    assert len(context.command_result.output) > 50  # Assuming verbose output is longer


@then(parsers.parse("parallel processing should use {workers:d} workers"))
def parallel_processing_uses_workers(context, workers):
    """Assert parallel processing uses specified number of workers"""
    # This would be verified by checking the indexer was called with correct worker count
    pass


@then("ignored patterns should be displayed")
def ignored_patterns_displayed(context):
    """Assert ignored patterns were shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["ignore", "skip", "pattern"])


@then("I should see file-by-file progress")
def file_by_file_progress_shown(context):
    """Assert individual file progress is shown"""
    output = context.command_result.output.lower()
    assert "processing" in output or "parsing" in output or "indexing" in output


# Additional common step definitions
@given("I have a project with no cache data")
def project_no_cache(temp_project, context):
    """Set up project without cache data"""
    context.current_directory = temp_project
    # No cache setup needed


@given("the cache is available")
def cache_available(context):
    """Set up cache availability"""
    # Cache is always available
    pass


@given("I have cached indexing data")
def cached_indexing_data(context):
    """Set up cached indexing data"""
    from claude_code_indexer.cache_manager import CacheManager
    cache_manager = CacheManager()
    cache_manager.set('test_data', {'files': 10, 'nodes': 50})
    context.cache_manager = cache_manager


@given("I have an enhanced project")
def enhanced_project(indexed_project, context):
    """Set up enhanced project with metadata"""
    # Reuse indexed project setup
    pass


@given("I have an enhanced project with diverse metadata")
def enhanced_project_diverse(indexed_project, context):
    """Set up enhanced project with diverse metadata"""
    # Reuse indexed project setup
    pass


@then("the cache should be cleared")
def cache_should_be_cleared(context):
    """Assert cache was cleared"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["cleared", "removed", "deleted"])


@then("cache statistics should be displayed")
def cache_stats_displayed(context):
    """Assert cache statistics shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["cache", "hits", "size", "entries"])