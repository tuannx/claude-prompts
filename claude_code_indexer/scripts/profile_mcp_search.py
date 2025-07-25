#!/usr/bin/env python3
"""
Profile MCP search to identify bottlenecks
Use the actual MCP search_code function
"""

import time
import cProfile
import pstats
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer')

def profile_mcp_search():
    """Profile MCP search operation"""
    
    print("🔍 PROFILING MCP SEARCH PERFORMANCE")  
    print("=" * 50)
    
    # Import MCP server search function
    from claude_code_indexer.mcp_server import search_code
    
    def search_operation():
        """The operation we want to profile"""
        project_path = "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer"
        result = search_code(project_path, "CacheManager", mode="any", limit=50)
        return result
    
    # First, do a quick timing test
    print("🚀 Quick timing test...")
    times = []
    
    for i in range(5):
        start = time.perf_counter()
        result = search_operation()
        end = time.perf_counter()
        elapsed = (end - start) * 1000
        times.append(elapsed)
        print(f"  Search {i+1}: {elapsed:.1f}ms")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    print(f"  Average: {avg_time:.1f}ms")
    print(f"  Best:    {min_time:.1f}ms")
    
    # Profile the search operation  
    print(f"\n📊 DETAILED PROFILING:")
    print("-" * 40)
    
    profiler = cProfile.Profile()
    
    profiler.enable()
    result = search_operation()
    profiler.disable()
    
    # Analyze results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    
    print(f"📊 TOP BOTTLENECKS (cumulative time):")
    stats.print_stats(15)
    
    # Test different search patterns
    print(f"\n🔄 TESTING DIFFERENT PATTERNS:")
    print("-" * 40)
    
    patterns = [
        ("Short term", "test"),
        ("Function", "parse_file"),  
        ("Class", "CacheManager"),
        ("Long term", "search_code_with_filters"),
        ("Common", "function")
    ]
    
    for name, term in patterns:
        start = time.perf_counter()
        project_path = "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer"
        result = search_code(project_path, term, mode="any", limit=50)
        end = time.perf_counter()
        elapsed = (end - start) * 1000
        
        # Count results if it's a list/dict
        count = 0
        if hasattr(result, '__len__'):
            count = len(result)
        elif hasattr(result, 'get') and 'results' in result:
            count = len(result['results'])
            
        print(f"{name:<15}: {elapsed:.1f}ms ({count} results)")

if __name__ == "__main__":
    profile_mcp_search()