#!/usr/bin/env python3
"""
Optimized search script with reduced overhead
"""
import os
import sys
from pathlib import Path

# Optimize Python settings
os.environ['PYTHONOPTIMIZE'] = '1'
sys.dont_write_bytecode = True

# Add the package path
sys.path.insert(0, '/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer')

# Import only what we need
from claude_code_indexer.storage_manager import get_storage_manager
from claude_code_indexer.indexer import CodeGraphIndexer

def fast_search(terms, project_path=None, limit=10):
    """Optimized search function"""
    if not project_path:
        project_path = Path.cwd()
    
    # Direct database search
    storage = get_storage_manager()
    indexer = CodeGraphIndexer(project_path=Path(project_path))
    
    # This would call the direct search method
    print(f"🔍 Searching for: {terms}")
    print(f"📁 Project: {project_path}")
    print(f"⚡ Using optimized direct access")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python optimized_search.py <terms>")
        sys.exit(1)
    
    terms = sys.argv[1]
    fast_search(terms)
