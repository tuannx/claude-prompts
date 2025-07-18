# Claude Code Indexer

A powerful code indexing tool that uses graph databases to analyze and understand code structure. Built specifically for Claude Code assistant workflows.

## Features

- 📊 **Graph-based code analysis** using Ensmallen library
- 🔍 **Intelligent node ranking** based on importance and centrality
- 💾 **SQLite database** for persistent storage
- 🎯 **Relevance tagging** for different code entity types
- 📈 **Network analysis** with PageRank and centrality measures
- 🚀 **Easy CLI interface** for quick setup and usage
- 🤖 **MCP Integration** for direct Claude Desktop support (v1.3.0+)
- 🔬 **Multi-keyword search** with AND/OR logic (v1.3.0+)
- 📂 **Project-based indexing** for MCP with separate databases (v1.4.0+)
- 🚫 **Smart ignore patterns** - auto-ignores node_modules, .git, etc (v1.5.0+)
- 📝 **Respects .gitignore** and .dockerignore files (v1.5.0+)
- 🌐 **Multi-language support** - Python, JavaScript, TypeScript (v1.6.0+), Java (v1.10.0+)
- 🏠 **Centralized storage** - All data in ~/.claude-code-indexer/ (v1.7.0+)

## Installation

### From PyPI (Recommended)

```bash
# Basic installation
pip install claude-code-indexer

# With MCP support for Claude Desktop
pip install 'claude-code-indexer[mcp]'
```

### From Source

```bash
git clone https://github.com/anthropics/claude-code-indexer.git
cd claude-code-indexer
pip install -e .
```

### Updating

The package includes auto-update functionality:

```bash
# Check for updates
claude-code-indexer update --check-only

# Update to latest version
claude-code-indexer update

# Sync CLAUDE.md with latest template
claude-code-indexer sync
```

Updates will also be checked automatically when you run any command.

## What's New in v1.5.0

### 🚫 Smart Ignore Patterns

The indexer now automatically ignores common non-source directories:
- **Dependencies**: node_modules/, vendor/, packages/, bower_components/
- **Build outputs**: build/, dist/, target/, *.egg-info/
- **Version control**: .git/, .svn/, .hg/
- **Python**: __pycache__/, *.pyc, venv/, .env/
- **IDE**: .idea/, .vscode/, *.swp
- **And many more...**

### 📝 .gitignore Support

Automatically respects patterns from:
- `.gitignore` - Git ignore patterns
- `.dockerignore` - Docker ignore patterns
- Custom patterns via CLI or MCP

## Quick Start

### 1. Initialize in your project

```bash
cd your-project
claude-code-indexer init
```

This will:
- Create or update your `CLAUDE.md` file with indexing instructions
- Initialize project in centralized storage (`~/.claude-code-indexer/`)
- No local database files created in your project

### 2. Index your codebase

```bash
# Index current directory
claude-code-indexer index .

# Index specific directory
claude-code-indexer index /path/to/your/code

# Index with custom patterns
claude-code-indexer index . --patterns "*.py,*.js,*.ts"

# Index with custom ignore patterns
claude-code-indexer index . --custom-ignore "tests/" --custom-ignore "*.test.py"

# See what will be ignored before indexing
claude-code-indexer index . --show-ignored
```

### 3. Query your code

```bash
# Show most important code entities
claude-code-indexer query --important

# Show all entities of specific type
claude-code-indexer query --type class

# Search for specific terms (single keyword)
claude-code-indexer search UserModel

# Search with multiple keywords (OR logic)
claude-code-indexer search auth user login

# Search with multiple keywords (AND logic - must match all)
claude-code-indexer search database connection --mode all

# View indexing statistics
claude-code-indexer stats
```

### 4. Manage projects

```bash
# List all indexed projects
claude-code-indexer projects

# Remove a project's index
claude-code-indexer remove project-name

# Clean up orphaned projects
claude-code-indexer clean

# Query a specific project
claude-code-indexer query --important --project /path/to/project
```

## CLI Commands

### `init`
Initialize Claude Code Indexer in current directory.

```bash
claude-code-indexer init [--force]
```

Options:
- `--force`: Overwrite existing configuration

### `index`
Index source code in specified directory.

```bash
claude-code-indexer index PATH [options]
```

Options:
- `--patterns`: File patterns to index (default: "*.py")
- `--db`: Database file path (default: centralized storage)
- `--force`: Force re-index all files (ignore cache)
- `--workers`: Number of parallel workers (default: auto)
- `--no-cache`: Disable caching
- `--custom-ignore`: Additional ignore patterns (can be used multiple times)
- `--show-ignored`: Show what patterns are being ignored

### `query`
Query indexed code entities.

```bash
claude-code-indexer query [options]
```

Options:
- `--important`: Show only important nodes
- `--type`: Filter by node type (file, class, method, function)
- `--limit`: Maximum number of results (default: 20)
- `--db`: Database file path (default: centralized storage)
- `--project`: Project name/path to query (default: current directory)

### `search`
Search for code entities by name. Supports multiple keywords.

```bash
claude-code-indexer search TERMS... [options]
```

Options:
- `--mode`: Search mode - 'any' (OR logic) or 'all' (AND logic) (default: 'any')
- `--limit`: Maximum number of results (default: 20)
- `--db`: Database file path

Examples:
```bash
# Single keyword
claude-code-indexer search auth

# Multiple keywords (match any)
claude-code-indexer search auth user login

# Multiple keywords (must match all)
claude-code-indexer search database connection --mode all
```

### `stats`
Show indexing statistics.

```bash
claude-code-indexer stats [options]
```

Options:
- `--db`: Database file path (default: centralized storage)
- `--cache`: Show cache statistics
- `--project`: Project name/path for stats (default: current directory)

