#!/usr/bin/env python3
"""Direct benchmark of search performance with FTS5"""

import time
import sqlite3
import statistics

# Database path
db_path = "/Users/tuannguyen/.claude-code-indexer/projects/8d98ceddc556/code_index.db"

def benchmark_fts5_search(conn, query, runs=5):
    """Benchmark FTS5 search"""
    times = []
    for _ in range(runs):
        start = time.time()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cn.name, cn.path, cn.importance_score
            FROM code_nodes_fts fts
            JOIN code_nodes cn ON fts.rowid = cn.id
            WHERE code_nodes_fts MATCH ?
            ORDER BY cn.importance_score DESC
            LIMIT 50
        """, (query,))
        results = cursor.fetchall()
        times.append(time.time() - start)
    return statistics.mean(times), len(results)

def benchmark_like_search(conn, query, runs=5):
    """Benchmark LIKE search"""
    times = []
    for _ in range(runs):
        start = time.time()
        cursor = conn.cursor()
        like_query = f"%{query}%"
        cursor.execute("""
            SELECT name, path, importance_score
            FROM code_nodes
            WHERE name LIKE ? OR path LIKE ? OR summary LIKE ?
            ORDER BY importance_score DESC
            LIMIT 50
        """, (like_query, like_query, like_query))
        results = cursor.fetchall()
        times.append(time.time() - start)
    return statistics.mean(times), len(results)

def main():
    print("🚀 Direct SQLite FTS5 vs LIKE Performance Test")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    
    # Test queries
    queries = ["search", "index", "cache", "test", "migration", "database", "performance"]
    
    print("\n✅ FTS5 Search Performance:")
    print("-" * 40)
    fts_times = {}
    for query in queries:
        avg_time, count = benchmark_fts5_search(conn, query)
        fts_times[query] = avg_time
        print(f"  '{query}': {avg_time*1000:.2f}ms ({count} results)")
    
    print("\n❌ LIKE Search Performance:")
    print("-" * 40)
    like_times = {}
    for query in queries:
        avg_time, count = benchmark_like_search(conn, query)
        like_times[query] = avg_time
        print(f"  '{query}': {avg_time*1000:.2f}ms ({count} results)")
    
    print("\n📈 Performance Improvement:")
    print("-" * 40)
    improvements = []
    for query in queries:
        if fts_times[query] > 0:
            improvement = like_times[query] / fts_times[query]
            improvements.append(improvement)
            print(f"  '{query}': {improvement:.1f}x faster with FTS5")
    
    avg_improvement = statistics.mean(improvements)
    print(f"\n🎯 Average improvement: {avg_improvement:.1f}x faster!")
    
    # Test compound queries
    print("\n🔍 Compound Query Test:")
    print("-" * 40)
    
    # FTS5 compound
    start = time.time()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cn.name, cn.path
        FROM code_nodes_fts fts
        JOIN code_nodes cn ON fts.rowid = cn.id
        WHERE code_nodes_fts MATCH 'search OR index OR cache'
        ORDER BY cn.importance_score DESC
        LIMIT 50
    """)
    fts_compound = cursor.fetchall()
    fts_time = time.time() - start
    
    # LIKE compound
    start = time.time()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, path
        FROM code_nodes
        WHERE (name LIKE '%search%' OR path LIKE '%search%' OR summary LIKE '%search%'
            OR name LIKE '%index%' OR path LIKE '%index%' OR summary LIKE '%index%'
            OR name LIKE '%cache%' OR path LIKE '%cache%' OR summary LIKE '%cache%')
        ORDER BY importance_score DESC
        LIMIT 50
    """)
    like_compound = cursor.fetchall()
    like_time = time.time() - start
    
    print(f"  FTS5 (OR query): {fts_time*1000:.2f}ms ({len(fts_compound)} results)")
    print(f"  LIKE (OR query): {like_time*1000:.2f}ms ({len(like_compound)} results)")
    print(f"  Improvement: {like_time/fts_time:.1f}x faster")
    
    conn.close()

if __name__ == "__main__":
    main()