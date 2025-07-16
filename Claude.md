# Claude Coding Assistant - Setup Rules

## Vibecode Mode (Fast Flow) 🚀
When user says "vibecode" or "!!!" or wants fast execution:
- **Skip confirmations** - Proceed directly without asking
- **Auto-planning** - Create todo and start immediately  
- **Silent execution** - Only report final results
- **Smart defaults** - Make reasonable choices autonomously
- **Batch reporting** - Summarize all changes at the end

!!! VIBECODE = NO ASK, JUST DO !!!
!!! USER TYPES "!!!" = VIBECODE MODE ON !!!

## Core Workflow Rules

1. **First think through the problem**, read the codebase for relevant files, and write a plan to `tasks/todo.md`.

2. **The plan should have a list of todo items** that you can check off as you complete them.

3. **Before you begin working**, check in with me and I will verify the plan. !!! SKIP IN VIBECODE !!!

4. **Then, begin working on the todo items**, marking them as complete as you go.

5. **Please every step of the way** just give me a high level explanation of what changes you made. !!! VIBECODE = SILENT !!!

6. **Make every task and code change you do as simple as possible**. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.

7. **Finally, add a review section** to the `todo.md` file with a summary of the changes you made and any other relevant information.

## Code Quality Principles

- **Use small files** to make changes easy
- **Trust the functionality of each file**
- **When debugging/testing, change only 1 file at a time**
- **Every change should be minimal and focused**
- **Prioritize simplicity over complexity**

## Session Management

- **Use Shift + Tab** to switch to Plan mode (prefer Opus 4 if available)
- **After completing a task**, use `/cancel` or start a new session for optimal performance and cost efficiency
- **Confirm before any code implementation** !!! VIBECODE = AUTO GO !!!

## Required Workflow Steps

1. **Planning Phase** → Use planning mode prompt
2. **Implementation Phase** → Follow todo checklist
3. **Security Check** → Run security validation prompt
4. **Learning Phase** → Use explanation prompt for knowledge transfer

## Task History Tracking
- **Create task file** in `tasks/YYYY/MM/` for each new request
- **Use template** from `tasks/templates/task-template.md`
- **Archive monthly** to keep workspace clean
- **Reference past tasks** for similar implementations

## Code Indexing with Graph Database

### ⚠️ IMPORTANT: Claude Code Indexer is ALREADY IMPLEMENTED
**DO NOT re-implement code indexing functionality!** The `claude-code-indexer` package provides everything needed.

### Quick Start (Just Use These Commands!)
```bash
# 1. Install the package (if not already installed)
pip install claude-code-indexer

# 2. Initialize in current directory (auto-updates this file)
claude-code-indexer init

# 3. Index the codebase
claude-code-indexer index .

# 4. Use the indexed data
claude-code-indexer query --important  # Show key components
claude-code-indexer search <term>      # Search for specific code
claude-code-indexer stats              # View statistics
```

### What It Does
- **Automatically indexes** Python code using AST parsing
- **Builds graph database** with Ensmallen for relationships
- **Calculates importance** using PageRank and centrality
- **Stores in SQLite** for fast queries
- **No implementation needed** - just use the CLI commands!

### SQLite Database Schema
```sql
-- Nodes table
CREATE TABLE code_nodes (
  id INTEGER PRIMARY KEY,
  node_type TEXT,  -- 'module', 'class', 'method', 'function'
  name TEXT,
  path TEXT,
  summary TEXT,
  importance_score REAL,  -- 0.0 to 1.0
  relevance_tags TEXT,    -- JSON array of tags
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relationships table
CREATE TABLE relationships (
  source_id INTEGER,
  target_id INTEGER,
  relationship_type TEXT,  -- 'imports', 'calls', 'inherits', 'contains'
  weight REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### CLI Commands
- `claude-code-indexer init` - Initialize in current directory
- `claude-code-indexer index <path>` - Index code directory
- `claude-code-indexer query --important` - Show important nodes
- `claude-code-indexer stats` - Show indexing statistics
- `claude-code-indexer search <term>` - Search for code entities

### Node Importance Ranking
- **Degree centrality**: Number of connections (in/out)
- **PageRank**: Overall importance in graph
- **Usage frequency**: How often referenced
- **Centrality measures**: Hub detection

### Relevance Tagging
- **structural**: Classes and core components
- **highly-used**: Nodes with many incoming edges
- **complex**: Nodes with many outgoing edges
- **test**: Test-related code
- **module**: File-level nodes

### Advanced Features
- **Ensmallen integration**: Graph embeddings and similarity
- **Code similarity**: Find similar components
- **Impact analysis**: Trace changes through codebase
- **Architecture visualization**: Understand code structure