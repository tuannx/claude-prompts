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

## 🏗️ Engineering Principles & Patterns

### MANDATORY: Apply These Principles in Order

#### 1. **KISS (Keep It Simple, Stupid)** - ALWAYS FIRST
```python
# ❌ BAD: Over-engineered
class AbstractFactoryManager:
    # 100 lines for reading a file...

# ✅ GOOD: Simple and direct  
def read_file(path):
    with open(path) as f:
        return f.read()
```

#### 2. **ReAct Pattern** - Think Before Code
```python
"""
REASONING: Need user authentication
- Option 1: Build custom - Complex, time-consuming
- Option 2: Use library - Fast, tested
DECISION: Use established library (bcrypt)

ACTION: Implement using bcrypt
"""
def hash_password(password):
    return bcrypt.hash(password)
```

#### 3. **SOLID Principles**
- **S**ingle Responsibility: One class, one purpose
- **O**pen/Closed: Extend, don't modify
- **L**iskov Substitution: Subtypes must substitute
- **I**nterface Segregation: Small, specific interfaces
- **D**ependency Inversion: Depend on abstractions

#### 4. **DRY (Don't Repeat Yourself)**
Extract common patterns, but don't over-abstract

#### 5. **OOP Best Practices**
- Encapsulation: Hide internal state
- Composition > Inheritance
- Program to interfaces

#### 6. **DDD (Domain-Driven Design)**
- Rich domain models with business logic
- Value objects for concepts
- Repositories for data access

#### 7. **EARS Requirements**
```
[WHEN <trigger>] [WHERE <state>] 
the <system> SHALL <action> [WITHIN <performance>]
```

### 📋 Quick Decision Framework

| Situation | Apply | Why |
|-----------|-------|-----|
| Starting new feature | KISS | Simplest solution first |
| Complex logic | ReAct | Document reasoning |
| Repeated code | DRY | Extract common parts |
| Growing classes | SOLID | Split responsibilities |
| Business complexity | DDD | Model the domain |
| Unclear requirements | EARS | Formalize needs |

### 🚀 Implementation Checklist
Before coding ANY feature:
- [ ] Requirements clear? (EARS)
- [ ] Simplest approach? (KISS)
- [ ] Reasoning documented? (ReAct)
- [ ] Single responsibility? (SOLID)
- [ ] No duplication? (DRY)
- [ ] Domain modeled? (DDD)

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