### `projects`
List all indexed projects.

```bash
claude-code-indexer projects [--all]
```

Options:
- `--all`: Show all projects including non-existent

### `remove`
Remove an indexed project.

```bash
claude-code-indexer remove PROJECT [--force]
```

Options:
- `--force`: Force removal without confirmation

### `clean`
Clean up orphaned project indexes.

```bash
claude-code-indexer clean
```

### `background`
Manage background indexing service for automatic updates.

```bash
# Start the background service
claude-code-indexer background start

# Stop the background service
claude-code-indexer background stop

# Check service status
claude-code-indexer background status

# Set indexing interval for current project (in seconds)
claude-code-indexer background set-interval --interval 600  # 10 minutes

# Set default interval for all projects
claude-code-indexer background set-interval --interval 300  # 5 minutes (default)

# Disable background indexing for a project
claude-code-indexer background set-interval --project /path/to/project --interval -1

# Enable/disable the service globally
claude-code-indexer background config --enable
claude-code-indexer background config --disable
```

Background indexing automatically keeps your code indexes up-to-date:
- Default interval: 300 seconds (5 minutes)
- Configure per-project or global intervals
- Runs as a daemon process
- Only re-indexes when files have changed
- Set interval to -1 to disable for specific projects

## Database Schema

The tool creates a SQLite database with the following structure:

### code_nodes
Stores information about code entities.

```sql
CREATE TABLE code_nodes (
    id INTEGER PRIMARY KEY,
    node_type TEXT,           -- 'file', 'class', 'method', 'function', 'import'
    name TEXT,                -- Entity name
    path TEXT,                -- File path
    summary TEXT,             -- Description
    importance_score REAL,    -- 0.0 to 1.0
    relevance_tags TEXT,      -- JSON array of tags
    created_at TIMESTAMP
);
```

### relationships
Stores relationships between code entities.

```sql
CREATE TABLE relationships (
    source_id INTEGER,
    target_id INTEGER,
    relationship_type TEXT,   -- 'imports', 'contains', 'calls', 'inherits'
    weight REAL,
    created_at TIMESTAMP
);
```

## Integration with Claude Code

After running `claude-code-indexer init`, your `CLAUDE.md` file will include:

- Complete setup instructions
- Database schema documentation
- CLI command reference
- Usage examples for Claude Code workflows

## MCP Integration for Claude Desktop (v1.3.0+)

Direct integration with Claude Desktop using Model Context Protocol:

### Quick Setup

```bash
# Install with MCP support
pip install 'claude-code-indexer[mcp]'

# Auto-configure Claude Desktop
claude-code-indexer mcp install

# Check status
claude-code-indexer mcp status
```

### MCP Tools Available

Once installed, Claude Desktop can directly use:

#### Core Tools
- **index_codebase(project_path, workers=4, force=False, custom_ignore=[])**: Index Python projects
- **get_project_stats(project_path)**: View code statistics and overview
- **query_important_code(project_path, limit=20, node_type=None)**: Find important components
- **search_code(project_path, terms, limit=10, mode="any")**: Multi-keyword search
- **manage_cache(project_path, action, days=30)**: Control indexing cache

#### New in v1.5.0
- **get_ignore_patterns(project_path)**: View active ignore patterns
- **list_indexed_projects()**: List all indexed projects

### MCP Usage Examples

```python
# Index a project (ignores node_modules, .git, etc automatically)
index_codebase("/path/to/project")

# Index with custom ignore patterns
index_codebase("/path/to/project", custom_ignore=["tests/", "*.test.py"])

# Search with multiple keywords
search_code("/path/to/project", "auth user login", mode="all")

# Check what's being ignored
get_ignore_patterns("/path/to/project")
```

### Benefits

- **Zero friction**: No need to type CLI commands in Claude Desktop
- **Auto-indexing**: Projects indexed when opened
- **Rich UI**: Visual code exploration
- **Session persistence**: Maintains context between chats

## Graph Analysis Features

### Node Importance Scoring
- **Degree centrality**: Based on number of connections
- **PageRank**: Overall importance in the dependency graph
- **Weighted scoring**: Combines multiple centrality measures

### Relevance Tags
- `structural`: Classes and main components
- `highly-used`: Entities with many incoming dependencies
- `complex`: Entities with many outgoing dependencies
- `test`: Test-related code
- `module`: File-level entities

### Advanced Analysis
- **Hub detection**: Find central components in your architecture
- **Dependency tracking**: Understand code relationships
- **Impact analysis**: Trace how changes propagate
- **Similarity detection**: Find related code patterns

## Examples

### Basic Usage

```python
from claude_code_indexer import CodeGraphIndexer

# Create indexer
indexer = CodeGraphIndexer("my_project.db")

# Index a directory
indexer.index_directory("./src")

# Query important nodes
important_nodes = indexer.query_important_nodes(min_score=0.5)
for node in important_nodes:
    print(f"{node['name']} ({node['node_type']}): {node['importance_score']}")
```

### Advanced Analysis

```python
# Get graph statistics
stats = indexer.get_stats()
print(f"Total nodes: {stats['total_nodes']}")
print(f"Node types: {stats['node_types']}")

# Build NetworkX graph for custom analysis
nx_graph = indexer.build_graph()
import networkx as nx
centrality = nx.betweenness_centrality(nx_graph)
```

## Requirements

- Python 3.8+
- ensmallen >= 0.8.0
- networkx >= 3.0
- pandas >= 1.5.0
- click >= 8.0.0
- rich >= 13.0.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- 📖 [Documentation](https://docs.anthropic.com/claude-code)
- 🐛 [Issues](https://github.com/claude-ai/code-indexer/issues)
- 💬 [Discussions](https://github.com/claude-ai/code-indexer/discussions)