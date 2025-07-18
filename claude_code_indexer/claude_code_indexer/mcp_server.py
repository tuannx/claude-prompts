#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server for Claude Code Indexer
Provides code indexing capabilities directly to Claude Desktop
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime

# Set MCP server mode for proper logging
os.environ['MCP_SERVER_MODE'] = '1'

# MCP SDK imports
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)

from .indexer import CodeGraphIndexer
from .cache_manager import CacheManager
from .parallel_processor import ParallelFileProcessor
from .storage_manager import get_storage_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create the MCP server
mcp = FastMCP("claude-code-indexer")

# Project management for MCP server using centralized storage
class ProjectManager:
    """Manages project-specific databases and caches using centralized storage"""
    
    def __init__(self):
        self.storage = get_storage_manager()
        self.indexers = {}  # Cache indexers per project
    
    def get_indexer(self, project_path: str, **kwargs) -> CodeGraphIndexer:
        """Get or create indexer for a project"""
        project_path_obj = Path(project_path).resolve()
        path_str = str(project_path_obj)
        
        if path_str not in self.indexers:
            self.indexers[path_str] = CodeGraphIndexer(
                project_path=project_path_obj,
                use_cache=True,
                parallel_workers=kwargs.get('workers', 4),
                enable_optimizations=True
            )
        
        return self.indexers[path_str]

# Global project manager
project_manager = ProjectManager()
    
@mcp.tool()
def index_codebase(project_path: Optional[str] = None, path: Optional[str] = None,
                  workers: int = 4, force: bool = False, 
                  custom_ignore: Optional[List[str]] = None) -> str:
    """Index Python codebase with graph analysis.
    
    Args:
        project_path: Project directory path to index (preferred)
        path: Alternative parameter name for project_path (backward compatibility)
        workers: Number of parallel workers (default: 4)
        force: Force re-index all files (default: False)
        custom_ignore: Additional ignore patterns beyond .gitignore (optional)
    
    Returns:
        Summary of indexing results
    """
    # Handle both parameter names for backward compatibility
    if project_path is None and path is not None:
        project_path = path
    elif project_path is None and path is None:
        return "❌ Error: Either 'project_path' or 'path' parameter is required"
    
    # Validate project path
    project_path = os.path.abspath(os.path.expanduser(project_path))
    if not os.path.exists(project_path):
        return f"❌ Project path does not exist: {project_path}"
    
    if not os.path.isdir(project_path):
        return f"❌ Project path is not a directory: {project_path}"
    
    # Get project-specific indexer
    indexer = project_manager.get_indexer(project_path, workers=workers)
    project_dir = project_manager.get_project_dir(project_path)
    
    # Run indexing
    start_time = datetime.now()
    try:
        indexer.index_directory(project_path, force_reindex=force, custom_ignore=custom_ignore)
        elapsed = (datetime.now() - start_time).total_seconds()
        
        stats = indexer.get_stats()
        return f"""✅ Indexing Complete!
📂 Project: {project_path}
📁 Total files: {stats.get('total_files', 0)}
🔗 Total nodes: {stats.get('total_nodes', 0)}
↔️ Total edges: {stats.get('total_edges', 0)}
⏱️ Time: {elapsed:.2f}s
🚀 Speed: {stats.get('total_files', 0) / elapsed:.1f} files/sec
💾 Database: {project_dir / 'code_index.db'}"""
    except Exception as e:
        return f"❌ Indexing failed: {str(e)}"
    
