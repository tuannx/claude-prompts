# Claude Coding Assistant - Setup Rules

## 🚀 MANDATORY: Start Every Session with Code Indexing

### ⚡ FIRST THING TO DO IN EVERY SESSION:
```bash
# 1. Check if project is indexed (takes 0.1s)
claude-code-indexer stats

# 2. If not indexed or outdated, run indexing (uses cache, very fast)
claude-code-indexer index . --workers 4

# 3. Load project context into memory
claude-code-indexer query --important --limit 20
```

### 📊 Why This is CRITICAL:
- **64.6x faster** than reading files manually (0.07s vs 4.66s)
- **Instant understanding** of project structure and relationships
- **Smart prioritization** - See most important code first
- **Change awareness** - Know what was modified since last session
- **Pattern detection** - Understand architecture and design patterns
- **Dependency mapping** - See how components connect

## 🎯 Session Workflow with Code Indexer

### 1. **Session Start (ALWAYS DO THIS)**
```bash
# Get project overview
claude-code-indexer stats

# See key components
claude-code-indexer query --important --limit 15

# Check recent changes
claude-code-indexer query --recent --limit 10
```

### 2. **Before Any Task**
```bash
# Search for relevant code
claude-code-indexer search "<feature_name>"

# Find related components
claude-code-indexer query --related "<component>"

# Check design patterns
claude-code-indexer query --patterns
```

### 3. **During Development**
```bash
# After making changes, re-index (instant with cache)
claude-code-indexer index . 

# Verify impact of changes
claude-code-indexer query --dependencies "<changed_file>"
```

## 🛠️ Core Workflow Rules

### With Code Indexer Integration:
1. **First, run `claude-code-indexer stats`** to understand the project
2. **Think through the problem** using indexed data for context
3. **Read specific files** only when needed (indexer shows which ones)
4. **Write a plan** based on graph analysis and importance scores
5. **Make changes** with full awareness of dependencies
6. **Re-index after changes** to maintain accurate context

## 📈 Performance Benefits

### Traditional Approach:
- Read multiple files: 5-10 seconds
- Search for code: 2-5 seconds per search
- Understand relationships: Manual analysis
- Find important code: Trial and error

### With Code Indexer:
- Load full context: 0.1 seconds (cached)
- Search anything: 0.05 seconds
- See relationships: Instant graph view
- Find important code: PageRank-sorted

## 🔍 Smart Code Search Examples

```bash
# Find all authentication-related code
claude-code-indexer search "auth"

# Find all database models
claude-code-indexer query --type class --path "**/models.py"

# Find most complex functions (high outgoing edges)
claude-code-indexer query --complex --type function

# Find unused code (no incoming edges)
claude-code-indexer query --unused

# Find test coverage
claude-code-indexer query --type test --stats
```

## 💡 Advanced Usage for Complex Tasks

### Refactoring:
```bash
# Find all dependencies before refactoring
claude-code-indexer query --dependencies "module_to_refactor.py"

# Check impact radius
claude-code-indexer query --impact "ClassName"
```

### Debugging:
```bash
# Trace call paths
claude-code-indexer query --call-path "function_name"

# Find related errors
claude-code-indexer search "error" --context 5
```

### Architecture Analysis:
```bash
# View design patterns
claude-code-indexer query --patterns --stats

# Check coupling metrics
claude-code-indexer stats --coupling

# Find circular dependencies
claude-code-indexer query --circular
```

## ⚠️ Important Notes

### Performance Optimization:
- **Always use cache** - 64.6x faster for re-indexing
- **Use parallel workers** - `--workers 4` for faster initial indexing
- **Incremental updates** - Only changed files are re-processed
- **Query limits** - Use `--limit` to avoid information overload

### Best Practices:
- **Index at session start** - Ensures fresh context
- **Re-index after major changes** - Maintains accuracy
- **Use search instead of grep** - Graph-aware results
- **Trust importance scores** - PageRank knows what matters

