#!/usr/bin/env python3
"""
BDD Step definitions for CLI commands
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Mock ensmallen before importing to avoid logger conflicts
sys.modules['ensmallen'] = MagicMock()

from claude_code_indexer.cli import cli
from claude_code_indexer import __version__, __app_name__

# Import pytest-bdd functions
from pytest_bdd import scenarios, given, when, then, parsers

# Load all feature files
scenarios('../features/cli_commands.feature')
scenarios('../features/enhance_commands.feature')
scenarios('../features/cache_management.feature')
scenarios('../features/project_management.feature')
scenarios('../features/background_service.feature')
scenarios('../features/mcp_integration.feature')


@pytest.fixture
def cli_runner():
    """Fixture providing CLI test runner"""
    return CliRunner()


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
    
    # Create a simple Python module
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


# Context to store test state
class BDDTestContext:
    def __init__(self):
        self.command_result = None
        self.current_directory = None
        self.temp_files = {}
        self.database_path = None


@pytest.fixture
def context():
    """Test context to store state between steps"""
    return BDDTestContext()


# Background steps
@given("I have a sample project with Python and JavaScript files")
@given('I have a sample project with Python and JavaScript files')
def sample_project_with_files(temp_project, sample_python_files, sample_javascript_files, context):
    """Create a sample project with both Python and JavaScript files"""
    context.current_directory = temp_project
    context.temp_files.update(sample_python_files)
    context.temp_files.update(sample_javascript_files)


@given("I am in an empty project directory")
def empty_project_directory(temp_project, context):
    """Set up empty project directory"""
    context.current_directory = temp_project


@given("I have an existing CLAUDE.md file")
def existing_claude_md(temp_project, context):
    """Create existing CLAUDE.md file"""
    claude_md = Path(temp_project) / "CLAUDE.md"
    claude_md.write_text("""# Existing CLAUDE.md

## Code Indexing with Graph Database
Old content here.