@mcp.tool()
def get_project_stats(project_path: str) -> str:
    """Get code indexing statistics and project overview.
    
    Args:
        project_path: Project directory path (required)
    
    Returns:
        Formatted statistics about the indexed codebase
    """
    # Validate project path
    project_path = os.path.abspath(os.path.expanduser(project_path))
    project_dir = project_manager.get_project_dir(project_path)
    db_path = project_dir / "code_index.db"
    
    if not db_path.exists():
        return f"❌ No indexed data found for project: {project_path}\nRun index_codebase first."
    
    indexer = project_manager.get_indexer(project_path)
    cache_manager = project_manager.get_cache_manager(project_path)
    
    stats = indexer.get_stats()
    cache_stats = cache_manager.get_cache_stats()
    
    return f"""📊 Code Indexing Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 Project: {project_path}
📅 Last indexed: {stats.get('last_indexed', 'Never')}
📁 Total files: {stats.get('total_files', 0)}
🔗 Total nodes: {stats.get('total_nodes', 0)}
↔️ Total edges: {stats.get('total_edges', 0)}

📋 Node Types:
{_format_node_types(stats.get('node_types', {}))}

🔗 Relationships:
{_format_relationships(stats.get('relationship_types', {}))}

💾 Cache Statistics:
• Total entries: {cache_stats['total_entries']}
• Recent (24h): {cache_stats['recent_entries']}
• Cache size: {cache_stats['cache_db_size'] / 1024:.1f} KB"""
    
@mcp.tool()
def query_important_code(project_path: str, limit: int = 20, node_type: Optional[str] = None) -> str:
    """Get most important code entities (classes, functions).
    
    Args:
        project_path: Project directory path (required)
        limit: Number of results to return (default: 20)
        node_type: Filter by type - 'class', 'function', 'method', 'file', or 'import'
    
    Returns:
        List of most important code entities with scores and tags
    """
    # Validate project path
    project_path = os.path.abspath(os.path.expanduser(project_path))
    project_dir = project_manager.get_project_dir(project_path)
    db_path = project_dir / "code_index.db"
    
    if not db_path.exists():
        return f"❌ No indexed data found for project: {project_path}\nRun index_codebase first."
    
    indexer = project_manager.get_indexer(project_path)
    
    # Get all nodes
    all_nodes = indexer.query_important_nodes(min_score=0.0, limit=1000)
    
    # Filter by type if specified
    if node_type:
        all_nodes = [n for n in all_nodes if n['node_type'] == node_type]
    
    # Sort by importance with type priority
    def sort_key(node):
        type_priority = {
            'class': 1000,
            'function': 100,
            'method': 10,
            'file': 1,
            'import': 0
        }.get(node['node_type'], 0)
        return node['importance_score'] + type_priority
    
    nodes = sorted(all_nodes, key=sort_key, reverse=True)[:limit]
    
    if not nodes:
        return "No entities found matching criteria."
    
    # Format results
    result = "🔍 Most important code entities:\n\n"
    for i, node in enumerate(nodes, 1):
        tags = ", ".join(node['relevance_tags']) if node['relevance_tags'] else "-"
        result += f"{i}. **{node['name']}** ({node['node_type']})\n"
        result += f"   📊 Score: {node['importance_score']:.3f}\n"
        result += f"   🏷️ Tags: {tags}\n"
        result += f"   📁 Path: {node['path']}\n\n"
    
    return result
    
