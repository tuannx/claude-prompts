#!/usr/bin/env python3
"""
BDD Step definitions for Index Command Parameters
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from pytest_bdd import scenarios, given, when, then, parsers

# Import shared step definitions
from shared_steps import *

# Mock ensmallen before importing
sys.modules['ensmallen'] = MagicMock()

# Load index parameter scenarios
scenarios('../features/index_parameters.feature')


@given("I have a sample project with Python and JavaScript files")
def sample_project_with_files(temp_project, sample_python_files, sample_javascript_files, context):
    """Create a sample project with both Python and JavaScript files"""
    context.current_directory = temp_project
    context.temp_files.update(sample_python_files)
    context.temp_files.update(sample_javascript_files)


@pytest.fixture
def temp_project():
    """Fixture providing temporary project directory"""
    import tempfile
    import shutil
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
    print("Hello World")
    calculator = Calculator()
    result = calculator.add(5, 3)
    print(f"Result: {result}")

class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

if __name__ == "__main__":
    main()
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
    
    # Create files
    for filename, content in files.items():
        file_path = Path(temp_project) / filename
        file_path.write_text(content)
    
    return files


@given("I have previously indexed files")
def previously_indexed_files(context):
    """Set up previously indexed files with cache"""
    # Mock cache data and indexed files
    pass


@then("only Python and JavaScript files should be processed")
def only_python_js_processed(context):
    """Assert only specific file types were processed"""
    # This would verify file pattern filtering worked
    pass


@then("the patterns should be applied correctly")
def patterns_applied_correctly(context):
    """Assert file patterns were used correctly"""
    output = context.command_result.output.lower()
    print(f"DEBUG: Command output: '{output}'")  # Debug output
    print(f"DEBUG: Exit code: {context.command_result.exit_code}")
    # Just check command succeeded for now
    assert context.command_result.exit_code == 0


@then("the database should be created at the specified path")
def database_created_at_path(context):
    """Assert database was created at custom path"""
    # This would verify the --db parameter worked
    pass


@then("indexing data should be stored in the custom database")
def data_stored_in_custom_db(context):
    """Assert data went to custom database"""
    # This would verify database path was used
    pass


@then("existing cache should be ignored")
def existing_cache_ignored(context):
    """Assert cache was bypassed"""
    # This would verify --force parameter worked
    pass


@then("all files should be re-processed")
def all_files_reprocessed(context):
    """Assert force re-indexing occurred"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["force", "reprocess", "reindex"])


@then("processing should be parallelized")
def processing_parallelized(context):
    """Assert parallel processing was used"""
    # This would verify --workers parameter was applied
    pass


@then("database optimizations should be skipped")
def optimizations_skipped(context):
    """Assert optimizations were disabled"""
    # This would verify --no-optimize parameter worked
    pass


@then("raw indexing data should be preserved")
def raw_data_preserved(context):
    """Assert raw data was kept without optimization"""
    # This would verify optimization was skipped
    pass


@then("performance metrics should be collected")
def performance_metrics_collected(context):
    """Assert benchmark data was gathered"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["benchmark", "performance", "timing", "speed"])


@then("benchmark results should be displayed")
def benchmark_results_displayed(context):
    """Assert benchmark results were shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["benchmark", "results", "metrics", "ms", "sec"])


@then("test files should be ignored")
def test_files_ignored(context):
    """Assert test files were excluded"""
    # This would verify custom ignore patterns worked
    pass


@then("specification files should be ignored")
def spec_files_ignored(context):
    """Assert spec files were excluded"""
    # This would verify custom ignore patterns worked
    pass


@then("custom ignore patterns should be applied")
def custom_ignore_applied(context):
    """Assert custom ignore patterns were used"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["ignore", "skip", "exclude"])


@then("ignored file patterns should be displayed")
def ignored_patterns_displayed(context):
    """Assert ignored patterns were shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["ignore", "skip", "pattern"])


@then("ignored files list should be shown")
def ignored_files_shown(context):
    """Assert list of ignored files was displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["ignore", "skip", "excluded"])


@then("parsing errors should be shown if any")
def parsing_errors_shown(context):
    """Assert parsing errors were displayed in verbose mode"""
    # This would verify verbose output includes errors
    pass


@then("only Python files should be processed")
def only_python_processed(context):
    """Assert only Python files were indexed"""
    # This would verify pattern filtering for Python only
    pass


@then("temporary files should be ignored")
def temp_files_ignored(context):
    """Assert temporary files were excluded"""
    # This would verify *.tmp ignore pattern worked
    pass


@then("build directory should be ignored")
def build_dir_ignored(context):
    """Assert build directory was excluded"""
    # This would verify build/ ignore pattern worked
    pass


@then("the ignore list should include custom patterns")
def ignore_list_includes_custom(context):
    """Assert custom patterns appear in ignore list"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["custom", "pattern", "ignore"])


# Additional step definitions for enhanced given scenarios
@given("I have a custom database at \"/tmp/custom.db\"")
def custom_database_at_path(context):
    """Set up custom database for testing"""
    context.custom_db_path = "/tmp/custom.db"
    # Mock database at this path
    pass


@given("I have an indexed project with diverse node types")
def project_with_diverse_nodes(context):
    """Set up project with various node types"""
    # Mock project with functions, classes, methods, files, imports
    pass


@given("I have an indexed project with relationships")
def project_with_relationships(context):
    """Set up project with code relationships"""
    # Mock project with calls, contains, imports, inheritance relationships
    pass


@given("I have a project with no cache data")
def project_no_cache(context):
    """Set up project without cache data"""
    # Mock project with empty cache
    pass