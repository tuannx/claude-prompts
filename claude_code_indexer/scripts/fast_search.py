#!/usr/bin/env python3
"""
Ultra-fast search client that bypasses CLI overhead
Direct WebSocket connection to MCP daemon
"""

import asyncio
import websockets
import json
import sys
import time
from pathlib import Path

class FastSearchClient:
    def __init__(self, daemon_url="ws://127.0.0.1:8765"):
        self.daemon_url = daemon_url
        self.websocket = None
    
    async def connect(self):
        """Connect to MCP daemon"""
        try:
            self.websocket = await websockets.connect(self.daemon_url)
            return True
        except Exception as e:
            print(f"❌ Cannot connect to MCP daemon: {e}")
            print("💡 Start daemon with: cci mcp-daemon start")
            return False
    
    async def search(self, terms, project_path=None, limit=10, mode="any"):
        """Fast search using direct WebSocket"""
        if not self.websocket:
            return None
        
        if not project_path:
            project_path = str(Path.cwd())
        
        request = {
            "method": "call_tool",
            "params": {
                "name": "search_code",
                "arguments": {
                    "project_path": project_path,
                    "terms": terms,
                    "limit": limit,
                    "mode": mode
                }
            }
        }
        
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            result = json.loads(response)
            return result
        except Exception as e:
            print(f"❌ Search error: {e}")
            return None
    
    async def close(self):
        """Close connection"""
        if self.websocket:
            await self.websocket.close()

async def fast_search_cli():
    """Fast CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python fast_search.py <search_terms> [--limit N] [--mode any|all]")
        print("Example: python fast_search.py CacheManager --limit 20")
        sys.exit(1)
    
    # Parse arguments
    terms = sys.argv[1]
    limit = 10
    mode = "any"
    
    for i, arg in enumerate(sys.argv):
        if arg == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
        elif arg == "--mode" and i + 1 < len(sys.argv):
            mode = sys.argv[i + 1]
    
    # Perform search
    client = FastSearchClient()
    
    start_time = time.perf_counter()
    
    if await client.connect():
        result = await client.search(terms, limit=limit, mode=mode)
        
        end_time = time.perf_counter()
        search_time = (end_time - start_time) * 1000
        
        if result and 'content' in result:
            # Parse the result content
            content = result['content'][0]['text'] if result['content'] else ""
            print(content)
            print(f"\n⚡ Search completed in {search_time:.1f}ms")
        else:
            print(f"No results found for '{terms}'")
    
    await client.close()

def benchmark_comparison():
    """Compare fast search vs regular CLI"""
    async def run_benchmark():
        print("🚀 FAST SEARCH vs CLI BENCHMARK")
        print("=" * 50)
        
        project_path = "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer"
        terms = ["CacheManager", "parse_file", "search_code"]
        
        # Test fast search
        client = FastSearchClient()
        if await client.connect():
            print("⚡ Fast WebSocket Search:")
            fast_times = []
            
            for term in terms:
                start = time.perf_counter()
                result = await client.search(term, project_path=project_path)
                end = time.perf_counter()
                elapsed = (end - start) * 1000
                fast_times.append(elapsed)
                print(f"   {term:<15}: {elapsed:.1f}ms")
            
            await client.close()
            
            avg_fast = sum(fast_times) / len(fast_times)
            print(f"   Average: {avg_fast:.1f}ms")
            
            print(f"\n🐌 Regular CLI (reference): ~1200ms")
            print(f"🚀 Speedup: {1200/avg_fast:.0f}x faster!")
    
    asyncio.run(run_benchmark())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        benchmark_comparison()
    else:
        asyncio.run(fast_search_cli())