#!/usr/bin/env python3
"""Realistic benchmark showing FTS5 advantages on larger datasets"""

import time
import sqlite3
import statistics

db_path = "/Users/tuannguyen/.claude-code-indexer/projects/8d98ceddc556/code_index.db"

def create_test_data(conn):
    """Create a larger test dataset to show FTS5 advantages"""
    cursor = conn.cursor()
    
    # Check current size
    cursor.execute("SELECT COUNT(*) FROM code_nodes")
    current_count = cursor.fetchone()[0]
    print(f"Current nodes: {current_count}")
    
    # Generate more test data if needed
    if current_count < 10000:
        print("Generating additional test data...")
        cursor.executemany("""
            INSERT INTO code_nodes (name, type, path, language, summary, line_number, column_number, importance_score)
            VALUES (?, 'function', ?, 'python', ?, 1, 0, 0.5)
        """, [
            (f"test_function_{i}", f"/test/path_{i % 100}/file_{i}.py", f"Test function that does {i % 10} operations")
            for i in range(current_count, 10000)
        ])
        conn.commit()
        
        # Update FTS5
        cursor.execute("""
            INSERT INTO code_nodes_fts(rowid, name, path, summary)
            SELECT id, name, path, summary FROM code_nodes
            WHERE id > ?
        """, (current_count,))
        conn.commit()
        print(f"Added {10000 - current_count} test nodes")

def benchmark_search(conn, search_type, pattern, runs=3):
    """Benchmark a search pattern"""
    cursor = conn.cursor()
    times = []
    
    for _ in range(runs):
        start = time.time()
        
        if search_type == "fts5":
            cursor.execute("""
                SELECT cn.name, cn.path, cn.summary
                FROM code_nodes_fts fts
                JOIN code_nodes cn ON fts.rowid = cn.id
                WHERE code_nodes_fts MATCH ?
                ORDER BY cn.importance_score DESC
                LIMIT 100
            """, (pattern,))
        else:  # LIKE
            like_pattern = f"%{pattern}%"
            cursor.execute("""
                SELECT name, path, summary
                FROM code_nodes
                WHERE name LIKE ? OR path LIKE ? OR summary LIKE ?
                ORDER BY importance_score DESC
                LIMIT 100
            """, (like_pattern, like_pattern, like_pattern))
        
        results = cursor.fetchall()
        elapsed = time.time() - start
        times.append(elapsed)
    
    return statistics.mean(times), len(results)

def main():
    print("🚀 Realistic FTS5 Performance Benchmark")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    
    # Create test data if needed
    create_test_data(conn)
    
    # Test patterns - from simple to complex
    test_patterns = [
        ("Simple word", "test"),
        ("Common prefix", "get*"),
        ("Multiple words", "test function"),
        ("Complex pattern", "cache OR index OR search"),
        ("Phrase search", '"code nodes"'),
        ("Negation", "test NOT unit"),
    ]
    
    print("\n📊 Search Performance Comparison:")
    print("-" * 80)
    print(f"{'Pattern':<30} {'FTS5 Time':<15} {'LIKE Time':<15} {'Speedup':<10}")
    print("-" * 80)
    
    total_fts_time = 0
    total_like_time = 0
    
    for desc, pattern in test_patterns:
        # Skip FTS5-specific patterns for LIKE
        like_pattern = pattern.replace('"', '').replace(' OR ', ' ').replace(' NOT ', ' ') if ' OR ' in pattern or '"' in pattern else pattern
        
        fts_time, fts_count = benchmark_search(conn, "fts5", pattern)
        like_time, like_count = benchmark_search(conn, "like", like_pattern)
        
        total_fts_time += fts_time
        total_like_time += like_time
        
        speedup = like_time / fts_time if fts_time > 0 else 0
        
        print(f"{desc:<30} {fts_time*1000:>10.2f}ms  {like_time*1000:>10.2f}ms  {speedup:>8.1f}x")
    
    print("-" * 80)
    overall_speedup = total_like_time / total_fts_time if total_fts_time > 0 else 0
    print(f"{'TOTAL':<30} {total_fts_time*1000:>10.2f}ms  {total_like_time*1000:>10.2f}ms  {overall_speedup:>8.1f}x")
    
    # Show database stats
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM code_nodes")
    total_nodes = cursor.fetchone()[0]
    
    print(f"\n📈 Database contains {total_nodes:,} nodes")
    print(f"   Average FTS5 query: {(total_fts_time/len(test_patterns))*1000:.2f}ms")
    print(f"   Average LIKE query: {(total_like_time/len(test_patterns))*1000:.2f}ms")
    
    # Memory cache test
    print("\n💾 Cache Performance Test:")
    print("-" * 40)
    
    # Import the actual search function
    import sys
    sys.path.insert(0, '/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer')
    from claude_code_indexer.mcp_server import search_code
    
    # First call - no cache
    start = time.time()
    result1 = search_code("/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer", "cache test", limit=50)
    first_time = time.time() - start
    
    # Second call - from cache
    start = time.time()
    result2 = search_code("/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer", "cache test", limit=50)
    cache_time = time.time() - start
    
    print(f"  First call: {first_time*1000:.2f}ms")
    print(f"  Cached call: {cache_time*1000:.2f}ms")
    print(f"  Cache speedup: {first_time/cache_time:.1f}x faster")
    
    conn.close()

if __name__ == "__main__":
    main()