@mcp.tool()
def search_code(project_path: str, terms: str, limit: int = 10, mode: str = "any") -> str:
    """Search for code entities by name or pattern. Supports multiple keywords.
    
    Args:
        project_path: Project directory path (required)
        terms: Search terms separated by spaces (e.g., "auth user login")
        limit: Number of results to return (default: 10)
        mode: Search mode - 'any' (OR logic) or 'all' (AND logic) (default: 'any')
    
    Returns:
        Search results with matching code entities
    
    Examples:
        search_code("/path/to/project", "auth")  # Single keyword
        search_code("/path/to/project", "auth user", mode="any")  # Match ANY keyword
        search_code("/path/to/project", "database connection", mode="all")  # Match ALL keywords
    """
    # Validate project path
    project_path = os.path.abspath(os.path.expanduser(project_path))
    project_dir = project_manager.get_project_dir(project_path)
    db_path = str(project_dir / "code_index.db")
    
    if not os.path.exists(db_path):
        return f"❌ No indexed data found for project: {project_path}\nRun index_codebase first."
    
    indexer = project_manager.get_indexer(project_path)
    
    # Parse multiple keywords
    keywords = terms.strip().split()
    if not keywords:
        return "❌ No search terms provided"
    
    # Search in database
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Build query based on mode
    if mode == 'any':
        # OR logic - match any keyword
        conditions = []
        params = []
        for keyword in keywords:
            conditions.append("(name LIKE ? OR path LIKE ? OR summary LIKE ?)")
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        where_clause = " OR ".join(conditions)
    else:
        # AND logic - must match all keywords
        conditions = []
        params = []
        for keyword in keywords:
            conditions.append("(name LIKE ? OR path LIKE ? OR summary LIKE ?)")
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        where_clause = " AND ".join(conditions)
    
    query = f"""
        SELECT * FROM code_nodes 
        WHERE {where_clause}
        ORDER BY importance_score DESC
        LIMIT ?
    """
    params.append(limit)
    
    cursor.execute(query, params)
    
    columns = [desc[0] for desc in cursor.description]
    results = []
    for row in cursor.fetchall():
        node = dict(zip(columns, row))
        if node.get('relevance_tags'):
            node['relevance_tags'] = json.loads(node['relevance_tags'])
        results.append(node)
    
    conn.close()
    
    if not results:
        return f"No results found for '{terms}' (mode: {mode})"
    
    # Format results
    output = f"🔍 Search results for '{terms}' (mode: {mode}):\n\n"
    for i, node in enumerate(results, 1):
        output += f"{i}. **{node['name']}** ({node['node_type']})\n"
        output += f"   📊 Score: {node['importance_score']:.3f}\n"
        output += f"   📁 Path: {node['path']}\n\n"
    
    return output
    
@mcp.tool()
def list_indexed_projects() -> str:
    """List all indexed projects.
    
    Returns:
        List of indexed projects with their stats
    """
    storage = get_storage_manager()
    projects = storage.list_projects()
    
    if not projects:
        return "📂 No indexed projects found."
    
    output = "📚 **Indexed Projects**\n\n"
    
    for project in projects:
        output += f"📁 **{project['name']}**\n"
        output += f"   Path: {project['path']}\n"
        output += f"   Status: {'✓ Exists' if project.get('exists', True) else '✗ Missing'}\n"
        
        if project.get('last_indexed'):
            output += f"   Last indexed: {project['last_indexed']}\n"
        
        if project.get('stats'):
            stats = project['stats']
            output += f"   Nodes: {stats.get('nodes', 0)}\n"
            output += f"   Files: {stats.get('files', 0)}\n"
        
        if project.get('db_size', 0) > 0:
            size_mb = project['db_size'] / 1024 / 1024
            output += f"   Size: {size_mb:.1f} MB\n"
        
        output += "\n"
    
    # Add storage stats
    stats = storage.get_storage_stats()
    output += f"💾 **Storage**: {stats['app_home']}\n"
    output += f"   Total projects: {stats['project_count']}\n"
    output += f"   Total size: {stats['total_size_mb']:.1f} MB\n"
    
    return output
    
@mcp.tool()
def manage_cache(project_path: str, action: str, days: int = 30) -> str:
    """Manage code indexing cache.
    
    Args:
        project_path: Project directory path (required)
        action: Cache action - 'stats' to view statistics or 'clear' to clear old entries
        days: Days threshold for clearing cache (default: 30, only used with 'clear' action)
    
    Returns:
        Cache statistics or confirmation of cache clearing
    """
    # Validate project path
    project_path = os.path.abspath(os.path.expanduser(project_path))
    project_path_obj = Path(project_path)
    cache_manager = CacheManager(project_path=project_path_obj)
    if action == "stats":
        stats = cache_manager.get_cache_stats()
        return f"""💾 Cache Statistics:
• Total entries: {stats['total_entries']}
• Recent (24h): {stats['recent_entries']}
• Total file size: {stats['total_file_size'] / 1024 / 1024:.1f} MB
• Cache DB size: {stats['cache_db_size'] / 1024:.1f} KB
• Location: {stats['cache_dir']}
• Project: {project_path}"""
    
    elif action == "clear":
        cache_manager.clear_cache(older_than_days=days)
        return f"✅ Cleared cache entries older than {days} days"
    
    return "❌ Unknown cache action. Use 'stats' or 'clear'"
    
