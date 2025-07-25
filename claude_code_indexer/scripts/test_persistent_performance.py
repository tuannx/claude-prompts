#!/usr/bin/env python3
"""Test performance comparison between persistent daemon and process spawning"""

import time
import subprocess
import sys
import asyncio
import statistics

# Add parent directory to path
sys.path.insert(0, '/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer')

from claude_code_indexer.mcp_client import SyncMCPClient


def test_persistent_server():
    """Test search using persistent server"""
    print("\n✅ Testing with Persistent MCP Daemon (WebSocket):")
    print("-" * 60)
    
    client = SyncMCPClient('ws://127.0.0.1:8765')
    project_path = "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer"
    
    queries = ["search", "index cache", "test migration", "FTS5 database"]
    times = []
    
    # Warm up
    client.search(project_path, "warmup", limit=10)
    
    for query in queries:
        query_times = []
        for i in range(3):
            start = time.time()
            result = client.search(project_path, query, limit=50)
            elapsed = time.time() - start
            query_times.append(elapsed)
            print(f"  '{query}' run {i+1}: {elapsed*1000:.0f}ms")
        
        avg_time = statistics.mean(query_times)
        times.append(avg_time)
        print(f"  '{query}' average: {avg_time*1000:.0f}ms")
        print()
    
    client.close()
    return times


def test_process_spawning():
    """Test search using process spawning"""
    print("\n❌ Testing with Process Spawning (Current method):")
    print("-" * 60)
    
    queries = ["search", "index cache", "test migration", "FTS5 database"]
    times = []
    
    for query in queries:
        query_times = []
        for i in range(3):
            start = time.time()
            
            # Split multi-word queries
            cmd = ["claude-code-indexer", "search"] + query.split()
            proc = subprocess.run(cmd, capture_output=True, text=True)
            
            elapsed = time.time() - start
            query_times.append(elapsed)
            print(f"  '{query}' run {i+1}: {elapsed*1000:.0f}ms")
        
        avg_time = statistics.mean(query_times)
        times.append(avg_time)
        print(f"  '{query}' average: {avg_time*1000:.0f}ms")
        print()
    
    return times


def main():
    print("🚀 MCP Performance Comparison: Persistent vs Process Spawning")
    print("=" * 60)
    
    # Test persistent server
    persistent_times = test_persistent_server()
    
    # Test process spawning
    spawn_times = test_process_spawning()
    
    # Compare results
    print("\n📊 Performance Summary:")
    print("-" * 60)
    print(f"{'Method':<20} {'Avg Time':<15} {'Speedup':<10}")
    print("-" * 60)
    
    avg_persistent = statistics.mean(persistent_times)
    avg_spawn = statistics.mean(spawn_times)
    
    print(f"{'Persistent Daemon':<20} {avg_persistent*1000:>10.0f}ms")
    print(f"{'Process Spawning':<20} {avg_spawn*1000:>10.0f}ms")
    print(f"{'Improvement':<20} {'':<10} {avg_spawn/avg_persistent:>8.1f}x")
    
    print("\n💡 Benefits of Persistent Daemon:")
    print("  • No process startup overhead")
    print("  • Connection reuse")
    print("  • Warm caches stay in memory")
    print("  • Better for repeated queries")


if __name__ == '__main__':
    main()