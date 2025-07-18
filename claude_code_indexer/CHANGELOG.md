# Changelog

All notable changes to Claude Code Indexer will be documented in this file.

## [1.10.0] - 2025-01-17

### 🚀 New Features
- **Java language support** - Added full Java parsing support using javalang AST library
- **Smart JVM class filtering** - Automatically ignores common JVM classes (String, List, Map, etc.) to focus on project-specific code
- **Comprehensive Java parsing** - Supports classes, interfaces, enums, records (Java 14+), methods, fields, constructors, inner classes, and more
- **Java-specific features** - Handles generics, annotations, modifiers, extends/implements relationships

### 🔧 Technical Details
- Uses `javalang` library for accurate AST-based parsing
- Filters 70+ common JVM classes from java.lang, java.util, java.io, java.nio, etc.
- Supports all modern Java features including records and sealed classes
- Maintains consistent node structure with other language parsers

## [1.9.2] - 2025-01-16

### 🐛 Critical Bug Fix
- **Fixed JavaScript/TypeScript indexing failure** - Fixed AttributeError when indexing JS/TS files with null/undefined names
- **Improved null safety** - Added proper null checks in calculate_importance_scores method
- **Fixed 0 nodes issue** - JavaScript and TypeScript files now properly create nodes and relationships

### 🔧 Technical Details
- Fixed `'NoneType' object has no attribute 'lower'` error in node name processing
- Added defensive coding with `.get()` and null checks
- Ensures all JS/TS entities (classes, functions, interfaces) are properly indexed

## [1.9.1] - 2025-01-16

### 🔧 Improvements
- **Random start offsets** - Projects now start indexing at random times to avoid all projects indexing simultaneously
- **Managed projects only** - Background indexing now only includes projects that are properly managed with valid paths
- **Better status display** - Shows full project paths (truncated if too long) for better visibility
- **Resource optimization** - Prevents system overload by staggering project indexing times

### 🐛 Bug Fixes
- Fixed issue where deleted projects would still appear in background indexing
- Fixed simultaneous indexing causing high CPU usage
- Improved project path validation

## [1.9.0] - 2025-01-16

### 🎯 Background Indexing Service
- **Automatic updates** - Keep your code index up-to-date automatically
- **Configurable intervals** - Set per-project or default intervals (default: 5 minutes)
- **Daemon mode** - Runs in background as a system service
- **Smart scheduling** - Only re-indexes when files have changed
- **Project management** - Configure different intervals for different projects

### 🛠️ New CLI Commands
- **`claude-code-indexer background start`** - Start the background service
- **`claude-code-indexer background stop`** - Stop the background service
- **`claude-code-indexer background restart`** - Restart the service
- **`claude-code-indexer background status`** - View service status and project schedules
- **`claude-code-indexer background config`** - Enable/disable the service
- **`claude-code-indexer background set-interval`** - Configure indexing intervals

### 📋 Configuration Options
- **Default interval** - 300 seconds (5 minutes) for all projects
- **Per-project intervals** - Override default for specific projects
- **Disable with -1** - Set interval to -1 to disable for a project
- **Persistent config** - Settings saved in `~/.claude-code-indexer/background_service.json`

### 🔧 Technical Details
- **Process management** - Uses psutil for reliable process control
- **Signal handling** - Graceful shutdown on SIGTERM/SIGINT
- **Multi-threading** - Projects indexed in parallel threads
- **Error recovery** - Continues running even if individual projects fail
- **Logging** - Service logs saved to `~/.claude-code-indexer/background_service.log`

## [1.8.0] - 2025-01-16

### 🚀 Enhanced JavaScript/TypeScript Support
- **Modern JS/TS syntax** - Support for arrow functions, async/await, JSX, TSX, React components
- **Better regex patterns** - Enhanced patterns for ES6 modules, dynamic imports, export *
- **React component detection** - Automatically detects functional and class components
- **TypeScript improvements** - Better handling of generics, abstract classes, const enums