@mcp.tool()
def get_ignore_patterns(project_path: str) -> str:
    """Get active ignore patterns for a project.
    
    Args:
        project_path: Project directory path (required)
    
    Returns:
        List of active ignore patterns
    """
    # Validate project path
    project_path = os.path.abspath(os.path.expanduser(project_path))
    if not os.path.exists(project_path):
        return f"❌ Project path does not exist: {project_path}"
    
    # Create ignore handler to get patterns
    from .ignore_handler import IgnoreHandler
    ignore_handler = IgnoreHandler(project_path)
    patterns = ignore_handler.get_patterns()
    
    # Check for .gitignore
    gitignore_exists = (Path(project_path) / '.gitignore').exists()
    dockerignore_exists = (Path(project_path) / '.dockerignore').exists()
    
    output = f"📝 Ignore Patterns for: {project_path}\n\n"
    
    if gitignore_exists:
        output += "✅ Using .gitignore\n"
    if dockerignore_exists:
        output += "✅ Using .dockerignore\n"
    
    output += f"\n📋 Total patterns: {len(patterns)}\n\n"
    output += "🚫 Ignored patterns:\n"
    
    # Group patterns by category
    categories = {
        'Dependencies': ['node_modules/', 'vendor/', 'packages/', 'bower_components/'],
        'Python': ['__pycache__/', '*.pyc', 'venv/', '.env/', 'env/'],
        'Build': ['build/', 'dist/', 'target/', '*.egg-info/'],
        'Version Control': ['.git/', '.svn/', '.hg/'],
        'IDE': ['.idea/', '.vscode/', '*.swp'],
        'Other': []
    }
    
    categorized = {cat: [] for cat in categories}
    
    for pattern in patterns:
        found = False
        for cat, cat_patterns in categories.items():
            if cat == 'Other':
                continue
            for cp in cat_patterns:
                if pattern == cp or pattern.startswith(cp.rstrip('/')):
                    categorized[cat].append(pattern)
                    found = True
                    break
            if found:
                break
        if not found:
            categorized['Other'].append(pattern)
    
    # Display by category
    for cat, items in categorized.items():
        if items:
            output += f"\n**{cat}:**\n"
            for item in sorted(items)[:10]:  # Show max 10 per category
                output += f"  • {item}\n"
            if len(items) > 10:
                output += f"  • ... and {len(items) - 10} more\n"
    
    return output
    
# Helper functions
def _format_node_types(node_types: Dict[str, int]) -> str:
    """Format node types for display"""
    if not node_types:
        return "• No data"
    
    lines = []
    for node_type, count in sorted(node_types.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"• {node_type}: {count}")
    return "\n".join(lines)


def _format_relationships(rel_types: Dict[str, int]) -> str:
    """Format relationship types for display"""
    if not rel_types:
        return "• No data"
    
    lines = []
    for rel_type, count in sorted(rel_types.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"• {rel_type}: {count}")
    return "\n".join(lines)
    


def main():
    """Main entry point for MCP server"""
    if not MCP_AVAILABLE:
        print("MCP SDK is required. Install with:", file=sys.stderr)
        print("pip install 'claude-code-indexer[mcp]'", file=sys.stderr)
        sys.exit(1)
    
    logger.info("Starting Claude Code Indexer MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()