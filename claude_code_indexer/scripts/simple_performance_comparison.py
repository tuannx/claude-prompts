#!/usr/bin/env python3
"""
Simple performance comparison between cci search and grep
Uses existing test-js-project for realistic testing
"""

import time
import subprocess
import os
from pathlib import Path

def time_command(cmd, cwd=None):
    """Time a command execution"""
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    end = time.perf_counter()
    return end - start, result

def test_performance():
    # Use existing test project
    test_dir = Path("/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer/test-js-project")
    
    if not test_dir.exists():
        print("❌ Test directory doesn't exist")
        return
    
    print("🚀 Performance Comparison: cci search vs grep")
    print(f"📁 Test directory: {test_dir}")
    print("-" * 60)
    
    # First ensure project is indexed
    print("📊 Indexing project...")
    subprocess.run(['cci', 'index', str(test_dir)], capture_output=True)
    
    # Test various search terms
    search_terms = [
        'main',      # Should find main.js and functions
        'util',      # Should find util.js  
        'function',  # Common keyword
        'test',      # Should find test files
    ]
    
    for term in search_terms:
        print(f"\n🔍 Searching for: '{term}'")
        
        # Test cci search
        cci_time, cci_result = time_command(['cci', 'search', term], cwd=test_dir)
        cci_lines = [line for line in cci_result.stdout.split('\n') if '│' in line and not line.startswith('┃')]
        cci_count = len([line for line in cci_lines if line.strip() and not line.startswith('┡')])
        
        # Test grep
        grep_time, grep_result = time_command(['grep', '-r', '-l', term, '.'], cwd=test_dir)
        grep_count = len([line for line in grep_result.stdout.split('\n') if line.strip()])
        
        # Results
        print(f"   cci:  {cci_time*1000:.1f}ms ({cci_count} results)")
        print(f"   grep: {grep_time*1000:.1f}ms ({grep_count} results)")
        
        if grep_time > 0 and cci_time > 0:
            ratio = grep_time / cci_time
            if ratio > 1:
                print(f"   🚀 cci is {ratio:.1f}x faster")
            else:
                print(f"   📈 grep is {1/ratio:.1f}x faster")

if __name__ == "__main__":
    test_performance()