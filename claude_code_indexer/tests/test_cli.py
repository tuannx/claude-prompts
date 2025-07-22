#!/usr/bin/env python3
"""
Comprehensive tests for CLI module
Goal: Increase coverage from 20% to 80%+
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from click.testing import CliRunner
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock ensmallen before importing to avoid logger conflicts
sys.modules['ensmallen'] = MagicMock()

from claude_code_indexer.cli import cli, show_app_header, console
from claude_code_indexer import __version__, __app_name__


class TestCLI:
    """Test suite for CLI commands"""
    
    @pytest.fixture
    def runner(self):
        """Create CLI test runner"""
        return CliRunner()
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_indexer(self):
        """Mock CodeGraphIndexer"""
        with patch('claude_code_indexer.cli.CodeGraphIndexer') as mock:
            yield mock
    
    def test_cli_version(self, runner):
        """Test version command"""
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert __version__ in result.output
        assert __app_name__ in result.output
    
    def test_cli_help(self, runner):
        """Test help command"""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Claude Code Indexer' in result.output
        assert 'Index source code as graph database' in result.output
    
    def test_show_app_header(self):
        """Test app header display"""
        with patch.object(console, 'print') as mock_print:
            show_app_header()
            
            # Verify header was printed
            calls = mock_print.call_args_list
            assert len(calls) >= 2
            assert __app_name__ in str(calls[0])
            assert __version__ in str(calls[0])
    
    def test_init_command_new_project(self, runner, temp_dir):
        """Test init command in new project"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Create template file
            template_dir = Path(__file__).parent.parent / "claude_code_indexer" / "templates"
            template_dir.mkdir(exist_ok=True)
            template_file = template_dir / "claude_md_template.md"
            template_file.write_text("## Code Indexing with Graph Database\nTemplate content")
            
            # Provide 'y' input for confirmation
            result = runner.invoke(cli, ['init'], input='y\n')
            
            assert result.exit_code == 0
            assert "Initializing project" in result.output
            assert Path("CLAUDE.md").exists()
            
            # Check CLAUDE.md content
            with open("CLAUDE.md") as f:
                content = f.read()
                assert "Code Indexing with Graph Database" in content
    
    def test_init_command_existing_file(self, runner, temp_dir):
        """Test init command with existing CLAUDE.md"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Create existing CLAUDE.md
            existing_content = "# Existing Content\n\n## Code Indexing with Graph Database\nExisting section"
            Path("CLAUDE.md").write_text(existing_content)
            
            # Create template
            template_dir = Path(__file__).parent.parent / "claude_code_indexer" / "templates"
            template_dir.mkdir(exist_ok=True)
            template_file = template_dir / "claude_md_template.md"
            template_file.write_text("## Code Indexing with Graph Database\nNew template")
            
            result = runner.invoke(cli, ['init'])
            
            assert result.exit_code == 0
            assert "Code indexing section already exists" in result.output
    
    def test_init_command_force(self, runner, temp_dir):
        """Test init command with --force flag"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Create existing CLAUDE.md
            existing_content = "# Existing\n\n## Code Indexing with Graph Database\nOld\n\n## Other Section\nKeep this"
            Path("CLAUDE.md").write_text(existing_content)
            
            # Create template
            template_dir = Path(__file__).parent.parent / "claude_code_indexer" / "templates"
            template_dir.mkdir(exist_ok=True)
            template_file = template_dir / "claude_md_template.md"
            template_file.write_text("## Code Indexing with Graph Database\nNew template")
            
            result = runner.invoke(cli, ['init', '--force'])
            
            assert result.exit_code == 0
            assert "Updating existing section" in result.output
            
            # Check content was updated
            with open("CLAUDE.md") as f:
                content = f.read()
                assert "New template" in content
                assert "Keep this" in content
    
    def test_index_command_basic(self, runner, temp_dir, mock_indexer):
        """Test basic index command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Create test files
            Path("test.py").write_text("def hello(): pass")
            
            # Mock indexer behavior
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.index_directory.return_value = True
            
            result = runner.invoke(cli, ['index', '.'])
            
            assert result.exit_code == 0
            mock_instance.index_directory.assert_called_once()
    
    def test_index_command_with_options(self, runner, temp_dir, mock_indexer):
        """Test index command with various options"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            Path("test.py").write_text("def hello(): pass")
            
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.index_directory.return_value = True
            
            result = runner.invoke(cli, ['index', '.', '--verbose', '--no-cache', '--workers', '2'])
            
            assert result.exit_code == 0
            mock_indexer.assert_called_with(
                use_cache=False,
                parallel_workers=2,
                project_path=Path('.')
            )
    
    def test_query_command(self, runner, temp_dir, mock_indexer):
        """Test query command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Mock storage manager
            with patch('claude_code_indexer.cli.get_storage_manager') as mock_storage:
                mock_storage.return_value.get_project_from_path.return_value = Path('.')
                mock_storage.return_value.get_database_path.return_value = Path('test.db')
                
                # Create mock database
                import sqlite3
                conn = sqlite3.connect('test.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE code_nodes (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    node_type TEXT,
                    path TEXT,
                    importance_score REAL
                )''')
                cursor.execute("INSERT INTO code_nodes VALUES (1, 'test_func', 'function', 'test.py', 0.8)")
                conn.commit()
                conn.close()
                
                result = runner.invoke(cli, ['query'])
                
                assert result.exit_code == 0
                assert 'test_func' in result.output
    
    def test_query_important_command(self, runner, temp_dir):
        """Test query --important command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            with patch('claude_code_indexer.cli.get_storage_manager') as mock_storage:
                mock_storage.return_value.get_project_from_path.return_value = Path('.')
                mock_storage.return_value.get_database_path.return_value = Path('test.db')
                
                # Create mock database with important nodes
                import sqlite3
                conn = sqlite3.connect('test.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE code_nodes (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    node_type TEXT,
                    path TEXT,
                    importance_score REAL,
                    relevance_tags TEXT
                )''')
                cursor.execute("INSERT INTO code_nodes VALUES (1, 'important_func', 'function', 'test.py', 0.9, 'highly-used')")
                cursor.execute("INSERT INTO code_nodes VALUES (2, 'normal_func', 'function', 'test.py', 0.3, '')")
                conn.commit()
                conn.close()
                
                result = runner.invoke(cli, ['query', '--important'])
                
                assert result.exit_code == 0
                assert 'important_func' in result.output
    
    def test_search_command(self, runner, temp_dir):
        """Test search command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            with patch('claude_code_indexer.cli.get_storage_manager') as mock_storage:
                mock_storage.return_value.get_project_from_path.return_value = Path('.')
                mock_storage.return_value.get_database_path.return_value = Path('test.db')
                
                # Create mock database
                import sqlite3
                conn = sqlite3.connect('test.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE code_nodes (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    node_type TEXT,
                    path TEXT,
                    summary TEXT
                )''')
                cursor.execute("INSERT INTO code_nodes VALUES (1, 'search_test', 'function', 'test.py', 'Function for testing search')")
                conn.commit()
                conn.close()
                
                result = runner.invoke(cli, ['search', 'test'])
                
                assert result.exit_code == 0
                assert 'search_test' in result.output
    
    def test_stats_command(self, runner, temp_dir):
        """Test stats command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            with patch('claude_code_indexer.cli.get_storage_manager') as mock_storage:
                mock_storage.return_value.get_project_from_path.return_value = Path('.')
                mock_storage.return_value.get_database_path.return_value = Path('test.db')
                
                # Create mock database
                import sqlite3
                conn = sqlite3.connect('test.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE code_nodes (
                    id INTEGER PRIMARY KEY,
                    node_type TEXT,
                    language TEXT
                )''')
                cursor.execute('''CREATE TABLE relationships (
                    source_id INTEGER,
                    target_id INTEGER,
                    relationship_type TEXT
                )''')
                cursor.execute("INSERT INTO code_nodes VALUES (1, 'function', 'python')")
                cursor.execute("INSERT INTO code_nodes VALUES (2, 'class', 'python')")
                cursor.execute("INSERT INTO relationships VALUES (1, 2, 'calls')")
                conn.commit()
                conn.close()
                
                result = runner.invoke(cli, ['stats'])
                
                assert result.exit_code == 0
                assert 'Total Nodes: 2' in result.output
                assert 'Total Edges: 1' in result.output
    
    def test_enhance_command(self, runner, temp_dir, mock_indexer):
        """Test enhance command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.enhance_with_llm_metadata.return_value = None
            
            result = runner.invoke(cli, ['enhance', '.', '--sample', '10'])
            
            assert result.exit_code == 0
            mock_instance.enhance_with_llm_metadata.assert_called_with(sample_size=10)
    
    def test_projects_command(self, runner):
        """Test projects command"""
        with patch('claude_code_indexer.cli.get_storage_manager') as mock_storage:
            mock_storage.return_value.list_projects.return_value = [
                {'path': '/project1', 'db_size': 1024000, 'last_indexed': '2024-01-01'},
                {'path': '/project2', 'db_size': 2048000, 'last_indexed': '2024-01-02'}
            ]
            
            result = runner.invoke(cli, ['projects'])
            
            assert result.exit_code == 0
            assert '/project1' in result.output
            assert '/project2' in result.output
    
    def test_cache_command(self, runner):
        """Test cache command"""
        result = runner.invoke(cli, ['cache'])
        assert result.exit_code == 0
        assert 'cache' in result.output.lower()
    
    def test_cache_stats_command(self, runner):
        """Test cache stats command"""
        with patch('claude_code_indexer.cli.CacheManager') as mock_cache:
            mock_instance = Mock()
            mock_cache.return_value = mock_instance
            mock_instance.get_cache_stats.return_value = {
                'hits': 100,
                'misses': 20,
                'size': 1024000,
                'entries': 50
            }
            
            result = runner.invoke(cli, ['cache', 'stats'])
            
            assert result.exit_code == 0
            assert 'hits' in result.output.lower()
    
    def test_clean_command(self, runner, temp_dir):
        """Test clean command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Create test database
            Path('test.db').write_text('dummy')
            
            with patch('claude_code_indexer.cli.get_storage_manager') as mock_storage:
                mock_storage.return_value.get_project_from_path.return_value = Path('.')
                mock_storage.return_value.get_database_path.return_value = Path('test.db')
                
                # User confirms deletion
                result = runner.invoke(cli, ['clean'], input='y\n')
                
                assert result.exit_code == 0
                assert not Path('test.db').exists()
    
    def test_remove_command(self, runner):
        """Test remove command"""
        with patch('claude_code_indexer.cli.get_storage_manager') as mock_storage:
            mock_instance = mock_storage.return_value
            mock_instance.get_project_path.return_value = Path('/test/project')
            mock_instance.remove_project.return_value = True
            
            result = runner.invoke(cli, ['remove', '/test/project'], input='y\n')
            
            assert result.exit_code == 0
            mock_instance.remove_project.assert_called_with(Path('/test/project'))
    
    def test_background_command(self, runner):
        """Test background command group"""
        result = runner.invoke(cli, ['background'])
        assert result.exit_code == 0
        assert 'background' in result.output.lower()
    
    def test_background_status_command(self, runner):
        """Test background status command"""
        with patch('claude_code_indexer.cli.BackgroundIndexingService') as mock_service:
            mock_instance = Mock()
            mock_service.return_value = mock_instance
            mock_instance.get_status.return_value = {
                'enabled': True,
                'running': True,
                'projects': ['/project1', '/project2']
            }
            
            result = runner.invoke(cli, ['background', 'status'])
            
            assert result.exit_code == 0
            assert 'enabled' in result.output.lower()
    
    def test_mcp_command(self, runner):
        """Test mcp command group"""
        result = runner.invoke(cli, ['mcp'])
        assert result.exit_code == 0
        assert 'mcp' in result.output.lower()
    
    def test_mcp_install_command(self, runner):
        """Test mcp install command"""
        with patch('claude_code_indexer.cli.MCPInstaller') as mock_installer:
            mock_instance = Mock()
            mock_installer.return_value = mock_instance
            mock_instance.install.return_value = True
            
            result = runner.invoke(cli, ['mcp', 'install'])
            
            assert result.exit_code == 0
            mock_instance.install.assert_called_once()
    
    def test_llm_guide_command(self, runner):
        """Test llm-guide command"""
        result = runner.invoke(cli, ['llm-guide'])
        
        assert result.exit_code == 0
        assert 'LLM Guide' in result.output
        assert 'claude-code-indexer' in result.output
    
    def test_benchmark_command(self, runner, temp_dir, mock_indexer):
        """Test benchmark command"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Create test files
            for i in range(5):
                Path(f"test{i}.py").write_text(f"def func{i}(): pass")
            
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.index_directory.return_value = True
            
            result = runner.invoke(cli, ['benchmark', '.'])
            
            assert result.exit_code == 0
            assert 'Benchmark Results' in result.output
    
    def test_update_command(self, runner):
        """Test update command"""
        with patch('claude_code_indexer.cli.Updater') as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance
            mock_instance.check_for_updates.return_value = ('1.2.0', '1.1.0')
            
            # Test check only
            result = runner.invoke(cli, ['update', '--check'])
            
            assert result.exit_code == 0
            assert 'newer version' in result.output.lower()
            
            # Test actual update
            mock_instance.update_package.return_value = True
            result = runner.invoke(cli, ['update'], input='y\n')
            
            assert result.exit_code == 0
            mock_instance.update_package.assert_called_once()
    
    def test_error_handling(self, runner, temp_dir):
        """Test error handling in CLI"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Test invalid path
            result = runner.invoke(cli, ['index', '/nonexistent/path'])
            
            assert result.exit_code != 0
            
            # Test security error
            with patch('claude_code_indexer.cli.validate_file_path') as mock_validate:
                mock_validate.side_effect = SecurityError("Invalid path")
                
                result = runner.invoke(cli, ['index', '../../../etc/passwd'])
                
                assert result.exit_code != 0
    
    def test_verbose_output(self, runner, temp_dir, mock_indexer):
        """Test verbose output flag"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            Path("test.py").write_text("def hello(): pass")
            
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.index_directory.return_value = True
            
            result = runner.invoke(cli, ['index', '.', '--verbose'])
            
            assert result.exit_code == 0
            # Should have more detailed output
    
    def test_parallel_workers_validation(self, runner, temp_dir, mock_indexer):
        """Test parallel workers validation"""
        with runner.isolated_filesystem(temp_dir=temp_dir):
            # Test invalid worker count
            result = runner.invoke(cli, ['index', '.', '--workers', '0'])
            
            assert result.exit_code != 0
            
            # Test valid worker count
            mock_instance = Mock()
            mock_indexer.return_value = mock_instance
            mock_instance.index_directory.return_value = True
            
            result = runner.invoke(cli, ['index', '.', '--workers', '4'])
            
            assert result.exit_code == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])