### 🐛 Critical Bug Fixes
- **Fixed parallel processing** - JavaScript/TypeScript files now properly processed in parallel mode
- **Fixed ID mapping** - Resolved node ID mapping issue that caused 0 nodes to be indexed
- **Fixed parser integration** - Multi-language parser now correctly used in all processing paths

### 🔧 Improvements
- **Verbose logging** - New `--verbose` flag shows detailed parsing progress and errors
- **Better error handling** - Partial parsing success with detailed error messages
- **Improved comment removal** - Preserves JSX syntax while removing comments
- **Performance optimization** - More efficient ID mapping using dictionaries

### 📊 Enhanced Features
- **Multi-keyword search** - Works correctly with JavaScript/TypeScript code
- **PageRank scoring** - Proper importance calculation for JS/TS entities
- **Relationship mapping** - Accurate graph building for imports, exports, inheritance

## [1.7.0] - 2025-01-16

### 🎉 NEW: Centralized Storage Management
- **APP_HOME directory** - All project data now stored in `~/.claude-code-indexer/`
- **Project isolation** - Each project gets its own directory with unique ID
- **No permission issues** - No more writing to project directories
- **Project management** - New commands to list, remove, and clean projects

### 🛠️ New CLI Commands
- **`claude-code-indexer projects`** - List all indexed projects with stats
- **`claude-code-indexer remove <project>`** - Remove a project's index
- **`claude-code-indexer clean`** - Clean up orphaned projects
- **`--project` option** - Query/stats for specific projects by name

### 🏗️ Architecture Changes
- **StorageManager** - Centralized storage management system
- **Project metadata** - Track project info in `projects.json`
- **Smart project lookup** - Find projects by name or path
- **Automatic cleanup** - Remove indexes for deleted projects

### 🔧 Improvements
- **Better cache organization** - Cache per project in centralized location
- **Consistent database paths** - No more scattered `code_index.db` files
- **Project statistics** - Track indexing history and stats per project
- **MCP integration** - Updated to use centralized storage

### 💾 Storage Benefits
- **Single location** - All data in `~/.claude-code-indexer/`
- **Easy backup** - Backup all project indexes from one place
- **No conflicts** - Projects fully isolated from each other
- **Permission safe** - Works in read-only project directories

## [1.6.0] - 2025-01-16

### 🎉 NEW: Multi-Language Support
- **Multi-language indexing** - Now supports Python, JavaScript, and TypeScript
- **Composite Parser Pattern** - Extensible architecture for adding new languages
- **Language detection** - Automatic detection of programming languages
- **Enhanced database schema** - Added language, line_number, and column_number columns
- **Auto-discovery** - Automatically detects and indexes all supported file types

### 🔧 Language Support
- **Python** - Full AST parsing with classes, functions, methods, imports
- **JavaScript** - ES6 modules, classes, functions, arrow functions, imports/requires
- **TypeScript** - Interfaces, types, enums, namespaces, plus all JavaScript features
- **Extensible** - Easy to add new language parsers using Composite Pattern

### 🏗️ Architecture Improvements
- **Composite Pattern** - Clean separation of language-specific parsing logic
- **BaseParser interface** - Standardized parser API for all languages
- **CodeNode/CodeRelationship** - Unified data structures across languages
- **ParseResult** - Standardized parsing output format

### 🔍 Enhanced Querying
- **Language filtering** - Query by specific programming language
- **Multi-language stats** - See breakdown of files by language
- **Cross-language search** - Find patterns across different languages

### 💾 Database Enhancements
- **Language column** - Track programming language for each node
- **Line/column numbers** - Precise source code locations
- **Automatic migration** - Seamless upgrade from previous versions

### 🚀 Performance
- **Parallel processing** - Multi-language parsing with full parallelization
- **Smart caching** - Language-aware caching for faster re-indexing
- **Efficient filtering** - Skip unsupported file types early

