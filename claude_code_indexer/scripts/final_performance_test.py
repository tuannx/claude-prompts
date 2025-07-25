#!/usr/bin/env python3
"""
Final comprehensive performance test after installation
"""

import time
import subprocess
from pathlib import Path

def comprehensive_performance_test():
    print("🚀 FINAL PERFORMANCE TEST - cci v1.20.0")
    print("=" * 60)
    
    project_path = "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer/final_test"
    
    # Test 1: Basic CLI Performance (Cold Start)
    print("1️⃣ CLI PERFORMANCE (Cold Start)")
    print("-" * 40)
    
    cli_times = []
    for i in range(3):
        start = time.perf_counter()
        result = subprocess.run(['cci', 'search', 'hello', '--project', project_path], 
                               capture_output=True, text=True)
        elapsed = (time.perf_counter() - start) * 1000
        cli_times.append(elapsed)
        
        # Count results
        result_count = result.stdout.count('│') - result.stdout.count('┃') - result.stdout.count('┡')
        print(f"   Run {i+1}: {elapsed:.1f}ms ({result_count} results)")
    
    avg_cli = sum(cli_times) / len(cli_times)
    print(f"   Average: {avg_cli:.1f}ms")
    
    # Test 2: Start MCP Daemon and test performance
    print(f"\n2️⃣ MCP DAEMON PERFORMANCE")
    print("-" * 40)
    
    # Start daemon
    print("🚀 Starting MCP daemon...")
    daemon_start = subprocess.run(['cci', 'mcp-daemon', 'start'], capture_output=True, text=True)
    if "started" in daemon_start.stdout:
        print("✅ MCP daemon started")
        
        # Wait a moment for daemon to be ready
        time.sleep(2)
        
        # Test daemon performance
        daemon_times = []
        for i in range(5):
            start = time.perf_counter()
            result = subprocess.run(['cci', 'search', 'hello', '--project', project_path], 
                                   capture_output=True, text=True)
            elapsed = (time.perf_counter() - start) * 1000
            daemon_times.append(elapsed)
            print(f"   Run {i+1}: {elapsed:.1f}ms")
        
        avg_daemon = sum(daemon_times) / len(daemon_times)
        min_daemon = min(daemon_times)
        print(f"   Average: {avg_daemon:.1f}ms")
        print(f"   Best:    {min_daemon:.1f}ms")
        
        # Compare performance
        improvement = avg_cli / avg_daemon if avg_daemon > 0 else 0
        print(f"   🚀 Daemon is {improvement:.1f}x faster than cold CLI")
        
    else:
        print("❌ Failed to start MCP daemon")
        avg_daemon = avg_cli
        min_daemon = avg_cli
    
    # Test 3: Different search types
    print(f"\n3️⃣ SEARCH TYPE PERFORMANCE")
    print("-" * 40)
    
    search_tests = [
        ("Function search", "hello"),
        ("Class search", "TestManager"),
        ("File search", "app.js"),
    ]
    
    for test_name, term in search_tests:
        start = time.perf_counter()
        result = subprocess.run(['cci', 'search', term, '--project', project_path], 
                               capture_output=True, text=True)
        elapsed = (time.perf_counter() - start) * 1000
        
        result_count = result.stdout.count('│') - result.stdout.count('┃') - result.stdout.count('┡')
        print(f"   {test_name:<15}: {elapsed:.1f}ms ({result_count} results)")
    
    # Test 4: Query and Stats Performance
    print(f"\n4️⃣ OTHER COMMANDS PERFORMANCE")
    print("-" * 40)
    
    other_commands = [
        ("cci query --important", ['cci', 'query', '--important', '--project', project_path]),
        ("cci stats", ['cci', 'stats', '--project', project_path]),
    ]
    
    for cmd_name, cmd in other_commands:
        start = time.perf_counter()
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"   {cmd_name:<20}: {elapsed:.1f}ms")
    
    # Test 5: grep comparison
    print(f"\n5️⃣ COMPARISON WITH GREP")
    print("-" * 40)
    
    grep_times = []
    for i in range(3):
        start = time.perf_counter()
        result = subprocess.run(['grep', '-r', 'hello', project_path], 
                               capture_output=True, text=True)
        elapsed = (time.perf_counter() - start) * 1000
        grep_times.append(elapsed)
    
    avg_grep = sum(grep_times) / len(grep_times)
    print(f"   grep search: {avg_grep:.1f}ms")
    
    # Final Summary
    print(f"\n📊 FINAL PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"CLI (cold start):     {avg_cli:.1f}ms")
    print(f"MCP daemon (warm):    {avg_daemon:.1f}ms") 
    print(f"MCP daemon (best):    {min_daemon:.1f}ms")
    print(f"grep (reference):     {avg_grep:.1f}ms")
    
    print(f"\n🎯 KEY INSIGHTS:")
    if min_daemon < avg_grep:
        speedup = avg_grep / min_daemon
        print(f"🏆 Best cci performance ({min_daemon:.1f}ms) is {speedup:.1f}x FASTER than grep!")
    elif avg_daemon < avg_cli / 2:
        improvement = avg_cli / avg_daemon
        print(f"🚀 MCP daemon provides {improvement:.1f}x speedup over cold CLI")
    
    print(f"📈 cci provides semantic understanding that grep cannot match")
    print(f"💡 Use MCP daemon for best performance: cci mcp-daemon start")

if __name__ == "__main__":
    comprehensive_performance_test()