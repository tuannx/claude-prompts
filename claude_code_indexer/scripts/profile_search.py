#!/usr/bin/env python3
"""
Profile cci search to identify bottlenecks
"""

import time
import cProfile
import pstats
from pathlib import Path
import sys
import os

# Add current directory to path so we can import cci modules
sys.path.insert(0, '/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer')

def profile_search():
    """Profile the search operation to find bottlenecks"""
    
    # Import cci modules directly
    from claude_code_indexer.storage_manager import get_storage_manager
    from claude_code_indexer.indexer import CodeGraphIndexer
    
    print("🔍 PROFILING CCI SEARCH PERFORMANCE")
    print("=" * 50)
    
    # Setup
    project_path = Path("/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer")
    storage = get_storage_manager()
    indexer = CodeGraphIndexer(project_path=project_path)
    
    def search_operation():
        """The operation we want to profile"""
        results = indexer.search_code("CacheManager", mode="any", limit=50)
        return results
    
    # Profile the search
    profiler = cProfile.Profile()
    
    print("🚀 Running profiled search...")
    start_time = time.perf_counter()
    
    profiler.enable()
    results = search_operation()
    profiler.disable()
    
    end_time = time.perf_counter()
    search_time = (end_time - start_time) * 1000
    
    print(f"⏱️  Search completed in {search_time:.1f}ms")
    print(f"📊 Found {len(results)} results")
    
    # Analyze profiling results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    
    print(f"\n📊 TOP 10 BOTTLENECKS:")
    print("-" * 80)
    stats.print_stats(10)
    
    # Also run a few more searches to see pattern
    print(f"\n🔄 MULTIPLE SEARCH PATTERN:")
    print("-" * 40)
    
    terms = ['parse_file', 'search_code', 'BaseParser']
    times = []
    
    for term in terms:
        start = time.perf_counter()
        results = indexer.search_code(term, mode="any", limit=50)
        end = time.perf_counter()
        elapsed = (end - start) * 1000
        times.append(elapsed)
        print(f"{term:<15}: {elapsed:.1f}ms ({len(results)} results)")
    
    avg_time = sum(times) / len(times)
    print(f"Average: {avg_time:.1f}ms")
    
    # Test database query directly
    print(f"\n🗄️  DIRECT DATABASE TEST:")
    print("-" * 40)
    
    start = time.perf_counter()
    direct_results = indexer._search_database("CacheManager", mode="any", node_type=None, limit=50)
    end = time.perf_counter()
    db_time = (end - start) * 1000
    
    print(f"Direct DB query: {db_time:.1f}ms ({len(direct_results)} results)")
    
    if db_time < search_time / 2:
        print("⚠️  Database is fast - bottleneck is elsewhere!")
    else:
        print("💾 Database query is the bottleneck")

if __name__ == "__main__":
    profile_search()