### Integration with Claude Code:
- **Automatically installed** when you run any command
- **Updates CLAUDE.md** on first init
- **Preserves existing rules** while adding indexing
- **Works alongside** your existing workflow

## 🚨 DO NOT:
- **Skip initial indexing** - You'll miss critical context
- **Use grep/find** - Use `claude-code-indexer search` instead
- **Read files randomly** - Let importance scores guide you
- **Ignore cache** - It's 64.6x faster!
- **Re-implement indexing** - It's already done and optimized!

## 📊 Expected Performance:
- **First index**: 2-20 seconds depending on project size
- **Cached index**: 0.05-1 second (64.6x faster)
- **Queries**: 0.01-0.1 seconds
- **Search**: 0.05-0.2 seconds
- **Cache hit rate**: 95-100% in normal development

---

Remember: **ALWAYS start with `claude-code-indexer stats`** - it's the difference between coding blind and coding with full project awareness!

## Code Indexing with Graph Database

### 🚀 START EVERY SESSION: Load Project Context First!
**IMPORTANT: At the beginning of EVERY new Claude Code session, run these commands to understand the project:**

```bash
# 1. Quick project overview (takes ~0.1s with cache)
claude-code-indexer stats

# 2. Show the most important code components
claude-code-indexer query --important --limit 20

# 3. View project structure and relationships
claude-code-indexer query --type class --limit 10
claude-code-indexer query --type function --limit 15
```

### ⚡ Why Use Claude Code Indexer First?
- **64.6x faster** than re-reading files (0.07s vs 4.66s)
- **Instant context** - Cached analysis loads in milliseconds
- **Smart ranking** - See most important code first via PageRank
- **Relationship mapping** - Understand how code connects
- **Change detection** - Know what files were recently modified
- **Pattern recognition** - Detect design patterns and architectures

### ⚠️ IMPORTANT: Claude Code Indexer is ALREADY IMPLEMENTED
**DO NOT re-implement code indexing functionality!** The `claude-code-indexer` package provides everything needed.

### Quick Start (Just Use These Commands!)
```bash
# 1. Install the package (if not already installed)
pip install claude-code-indexer

# 2. Initialize in current directory (auto-updates this file)
claude-code-indexer init

# 3. Index the codebase with performance optimizations
claude-code-indexer index . --workers 4

# 4. Use the indexed data
claude-code-indexer query --important  # Show key components
claude-code-indexer search <term>      # Search for specific code
claude-code-indexer stats              # View statistics
```

### 🎯 Recommended Workflow for Claude Code
1. **Start session** → Run `claude-code-indexer stats` to see project overview
2. **Before coding** → Run `claude-code-indexer query --important` to understand key components
3. **When searching** → Use `claude-code-indexer search <term>` instead of grep/find
4. **After changes** → Re-run `claude-code-indexer index .` (uses cache, very fast)
5. **For debugging** → Use `claude-code-indexer query --related <component>` to trace dependencies

### What It Does
- **Automatically indexes** Python code using AST parsing
- **Builds graph database** with NetworkX for relationships
- **Calculates importance** using PageRank and centrality
- **Stores in SQLite** for fast queries with APSW optimization
- **Caches results** for 64.6x faster re-indexing
- **Parallel processing** for large codebases
- **No implementation needed** - just use the CLI commands!

### Performance Features (v1.2.0+)
- **Smart caching** - Only re-indexes changed files
- **Parallel processing** - Multi-worker AST parsing
- **Database optimization** - APSW with connection pooling
- **Incremental updates** - Hash-based change detection
- **Memory efficient** - Streaming processing for large projects

### CLI Commands
- `claude-code-indexer init` - Initialize in current directory
- `claude-code-indexer index <path>` - Index code directory
  - `--workers N` - Use N parallel workers
  - `--force` - Force re-index all files
  - `--no-cache` - Disable caching
- `claude-code-indexer query --important` - Show important nodes
  - `--limit N` - Limit results
  - `--type <type>` - Filter by node type
