#!/usr/bin/env python3
"""
Simple test to identify bottlenecks in search
"""

import time
import subprocess
import os

def test_bottlenecks():
    project_path = "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer"
    
    print("🔍 IDENTIFYING BOTTLENECKS")
    print("=" * 40)
    
    # Test 1: Pure CLI overhead
    print("1️⃣ CLI overhead test:")
    start = time.perf_counter()
    result = subprocess.run(['cci', '--version'], capture_output=True, text=True)
    cli_overhead = (time.perf_counter() - start) * 1000
    print(f"   CLI startup: {cli_overhead:.1f}ms")
    
    # Test 2: Database connection
    print("\n2️⃣ Database connection test:")  
    start = time.perf_counter()
    result = subprocess.run(['cci', 'stats'], capture_output=True, text=True, cwd=project_path)
    db_time = (time.perf_counter() - start) * 1000
    print(f"   Stats command: {db_time:.1f}ms")
    
    # Test 3: Simple vs complex search
    print("\n3️⃣ Search complexity test:")
    
    # Simple search
    start = time.perf_counter()
    result = subprocess.run(['cci', 'search', 'test'], capture_output=True, text=True, cwd=project_path)
    simple_time = (time.perf_counter() - start) * 1000
    print(f"   Simple search: {simple_time:.1f}ms")
    
    # Complex search
    start = time.perf_counter()
    result = subprocess.run(['cci', 'search', 'CacheManager', '--type', 'class'], capture_output=True, text=True, cwd=project_path)
    complex_time = (time.perf_counter() - start) * 1000
    print(f"   Complex search: {complex_time:.1f}ms")
    
    # Test 4: MCP daemon vs direct
    print("\n4️⃣ MCP daemon test:")
    
    # Stop daemon first
    subprocess.run(['cci', 'mcp-daemon', 'stop'], capture_output=True)
    
    # Test without daemon
    start = time.perf_counter()
    result = subprocess.run(['cci', 'search', 'test'], capture_output=True, text=True, cwd=project_path)
    no_daemon_time = (time.perf_counter() - start) * 1000
    print(f"   Without daemon: {no_daemon_time:.1f}ms")
    
    # Start daemon
    subprocess.run(['cci', 'mcp-daemon', 'start'], capture_output=True)
    time.sleep(1)  # Let daemon start
    
    # Test with daemon
    start = time.perf_counter()
    result = subprocess.run(['cci', 'search', 'test'], capture_output=True, text=True, cwd=project_path)
    with_daemon_time = (time.perf_counter() - start) * 1000
    print(f"   With daemon: {with_daemon_time:.1f}ms")
    
    # Test 5: Multiple rapid searches
    print("\n5️⃣ Rapid search test:")
    times = []
    for i in range(5):
        start = time.perf_counter()
        result = subprocess.run(['cci', 'search', 'test'], capture_output=True, text=True, cwd=project_path)
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
        print(f"   Search {i+1}: {elapsed:.1f}ms")
    
    avg_rapid = sum(times) / len(times)
    print(f"   Average: {avg_rapid:.1f}ms")
    
    print("\n📊 ANALYSIS:")
    print("-" * 40)
    if cli_overhead > 100:
        print(f"⚠️  CLI startup is slow: {cli_overhead:.1f}ms")
    if db_time > 200:
        print(f"⚠️  Database operations are slow: {db_time:.1f}ms")
    if abs(simple_time - complex_time) < 100:
        print("ℹ️  Search complexity doesn't matter much")
    if no_daemon_time > with_daemon_time * 1.5:
        print(f"🚀 Daemon helps: {no_daemon_time:.1f}ms -> {with_daemon_time:.1f}ms")
    
    print(f"\n🎯 PRIMARY BOTTLENECK:")
    bottlenecks = [
        ("CLI overhead", cli_overhead),
        ("Database query", db_time - cli_overhead),
        ("Search logic", avg_rapid - db_time)
    ]
    
    for name, time_ms in bottlenecks:
        if time_ms > 0:
            percentage = (time_ms / avg_rapid) * 100
            print(f"   {name}: {time_ms:.1f}ms ({percentage:.1f}%)")

if __name__ == "__main__":
    test_bottlenecks()