### 📊 Statistics
- **Language breakdown** - See file counts by programming language
- **Cross-language analysis** - Understand polyglot codebases
- **Enhanced reporting** - Detailed parsing statistics

## [1.5.1] - 2025-01-16

### 🐛 Bug Fixes
- Fixed persistent temp file creation error in MCP read-only environment
- Added backward compatibility for both 'path' and 'project_path' parameters
- Improved temp file handling with fallback to home directory

## [1.5.0] - 2025-01-16

### 🎉 New Features
- **Smart Ignore Patterns**: Automatically ignores common non-source directories
  - Dependencies: `node_modules/`, `vendor/`, `packages/`, `bower_components/`
  - Build outputs: `build/`, `dist/`, `target/`, `*.egg-info/`
  - Version control: `.git/`, `.svn/`, `.hg/`
  - Python: `__pycache__/`, `*.pyc`, `venv/`, `.env/`
  - IDE: `.idea/`, `.vscode/`, `*.swp`
  - And many more...

- **Gitignore Support**: Automatically respects patterns from:
  - `.gitignore` files
  - `.dockerignore` files
  - Custom patterns via CLI or MCP

### 🔧 CLI Enhancements
- Added `--custom-ignore` option for additional ignore patterns
- Added `--show-ignored` flag to preview what will be ignored
- Examples:
  ```bash
  claude-code-indexer index . --custom-ignore "tests/" --custom-ignore "*.test.py"
  claude-code-indexer index . --show-ignored
  ```

### 🤖 MCP Improvements
- Added `custom_ignore` parameter to `index_codebase()` tool
- New tool: `get_ignore_patterns(project_path)` - View active ignore patterns
- Fixed temp file creation in read-only MCP environment

## [1.4.1] - 2025-01-16

### 🐛 Bug Fixes
- Fixed read-only file system error for `temp_edges.tsv` in MCP environment
- Improved temp file handling with automatic fallback to home directory

## [1.4.0] - 2025-01-16

### 🎉 New Features
- **Project-based MCP Storage**: Each project gets its own database
  - Separate databases stored in `~/.claude_code_indexer/projects/`
  - Support for multiple concurrent projects
  - Project path is now required for all MCP tools

### 🤖 MCP Changes
- All MCP tools now require `project_path` as first parameter
- New tool: `list_indexed_projects()` - List all indexed projects with stats
- Better error messages for missing project paths

### 🐛 Bug Fixes
- Fixed JSON parsing errors by redirecting all output to stderr in MCP mode
- Fixed MCP server environment detection

## [1.3.0] - 2025-01-16

### 🎉 New Features
- **Multi-keyword Search**: Support for searching with multiple keywords
  - OR logic (default): Match any keyword
  - AND logic: Match all keywords with `--mode all`
  - Works in both CLI and MCP server

### 🔧 CLI Enhancements
- Search command now accepts multiple arguments
- Examples:
  ```bash
  claude-code-indexer search auth user login
  claude-code-indexer search database connection --mode all
  ```

### 🤖 MCP Improvements
- Updated `search_code` tool to support multi-keyword search
- Added `mode` parameter for AND/OR search logic

## [1.2.0] - 2025-01-15

### 🚀 Performance Improvements
- **64.6x faster re-indexing** with intelligent caching
- **Parallel processing** with configurable workers
- **APSW database optimization** for faster queries
- **Connection pooling** for concurrent access

### 🎉 New Features
- Cache management commands
- Performance benchmarking tool
- Auto-update functionality

## [1.1.0] - 2025-01-14

### 🎉 New Features
- **MCP Integration**: Direct integration with Claude Desktop
- **Pattern Detection**: Identify design patterns (Singleton, Factory, etc.)
- **Library Detection**: Track external dependencies
- **Infrastructure Detection**: Find databases, APIs, cloud services

## [1.0.0] - 2025-01-13

### 🎉 Initial Release
- Graph-based code analysis using Ensmallen
- AST parsing for Python code
- PageRank importance scoring
- SQLite storage
- CLI interface
- Basic search and query functionality