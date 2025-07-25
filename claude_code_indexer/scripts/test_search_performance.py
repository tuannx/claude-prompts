#!/usr/bin/env python3
"""Performance testing for search optimizations in v1.20.0"""

import time
import os
import sys
from pathlib import Path
import sqlite3
import statistics

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from claude_code_indexer.indexer import CodeGraphIndexer
from claude_code_indexer.mcp_server import search_code


def measure_search_performance(indexer, test_queries, use_fts=True, repeat=5):
    """Measure search performance with multiple runs"""
    results = {}
    
    for query in test_queries:
        times = []
        for _ in range(repeat):
            start = time.time()
            result = search_code(
                project_path=indexer.root_path,
                terms=query,
                limit=50,
                mode="any",
                use_fts=use_fts
            )
            end = time.time()
            times.append(end - start)
        
        results[query] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
    
    return results


def test_cache_performance(indexer, query="search", repeat=10):
    """Test cache hit performance"""
    # First call - cache miss
    start = time.time()
    result1 = search_code(
        project_path=indexer.root_path,
        terms=query,
        limit=50,
        mode="any",
        use_fts=True
    )
    first_call_time = time.time() - start
    
    # Subsequent calls - cache hits
    cache_times = []
    for _ in range(repeat):
        start = time.time()
        result = search_code(
            project_path=indexer.root_path,
            terms=query,
            limit=50,
            mode="any",
            use_fts=True
        )
        cache_times.append(time.time() - start)
    
    return {
        'first_call': first_call_time,
        'cache_hits_avg': statistics.mean(cache_times),
        'cache_speedup': first_call_time / statistics.mean(cache_times) if cache_times else 0
    }


def check_fts5_status(db_path):
    """Check if FTS5 is available and populated"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if FTS5 table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='code_nodes_fts'")
        fts_exists = cursor.fetchone() is not None
        
        if fts_exists:
            # Count entries
            cursor.execute("SELECT COUNT(*) FROM code_nodes_fts")
            fts_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM code_nodes")
            nodes_count = cursor.fetchone()[0]
            
            return {
                'enabled': True,
                'fts_entries': fts_count,
                'total_nodes': nodes_count,
                'synced': fts_count == nodes_count
            }
    except Exception as e:
        return {'enabled': False, 'error': str(e)}
    finally:
        conn.close()
    
    return {'enabled': False}


def main():
    """Run performance tests"""
    print("🚀 Claude Code Indexer v1.20.0 - Search Performance Test")
    print("=" * 60)
    
    # Use current directory as test project
    project_path = os.path.abspath(".")
    indexer = CodeGraphIndexer(project_path)
    
    # Check if indexed
    if not os.path.exists(indexer.db_path):
        print("❌ Project not indexed. Indexing now...")
        indexer.index_codebase(force=True)
    
    # Check FTS5 status
    print("\n📊 FTS5 Status:")
    fts_status = check_fts5_status(indexer.db_path)
    print(f"  - Enabled: {fts_status.get('enabled', False)}")
    if fts_status.get('enabled'):
        print(f"  - FTS entries: {fts_status.get('fts_entries', 0)}")
        print(f"  - Total nodes: {fts_status.get('total_nodes', 0)}")
        print(f"  - Synced: {fts_status.get('synced', False)}")
    
    # Test queries
    test_queries = [
        "search",
        "index cache",
        "def test",
        "class Code",
        "import os sys",
        "migration database",
        "FTS5 virtual table"
    ]
    
    print("\n🔍 Testing Search Performance...")
    print("-" * 60)
    
    # Test with FTS5
    if fts_status.get('enabled'):
        print("\n✅ WITH FTS5:")
        fts_results = measure_search_performance(indexer, test_queries, use_fts=True)
        for query, stats in fts_results.items():
            print(f"  '{query}':")
            print(f"    - Avg: {stats['avg_time']*1000:.2f}ms")
            print(f"    - Min: {stats['min_time']*1000:.2f}ms")
            print(f"    - Max: {stats['max_time']*1000:.2f}ms")
    
    # Test without FTS5
    print("\n❌ WITHOUT FTS5 (LIKE queries):")
    like_results = measure_search_performance(indexer, test_queries, use_fts=False)
    for query, stats in like_results.items():
        print(f"  '{query}':")
        print(f"    - Avg: {stats['avg_time']*1000:.2f}ms")
        print(f"    - Min: {stats['min_time']*1000:.2f}ms")
        print(f"    - Max: {stats['max_time']*1000:.2f}ms")
    
    # Compare performance
    if fts_status.get('enabled'):
        print("\n📈 PERFORMANCE IMPROVEMENT:")
        for query in test_queries:
            fts_time = fts_results[query]['avg_time']
            like_time = like_results[query]['avg_time']
            speedup = like_time / fts_time if fts_time > 0 else 0
            print(f"  '{query}': {speedup:.1f}x faster with FTS5")
    
    # Test cache performance
    print("\n💾 Testing Cache Performance...")
    print("-" * 60)
    cache_stats = test_cache_performance(indexer, "search code", repeat=10)
    print(f"  - First call (cache miss): {cache_stats['first_call']*1000:.2f}ms")
    print(f"  - Cache hits (avg): {cache_stats['cache_hits_avg']*1000:.2f}ms")
    print(f"  - Cache speedup: {cache_stats['cache_speedup']:.1f}x faster")
    
    # Overall statistics
    print("\n📊 OVERALL STATISTICS:")
    print("-" * 60)
    if fts_status.get('enabled'):
        avg_fts = statistics.mean([s['avg_time'] for s in fts_results.values()])
        avg_like = statistics.mean([s['avg_time'] for s in like_results.values()])
        print(f"  - Average FTS5 search: {avg_fts*1000:.2f}ms")
        print(f"  - Average LIKE search: {avg_like*1000:.2f}ms")
        print(f"  - Average speedup: {avg_like/avg_fts:.1f}x")
    else:
        avg_like = statistics.mean([s['avg_time'] for s in like_results.values()])
        print(f"  - Average search time: {avg_like*1000:.2f}ms")
        print(f"  - FTS5 not available (install SQLite with FTS5 support)")


if __name__ == "__main__":
    main()