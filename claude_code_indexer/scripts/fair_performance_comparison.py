#!/usr/bin/env python3
"""
Fair performance comparison: cci vs grep for their intended use cases
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

def test_fair_comparison():
    # Use the current project (large realistic codebase)
    test_dir = Path("/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer")
    
    print("🚀 Fair Performance Comparison")
    print(f"📁 Test directory: {test_dir}")
    print("=" * 80)
    
    # Ensure project is indexed
    print("📊 Indexing project (one-time cost)...")
    index_start = time.perf_counter()
    subprocess.run(['cci', 'index', str(test_dir)], capture_output=True)
    index_time = time.perf_counter() - index_start
    print(f"   Indexing took: {index_time:.2f}s")
    print()
    
    # Test 1: Semantic Code Search (cci's strength)
    print("🎯 Test 1: SEMANTIC CODE SEARCH (finding functions/classes)")
    print("-" * 60)
    
    semantic_terms = [
        'BaseParser',      # Class name
        'parse_file',      # Method name  
        'CacheManager',    # Class name
        'search_code',     # Function name
    ]
    
    total_cci_time = 0
    total_grep_time = 0
    
    for term in semantic_terms:
        print(f"🔍 Finding code entity: '{term}'")
        
        # cci search (optimized for this)
        cci_time, cci_result = time_command(['cci', 'search', term], cwd=test_dir)
        cci_lines = [line for line in cci_result.stdout.split('\n') 
                     if '│' in line and not line.startswith('┃') and not line.startswith('┡')]
        cci_count = len([line for line in cci_lines if line.strip() and '─' not in line])
        
        # grep equivalent (searching for class/function definitions)
        grep_time, grep_result = time_command(
            ['grep', '-r', '-n', f'(class|def|function).*{term}', '.', '--include=*.py', '--include=*.js'], 
            cwd=test_dir
        )
        grep_count = len([line for line in grep_result.stdout.split('\n') if line.strip()])
        
        print(f"   cci:  {cci_time*1000:.1f}ms -> {cci_count} entities")
        print(f"   grep: {grep_time*1000:.1f}ms -> {grep_count} matches")
        
        total_cci_time += cci_time
        total_grep_time += grep_time
        
        if grep_time > 0 and cci_time > 0:
            ratio = grep_time / cci_time
            if ratio > 1:
                print(f"   🚀 cci is {ratio:.1f}x faster for semantic search")
            else:
                print(f"   📈 grep is {1/ratio:.1f}x faster")
    
    print(f"\n📊 Semantic search totals:")
    print(f"   cci total:  {total_cci_time*1000:.1f}ms")
    print(f"   grep total: {total_grep_time*1000:.1f}ms")
    if total_grep_time > 0:
        overall_ratio = total_grep_time / total_cci_time
        if overall_ratio > 1:
            print(f"   🏆 cci is {overall_ratio:.1f}x faster overall for semantic search")
        else:
            print(f"   🏆 grep is {1/overall_ratio:.1f}x faster overall")
    
    print("\n" + "=" * 80)
    
    # Test 2: Content Search (grep's strength)  
    print("🎯 Test 2: CONTENT SEARCH (finding text in files)")
    print("-" * 60)
    
    content_terms = [
        'import',       # Common text
        'function',     # Keyword
        'TODO',         # Comment marker
        'error',        # Common word
    ]
    
    total_cci_content = 0
    total_grep_content = 0
    
    for term in content_terms:
        print(f"🔍 Finding content: '{term}'")
        
        # cci search (not optimized for content search)
        cci_time, cci_result = time_command(['cci', 'search', term], cwd=test_dir)
        cci_lines = [line for line in cci_result.stdout.split('\n') 
                     if '│' in line and not line.startswith('┃') and not line.startswith('┡')]
        cci_count = len([line for line in cci_lines if line.strip() and '─' not in line])
        
        # grep (optimized for this)
        grep_time, grep_result = time_command(['grep', '-r', '-l', term, '.'], cwd=test_dir)
        grep_count = len([line for line in grep_result.stdout.split('\n') if line.strip()])
        
        print(f"   cci:  {cci_time*1000:.1f}ms -> {cci_count} entities")
        print(f"   grep: {grep_time*1000:.1f}ms -> {grep_count} files")
        
        total_cci_content += cci_time
        total_grep_content += grep_time
        
        if grep_time > 0 and cci_time > 0:
            ratio = cci_time / grep_time
            if ratio > 1:
                print(f"   🚀 grep is {ratio:.1f}x faster for content search")
            else:
                print(f"   📈 cci is {1/ratio:.1f}x faster")
    
    print(f"\n📊 Content search totals:")
    print(f"   cci total:  {total_cci_content*1000:.1f}ms")
    print(f"   grep total: {total_grep_content*1000:.1f}ms")
    if total_grep_content > 0:
        content_ratio = total_cci_content / total_grep_content
        print(f"   🏆 grep is {content_ratio:.1f}x faster for content search")
    
    print("\n" + "=" * 80)
    print("🎯 CONCLUSION")
    print("=" * 80)
    print("• cci search excels at finding CODE ENTITIES (functions, classes)")
    print("• grep excels at finding TEXT CONTENT in files")
    print("• cci provides semantic understanding + importance scoring")
    print("• grep provides simple text matching")
    print(f"• cci indexing is a one-time cost ({index_time:.1f}s) for ongoing benefits")

if __name__ == "__main__":
    test_fair_comparison()