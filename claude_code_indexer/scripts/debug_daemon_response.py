#!/usr/bin/env python3
"""
Debug daemon response format
"""

import asyncio
import websockets
import json

async def debug_response():
    try:
        uri = "ws://127.0.0.1:8765"
        async with websockets.connect(uri) as websocket:
            request = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "search_code",
                    "arguments": {
                        "project_path": "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer",
                        "terms": "CacheManager",
                        "limit": 5
                    }
                },
                "id": 1
            }
            
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            result = json.loads(response)
            
            print("📊 DAEMON RESPONSE:")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_response())