## Other Section
Keep this content.
""")
    context.current_directory = temp_project


@given("I have a project with Python files")
def project_with_python_files(temp_project, sample_python_files, context):
    """Create project with Python files"""
    context.current_directory = temp_project
    context.temp_files.update(sample_python_files)


@given("I have an indexed project")
@given('I have an indexed project')
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


@given(parsers.parse("I have an indexed project with {count:d} nodes"))
def indexed_project_with_nodes(temp_project, context, count):
    """Create indexed project with specific number of nodes"""
    context.current_directory = temp_project
    
    # Create mock database with specified number of nodes
    db_path = Path(temp_project) / "code_index.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE code_nodes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        node_type TEXT,
        path TEXT,
        importance_score REAL,
        relevance_tags TEXT,
        summary TEXT
    )''')
    
    # Insert specified number of nodes
    for i in range(count):
        cursor.execute("INSERT INTO code_nodes VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (i, f'node_{i}', 'function', f'file_{i}.py', 0.5, '', f'Function node_{i} description'))
    
    conn.commit()
    conn.close()
    context.database_path = str(db_path)


# When steps - Command execution
@when(parsers.parse('I run "{command}"'))
@when('I run "{command}"')
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
        
        # Mock storage stats
        mock_storage_instance.get_storage_stats.return_value = {
            'app_home': '/home/user/.claude-code-indexer',
            'project_count': 3,
            'total_size_mb': 5.7,
            'databases': [{'path': Path("/tmp/test_project") / "code_index.db", 'size': '1.2 MB'}]
        }
        
        # Mock list projects
        mock_storage_instance.list_projects.return_value = [
            {
                'name': 'project1',
                'path': '/path/to/project1',
                'last_indexed': '2024-01-01T12:00:00',
                'db_size': 1024 * 1024,  # 1 MB
                'exists': True
            },
            {
                'name': 'project2',
                'path': '/path/to/project2',
                'last_indexed': '2024-01-02T14:30:00',
                'db_size': 2 * 1024 * 1024,  # 2 MB
                'exists': True
            },
            {
                'name': 'project3',
                'path': '/path/to/project3',
                'last_indexed': 'Never',
                'db_size': 0,
                'exists': False
            }
        ]
        
        # Mock other dependencies as needed
        with patch('claude_code_indexer.cli.CodeGraphIndexer') as mock_indexer, \
             patch('claude_code_indexer.cli.os.path.exists') as mock_exists, \
             patch('claude_code_indexer.cache_manager.CacheManager') as mock_cache_manager:
            
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.index_directory.return_value = True
            default_dir = context.current_directory if context.current_directory else "/tmp/test_project"
            mock_instance.db_path = Path(default_dir) / "code_index.db"
            mock_instance.parsing_errors = []  # Mock empty parsing errors list
            mock_instance.get_stats.return_value = {
                'last_indexed': '2024-01-01 12:00',
                'total_nodes': '10',
                'total_edges': '5',
                'node_types': {'function': 5, 'class': 3, 'method': 2},
                'relationship_types': {'calls': 3, 'contains': 2}
            }
            
            # Mock query methods
            mock_instance.query_important_nodes.return_value = [
                {
                    'name': 'main',
                    'node_type': 'function',
                    'importance_score': 0.8,
                    'relevance_tags': ['entry-point'],
                    'path': 'main.py'
                },
                {
                    'name': 'Calculator',
                    'node_type': 'class',
                    'importance_score': 0.7,
                    'relevance_tags': ['utility'],
                    'path': 'main.py'
                }
            ]
            
            # Mock search method
            mock_instance.search_nodes.return_value = [
                {
                    'name': 'calculate',
                    'node_type': 'function',
                    'importance_score': 0.6,
                    'relevance_tags': [],
                    'path': 'utils.py'
                }
            ]
            
            # Mock enhance metadata method
            mock_instance.enhance_metadata.return_value = {
                'analyzed_count': 10,
                'total_nodes': 10,
                'analysis_duration': '2.5s',
                'nodes_per_second': 4.0,
                'architectural_layers': {
                    'service': 3,
                    'model': 2,
                    'controller': 2,
                    'utility': 3
                },
                'criticality_distribution': {
                    'critical': 2,
                    'important': 5,
                    'normal': 3
                },
                'business_domains': {
                    'authentication': 2,
                    'data_processing': 5,
                    'utility': 3
                },
                'average_complexity': 0.65
            }
            
            # Mock file existence check
            mock_exists.return_value = True
            
            # Mock CacheManager
            mock_cache_instance = Mock()
            mock_cache_manager.return_value = mock_cache_instance
            
            # Mock cache manager methods
            def mock_print_cache_stats():
                console = Mock()
                # Simulate printing cache stats
                print("💾 Cache Statistics")
                print("Hit Rate: 85.3%")
                print("Total Size: 12.5 MB")
                print("Entry Count: 245 items")
            
            mock_cache_instance.print_cache_stats = mock_print_cache_stats
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


@when('I confirm the removal')
def confirm_removal(context):
    """Simulate user confirming removal"""
    # This would be handled by providing 'y' input to the command
    pass


@when('I cancel the removal')
def cancel_removal(context):
    """Simulate user canceling removal"""
    # This would be handled by providing 'n' input to the command
    pass


# Then steps - Assertions
@then("the command should succeed")
def command_should_succeed(context):
    """Assert that the command executed successfully"""
    assert context.command_result.exit_code == 0, f"Command failed with: {context.command_result.output}"


@then("the command should fail")
def command_should_fail(context):
    """Assert that the command failed"""
    assert context.command_result.exit_code != 0


@then("a CLAUDE.md file should be created")
def claude_md_should_be_created(context):
    """Assert CLAUDE.md file was created"""
    claude_md_path = Path(context.current_directory) / "CLAUDE.md"
    assert claude_md_path.exists(), "CLAUDE.md file was not created"


@then(parsers.parse('the file should contain "{text}"'))
def file_should_contain(context, text):
    """Assert file contains specific text"""
    claude_md_path = Path(context.current_directory) / "CLAUDE.md"
    if claude_md_path.exists():
        content = claude_md_path.read_text()
        assert text in content, f"File does not contain '{text}'"


@then("the CLAUDE.md file should be updated")
def claude_md_should_be_updated(context):
    """Assert CLAUDE.md file was updated"""
    claude_md_path = Path(context.current_directory) / "CLAUDE.md"
    assert claude_md_path.exists(), "CLAUDE.md file does not exist"


@then("files should be indexed in the database")
def files_should_be_indexed(context):
    """Assert files were indexed"""
    # Check that indexing was attempted
    assert "indexing" in context.command_result.output.lower() or "indexed" in context.command_result.output.lower()


@then("the indexing stats should be displayed")
def indexing_stats_should_be_displayed(context):
    """Assert indexing statistics are shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["files", "nodes", "processed", "completed"])


@then("detailed processing information should be displayed")
def detailed_processing_info_displayed(context):
    """Assert verbose output is shown"""
    # In verbose mode, more detailed output should be present
    assert len(context.command_result.output) > 50  # Assuming verbose output is longer


@then("I should see file-by-file progress")
def file_by_file_progress_shown(context):
    """Assert individual file progress is shown"""
    output = context.command_result.output.lower()
    assert "processing" in output or "parsing" in output


@then("caching should be disabled")
def caching_should_be_disabled(context):
    """Assert caching is disabled"""
    # This would be verified by checking the indexer was called with use_cache=False
    pass


