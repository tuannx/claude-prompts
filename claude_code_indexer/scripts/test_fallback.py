#!/usr/bin/env python3
"""Test fallback mechanism when daemon is not available"""

import json
import subprocess
import sys

def test_mcp_proxy_fallback():
    """Test that proxy falls back to direct mode when daemon is unavailable"""
    
    # First, make sure daemon is NOT running
    subprocess.run([sys.executable, "-m", "claude_code_indexer.cli", "mcp-daemon", "stop"], 
                   capture_output=True)
    
    print("🧪 Testing MCP Proxy Fallback Mechanism")
    print("=" * 60)
    
    # Test a simple tool call
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_project_stats",
            "arguments": {
                "project_path": "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer"
            }
        },
        "id": 1
    }
    
    print("\n📤 Sending request to MCP proxy (daemon NOT running)...")
    
    # Call the proxy
    proc = subprocess.Popen(
        [sys.executable, "-m", "claude_code_indexer.mcp_proxy"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = proc.communicate(json.dumps(request))
    
    print("\n📥 Response:")
    if stdout:
        try:
            response = json.loads(stdout)
            print(json.dumps(response, indent=2))
            
            if 'result' in response:
                print("\n✅ Fallback mode worked! Got response from direct mode.")
            else:
                print("\n❌ Error in response")
        except json.JSONDecodeError:
            print(f"Raw stdout: {stdout}")
    
    print("\n⚠️  Warnings/Errors:")
    if stderr:
        print(stderr)
    
    # Test with daemon running
    print("\n" + "=" * 60)
    print("\n🚀 Starting daemon and testing again...")
    
    # Start daemon
    subprocess.run([sys.executable, "-m", "claude_code_indexer.cli", "mcp-daemon", "start"],
                   capture_output=True)
    
    import time
    time.sleep(2)  # Give daemon time to start
    
    # Call proxy again
    proc = subprocess.Popen(
        [sys.executable, "-m", "claude_code_indexer.mcp_proxy"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = proc.communicate(json.dumps(request))
    
    print("\n📥 Response (with daemon):")
    if stdout:
        try:
            response = json.loads(stdout)
            print(json.dumps(response, indent=2))
            print("\n✅ Daemon mode worked!")
        except json.JSONDecodeError:
            print(f"Raw stdout: {stdout}")
    
    if stderr:
        print(f"\nStderr: {stderr}")
    
    # Clean up
    subprocess.run([sys.executable, "-m", "claude_code_indexer.cli", "mcp-daemon", "stop"],
                   capture_output=True)

if __name__ == "__main__":
    test_mcp_proxy_fallback()