- `claude-code-indexer stats` - Show indexing statistics
  - `--cache` - Include cache statistics
- `claude-code-indexer search <term>` - Search for code entities
- `claude-code-indexer cache --clear` - Clear old cache entries
- `claude-code-indexer benchmark` - Test performance

### SQLite Database Schema
```sql
-- Nodes table with performance optimizations
CREATE TABLE code_nodes (
  id INTEGER PRIMARY KEY,
  node_type TEXT,  -- 'module', 'class', 'method', 'function'
  name TEXT,
  path TEXT,
  summary TEXT,
  importance_score REAL,  -- 0.0 to 1.0
  weight REAL DEFAULT 0.0,  -- Usage frequency weight
  frequency_score REAL DEFAULT 0.0,
  usage_stats TEXT DEFAULT "{}",  -- JSON usage statistics
  relevance_tags TEXT,    -- JSON array of tags
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relationships table with weights
CREATE TABLE relationships (
  source_id INTEGER,
  target_id INTEGER,
  relationship_type TEXT,  -- 'imports', 'calls', 'inherits', 'contains'
  weight REAL DEFAULT 1.0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pattern detection results
CREATE TABLE IF NOT EXISTS patterns (
  id INTEGER PRIMARY KEY,
  file_path TEXT,
  pattern_type TEXT,
  confidence REAL,
  details TEXT
);

-- Library usage tracking
CREATE TABLE IF NOT EXISTS libraries (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  category TEXT,
  usage_count INTEGER DEFAULT 1,
  import_statements TEXT
);
```

### Node Importance Ranking
- **Degree centrality**: Number of connections (in/out)
- **PageRank**: Overall importance in graph
- **Usage frequency**: How often referenced
- **Centrality measures**: Hub detection
- **Weight calculation**: Based on imports, calls, and references

### Pattern & Infrastructure Detection
- **Design Patterns**: Singleton, Factory, Observer, Strategy, etc.
- **Libraries**: Categorized by type (web, ML, database, testing)
- **Infrastructure**: Databases, APIs, cloud services, message queues
- **Architecture**: MVC, microservices, monolithic patterns

### Relevance Tagging
- **structural**: Classes and core components
- **highly-used**: Nodes with many incoming edges
- **complex**: Nodes with many outgoing edges
- **test**: Test-related code
- **module**: File-level nodes
- **pattern**: Contains design patterns
- **infrastructure**: External service connections

### Advanced Features
- **Graph analysis**: NetworkX-powered relationship mapping
- **Code similarity**: Find similar components
- **Impact analysis**: Trace changes through codebase
- **Architecture visualization**: Understand code structure
- **Incremental indexing**: Only process changed files
- **Performance monitoring**: Built-in benchmarking tools

### Example Usage for Claude Code Sessions
```bash
# Start of session - understand the project (0.1s with cache)
$ claude-code-indexer stats
📊 Code Indexing Statistics
 Last indexed: 2024-01-15 10:30:45
 Total nodes: 1,234
 Total edges: 2,456
 Cache hit rate: 98.5%

# See most important components
$ claude-code-indexer query --important --limit 10
🔍 Most important code entities:
1. MainApplication (class) - score: 0.85
2. DatabaseManager (class) - score: 0.72
3. process_request (function) - score: 0.68
...

# Search for specific functionality
$ claude-code-indexer search "authentication"
🔍 Search results for 'authentication':
- auth.py: AuthenticationManager (class)
- middleware.py: authenticate_user (function)
- models.py: User.check_password (method)
```

### Performance Benchmarks
- **Small project (50 files)**: ~0.5s fresh, ~0.05s cached
- **Medium project (500 files)**: ~3s fresh, ~0.2s cached  
- **Large project (5000 files)**: ~20s fresh, ~1s cached
- **Cache hit rate**: Typically 95-100% in development
- **Memory usage**: ~50MB for 1000 files
- **Database size**: ~1MB per 100 files indexed