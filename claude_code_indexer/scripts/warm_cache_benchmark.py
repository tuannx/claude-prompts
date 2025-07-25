#!/usr/bin/env python3
"""
Test second-touch performance with warm cache
Compare cci vs grep when cache is warmed up
"""

import time
import subprocess
from pathlib import Path

def time_command(cmd, cwd=None):
    """Time a command execution"""
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    end = time.perf_counter()
    return end - start, result

def test_warm_performance():
    test_dir = Path("/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer")
    
    print("🔥 WARM CACHE PERFORMANCE TEST")
    print("Testing second-touch performance after cache warm-up")
    print("=" * 70)
    
    # Ensure MCP daemon is running for best performance
    print("🚀 Starting MCP daemon...")
    subprocess.run(['cci', 'mcp-daemon', 'start'], capture_output=True)
    
    search_terms = [
        'CacheManager',
        'parse_file', 
        'search_code',
        'BaseParser',
        'indexer'
    ]
    
    print("\n1️⃣ FIRST TOUCH (Cold Cache)")
    print("-" * 40)
    
    first_touch_times = {}
    for term in search_terms:
        cci_time, _ = time_command(['cci', 'search', term], cwd=test_dir)
        first_touch_times[term] = cci_time
        print(f"   {term:<15}: {cci_time*1000:.1f}ms")
    
    avg_first = sum(first_touch_times.values()) / len(first_touch_times) * 1000
    print(f"   Average: {avg_first:.1f}ms")
    
    print("\n2️⃣ SECOND TOUCH (Warm Cache)")  
    print("-" * 40)
    
    second_touch_times = {}
    for term in search_terms:
        # Run the same search again - should hit cache
        cci_time, cci_result = time_command(['cci', 'search', term], cwd=test_dir)
        second_touch_times[term] = cci_time
        
        # Count results
        cci_lines = [line for line in cci_result.stdout.split('\n') 
                     if '│' in line and not line.startswith('┃') and not line.startswith('┡')]
        cci_count = len([line for line in cci_lines if line.strip() and '─' not in line])
        
        print(f"   {term:<15}: {cci_time*1000:.1f}ms ({cci_count} results)")
    
    avg_second = sum(second_touch_times.values()) / len(second_touch_times) * 1000
    print(f"   Average: {avg_second:.1f}ms")
    
    print("\n3️⃣ GREP COMPARISON (for reference)")
    print("-" * 40)
    
    grep_times = {}
    for term in search_terms:
        grep_time, grep_result = time_command(['grep', '-r', '-l', term, '.'], cwd=test_dir)
        grep_times[term] = grep_time
        grep_count = len([line for line in grep_result.stdout.split('\n') if line.strip()])
        print(f"   {term:<15}: {grep_time*1000:.1f}ms ({grep_count} files)")
    
    avg_grep = sum(grep_times.values()) / len(grep_times) * 1000
    print(f"   Average: {avg_grep:.1f}ms")
    
    print("\n📊 PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f"First touch (cold):  {avg_first:.1f}ms")
    print(f"Second touch (warm): {avg_second:.1f}ms") 
    print(f"Grep (reference):    {avg_grep:.1f}ms")
    
    improvement = avg_first / avg_second if avg_second > 0 else 0
    grep_vs_warm = avg_grep / (avg_second / 1000) if avg_second > 0 else 0
    
    print(f"\n🚀 Cache speedup: {improvement:.1f}x faster")
    if grep_vs_warm < 1:
        print(f"🏆 Warm cci is {1/grep_vs_warm:.1f}x faster than grep!")
    else:
        print(f"📈 Grep is {grep_vs_warm:.1f}x faster than warm cci")
    
    # Test rapid-fire searches
    print("\n4️⃣ RAPID-FIRE TEST (10 searches)")
    print("-" * 40)
    
    rapid_times = []
    for i in range(10):
        cci_time, _ = time_command(['cci', 'search', 'CacheManager'], cwd=test_dir)
        rapid_times.append(cci_time * 1000)
        print(f"   Search {i+1}: {cci_time*1000:.1f}ms")
    
    avg_rapid = sum(rapid_times) / len(rapid_times)
    min_rapid = min(rapid_times)
    print(f"   Average: {avg_rapid:.1f}ms")
    print(f"   Best:    {min_rapid:.1f}ms")

if __name__ == "__main__":
    test_warm_performance()