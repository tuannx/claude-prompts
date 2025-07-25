#!/usr/bin/env python3
"""
Test direct MCP daemon performance (bypass CLI)
"""

import time
import json
import asyncio
import websockets

async def test_daemon_direct():
    """Test direct WebSocket connection to MCP daemon"""
    
    print("🚀 TESTING DIRECT MCP DAEMON PERFORMANCE")
    print("=" * 50)
    
    try:
        # Connect directly to MCP daemon
        uri = "ws://127.0.0.1:8765"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to MCP daemon")
            
            # Test search request
            search_request = {
                "method": "call_tool",
                "params": {
                    "name": "search_code",
                    "arguments": {
                        "project_path": "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer",
                        "terms": "CacheManager",
                        "limit": 50,
                        "mode": "any"
                    }
                }
            }
            
            # Send multiple requests to test performance
            times = []
            
            for i in range(5):
                start = time.perf_counter()
                
                # Send request
                await websocket.send(json.dumps(search_request))
                
                # Receive response
                response = await websocket.recv()
                result = json.loads(response)
                
                end = time.perf_counter()
                elapsed = (end - start) * 1000
                times.append(elapsed)
                
                print(f"Search {i+1}: {elapsed:.1f}ms")
            
            avg_time = sum(times) / len(times)
            min_time = min(times)
            
            print(f"\n📊 DAEMON PERFORMANCE:")
            print(f"   Average: {avg_time:.1f}ms")
            print(f"   Best:    {min_time:.1f}ms")
            print(f"   🚀 {1700/avg_time:.1f}x faster than CLI!")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure MCP daemon is running: cci mcp-daemon start")

if __name__ == "__main__":
    asyncio.run(test_daemon_direct())