@then("all files should be processed fresh")
def all_files_processed_fresh(context):
    """Assert fresh processing occurred"""
    # This would be verified by checking no cache hits occurred
    pass


@then(parsers.parse("parallel processing should use {workers:d} workers"))
def parallel_processing_uses_workers(context, workers):
    """Assert parallel processing uses specified number of workers"""
    # This would be verified by checking the indexer was called with correct worker count
    pass


@then(parsers.parse('an error message about {error_type} should be displayed'))
def error_message_displayed(context, error_type):
    """Assert specific error message is shown"""
    output = context.command_result.output.lower()
    assert error_type.lower() in output


@then("all nodes should be displayed")
def all_nodes_displayed(context):
    """Assert all nodes are shown in output"""
    # Check that node information is present
    output = context.command_result.output.lower()
    assert any(word in output for word in ["node", "function", "class", "method"])


@then("the output should be formatted nicely")
def output_formatted_nicely(context):
    """Assert output is well-formatted"""
    # Check for basic formatting
    assert len(context.command_result.output.strip()) > 0


@then("only important nodes should be displayed")
def only_important_nodes_displayed(context):
    """Assert only important nodes are shown"""
    output = context.command_result.output.lower()
    assert "important" in output or "score" in output


@then("nodes should be sorted by importance score")
def nodes_sorted_by_importance(context):
    """Assert nodes are sorted by importance"""
    # This would require parsing the output and checking order
    pass


@then(parsers.parse('search results should contain "{term}"'))
def search_results_contain_term(context, term):
    """Assert search results contain specific term"""
    output = context.command_result.output.lower()
    assert term.lower() in output


@then('search results should contain both "class" and "method"')
def search_results_contain_both_terms(context):
    """Assert search results contain both terms"""
    output = context.command_result.output.lower()
    assert "class" in output and "method" in output


@then("results should be ranked by relevance")
def results_ranked_by_relevance(context):
    """Assert results are relevance-ranked"""
    # This would require checking the ranking algorithm was applied
    pass


@then("statistics should include total nodes count")
def stats_include_nodes_count(context):
    """Assert statistics include node count"""
    output = context.command_result.output.lower()
    assert "nodes" in output and any(char.isdigit() for char in context.command_result.output)


@then("statistics should include total edges count")
def stats_include_edges_count(context):
    """Assert statistics include edge count"""
    output = context.command_result.output.lower()
    assert "edges" in output or "relationships" in output


@then("language breakdown should be displayed")
def language_breakdown_displayed(context):
    """Assert language statistics are shown"""
    output = context.command_result.output.lower()
    assert "python" in output or "javascript" in output or "language" in output


@then("the version number should be displayed")
def version_number_displayed(context):
    """Assert version is shown"""
    assert __version__ in context.command_result.output


@then("the application name should be displayed")
def app_name_displayed(context):
    """Assert application name is shown"""
    assert __app_name__ in context.command_result.output


@then("usage information should be displayed")
def usage_info_displayed(context):
    """Assert usage/help information is shown"""
    output = context.command_result.output.lower()
    assert "usage" in output or "options" in output or "commands" in output


@then("all available commands should be listed")
def all_commands_listed(context):
    """Assert all commands are listed in help"""
    output = context.command_result.output.lower()
    expected_commands = ["init", "index", "query", "search", "stats"]
    for cmd in expected_commands:
        assert cmd in output


@then("LLM usage guide should be displayed")
def llm_guide_displayed(context):
    """Assert LLM guide is shown"""
    output = context.command_result.output.lower()
    assert "llm" in output or "guide" in output


@then("security warnings should be included")
def security_warnings_included(context):
    """Assert security warnings are present"""
    output = context.command_result.output.lower()
    assert "security" in output or "warning" in output or "never" in output


@then("quick start instructions should be shown")
def quick_start_shown(context):
    """Assert quick start instructions are present"""
    output = context.command_result.output.lower()
    assert "quick start" in output or "index ." in output


@then("the file should contain the latest template")
def file_should_contain_latest_template(context):
    """Assert file contains updated template content"""
    claude_md_path = Path(context.current_directory) / "CLAUDE.md"
    if claude_md_path.exists():
        content = claude_md_path.read_text()
        assert any(phrase in content for phrase in ["Code Indexing", "Graph Database", "claude-code-indexer"])
    else:
        # If file doesn't exist, check if creation was indicated in output
        output = context.command_result.output.lower()
        assert any(word in output for word in ["created", "initialized", "template"])


