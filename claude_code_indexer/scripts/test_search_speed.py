#!/usr/bin/env python3
"""Simple performance test for search optimizations"""

import time
import subprocess
import json
import statistics

def run_search(query, use_fts=True):
    """Run a search and return the time taken"""
    start = time.time()
    
    # Run search using MCP
    cmd = ["python", "-m", "claude_code_indexer.mcp_server"]
    input_data = json.dumps({
        "method": "tools/call",
        "params": {
            "name": "search_code",
            "arguments": {
                "project_path": "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer",
                "terms": query,
                "limit": 50,
                "mode": "any",
                "use_fts": use_fts
            }
        }
    })
    
    try:
        result = subprocess.run(cmd, input=input_data, capture_output=True, text=True)
        elapsed = time.time() - start
        return elapsed, len(result.stdout) if result.returncode == 0 else 0
    except Exception as e:
        return time.time() - start, 0


def main():
    print("🚀 Claude Code Indexer v1.20.0 - Quick Search Performance Test")
    print("=" * 60)
    
    # First, ensure the project is indexed
    print("\n📦 Ensuring project is indexed...")
    subprocess.run(["claude-code-indexer", "index", "."], capture_output=True)
    
    # Test queries
    queries = [
        "search",
        "index cache", 
        "def test",
        "migration database",
        "FTS5"
    ]
    
    print("\n🔍 Running Search Performance Tests...")
    print("-" * 60)
    
    # Test with FTS5
    print("\n✅ WITH FTS5 (New in v1.20.0):")
    fts_times = {}
    for query in queries:
        times = []
        for _ in range(3):  # 3 runs per query
            elapsed, size = run_search(query, use_fts=True)
            times.append(elapsed)
        avg_time = statistics.mean(times)
        fts_times[query] = avg_time
        print(f"  '{query}': {avg_time*1000:.1f}ms")
    
    # Test without FTS5
    print("\n❌ WITHOUT FTS5 (LIKE queries):")
    like_times = {}
    for query in queries:
        times = []
        for _ in range(3):  # 3 runs per query
            elapsed, size = run_search(query, use_fts=False)
            times.append(elapsed)
        avg_time = statistics.mean(times)
        like_times[query] = avg_time
        print(f"  '{query}': {avg_time*1000:.1f}ms")
    
    # Show improvements
    print("\n📈 PERFORMANCE IMPROVEMENTS:")
    print("-" * 60)
    improvements = []
    for query in queries:
        if query in fts_times and query in like_times and fts_times[query] > 0:
            improvement = like_times[query] / fts_times[query]
            improvements.append(improvement)
            print(f"  '{query}': {improvement:.1f}x faster")
    
    if improvements:
        avg_improvement = statistics.mean(improvements)
        print(f"\n🎯 Average improvement: {avg_improvement:.1f}x faster with FTS5!")
    
    # Test cache
    print("\n💾 Testing Cache Performance...")
    print("-" * 60)
    
    # First call - no cache
    start = time.time()
    subprocess.run(["claude-code-indexer", "search", "cache", "performance"], capture_output=True)
    first_time = time.time() - start
    
    # Second call - should hit cache
    start = time.time()
    subprocess.run(["claude-code-indexer", "search", "cache", "performance"], capture_output=True)
    cached_time = time.time() - start
    
    print(f"  First search: {first_time*1000:.1f}ms")
    print(f"  Cached search: {cached_time*1000:.1f}ms")
    if cached_time > 0:
        print(f"  Cache speedup: {first_time/cached_time:.1f}x faster")


if __name__ == "__main__":
    main()