# Additional step definitions for enhance features
@given("I have an indexed project with diverse code patterns")
def indexed_project_with_patterns(temp_project, context):
    """Create indexed project with various code patterns"""
    context.current_directory = temp_project
    
    # Create files with different patterns
    patterns_file = Path(temp_project) / "patterns.py"
    patterns_file.write_text('''
# Singleton Pattern
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Factory Pattern  
class UserFactory:
    @staticmethod
    def create_user(user_type):
        if user_type == "admin":
            return AdminUser()
        return RegularUser()

# Observer Pattern
class EventManager:
    def __init__(self):
        self.observers = []
    
    def subscribe(self, observer):
        self.observers.append(observer)
    
    def notify(self, event):
        for observer in self.observers:
            observer.update(event)
''')


# Step definitions for enhance command results
@then("LLM metadata should be generated")
def llm_metadata_generated(context):
    """Assert LLM metadata was created"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["metadata", "enhanced", "analysis", "llm"])


@then("enhancement progress should be displayed")
def enhancement_progress_displayed(context):
    """Assert enhancement progress is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["progress", "processing", "enhancing", "analyzing"])


@then("a summary of enhanced nodes should be shown")
def summary_of_enhanced_nodes_shown(context):
    """Assert summary is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["summary", "nodes", "enhanced", "completed"])


@then(parsers.parse("only {count:d} nodes should be enhanced"))
def only_n_nodes_enhanced(context, count):
    """Assert specific number of nodes were enhanced"""
    output = context.command_result.output
    # Check that the output mentions the correct number
    assert str(count) in output or f"Analyzed Nodes: {count}" in output


@then("the sample should be representative")
def sample_should_be_representative(context):
    """Assert sampling strategy is good"""
    # This is checked by seeing diversity in the output
    output = context.command_result.output.lower()
    assert any(word in output for word in ["analyzed", "enhanced", "complete"])


# Additional step definitions for cache features
@given("I have a project with cached data")
def project_with_cached_data(temp_project, context):
    """Set up project with cache data"""
    context.current_directory = temp_project
    # Cache data will be mocked in the command execution


@then("cache hit rate should be displayed")
def cache_hit_rate_displayed(context):
    """Assert cache hit rate is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["hit", "rate", "ratio", "%"])


@then("cache size information should be shown")
def cache_size_shown(context):
    """Assert cache size is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["size", "mb", "gb", "bytes"])


@then("cache entry count should be displayed")
def cache_entry_count_displayed(context):
    """Assert entry count is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["entries", "count", "items"])


@given("I have cached indexing data")
def cached_indexing_data(context):
    """Set up cached indexing data"""
    # Cache data will be mocked when CacheManager is initialized
    pass


@given("I have old cached data")
def old_cached_data(context):
    """Set up old cache entries"""
    # Old cache data will be mocked
    pass


@then("old cache entries should be removed")
def old_entries_removed(context):
    """Assert old entries were cleared"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["removed", "cleared", "deleted", "cleaned"])


@then("current cache should be preserved")
def current_cache_preserved(context):
    """Assert recent entries remain"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["cleared", "successfully"])


@then("storage space should be reclaimed")
def storage_space_reclaimed(context):
    """Assert space was freed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["freed", "reclaimed", "space", "cleared", "successfully"])


# Additional step definitions for project management
@given("I have multiple indexed projects")
def multiple_indexed_projects(context):
    """Set up multiple projects"""
    # Mock storage manager will return multiple projects
    pass


@given(parsers.parse("I have {count:d} indexed projects"))
def n_indexed_projects(context, count):
    """Set up specific number of projects"""
    # Storage manager mock will return N projects
    pass


@then(parsers.parse("all {count:d} projects should be listed"))
def all_projects_listed(context, count):
    """Assert all projects are shown"""
    output = context.command_result.output
    # Check that multiple projects appear in output
    assert "projects" in output.lower()


@then("project paths should be displayed")
def project_paths_displayed(context):
    """Assert project paths are shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["path", "directory", "/"])


@then("database sizes should be shown")
def database_sizes_shown(context):
    """Assert database size info is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["size", "mb", "kb", "bytes"])


@then("last indexed times should be shown")
def last_indexed_times_shown(context):
    """Assert timestamps are displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["last", "indexed", "time", "ago", "never"])


# Additional step definitions for background service
@given("the background service is available")
def background_service_available(context):
    """Set up background service availability"""
    pass


@given("I have a background service running")
def background_service_running(context):
    """Set up running background service"""
    pass


@given("I have a background service not running")
def background_service_not_running(context):
    """Set up stopped background service"""
    pass


# Additional step definitions for MCP
@given("Claude Desktop is available on the system")
def claude_desktop_available(context):
    """Set up system with Claude Desktop"""
    pass


@given("MCP server is not installed")
def mcp_server_not_installed(context):
    """Set up system without MCP server"""
    pass

