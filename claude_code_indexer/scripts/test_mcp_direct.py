#!/usr/bin/env python3
"""
Test MCP server functionality directly
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def test_mcp_server():
    """Test MCP server functionality"""
    
    print("🔍 TESTING MCP SERVER")
    print("=" * 40)
    
    # Test 1: Check if MCP server can start
    print("1️⃣ Testing MCP server import...")
    try:
        from claude_code_indexer.mcp_server import search_code, get_project_stats
        print("✅ MCP server imports successfully")
    except Exception as e:
        print(f"❌ MCP server import failed: {e}")
        return
    
    # Test 2: Test MCP functions directly
    print("\n2️⃣ Testing MCP functions directly...")
    project_path = "/Users/tuannguyen/Projects/claude-prompts/claude_code_indexer/final_test"
    
    try:
        # Test search_code function
        print("🔍 Testing search_code...")
        result = search_code(project_path, "hello", limit=5)
        print(f"✅ search_code returned: {len(result) if isinstance(result, str) else 'result'} characters")
        
        # Test get_project_stats function  
        print("📊 Testing get_project_stats...")
        stats = get_project_stats(project_path)
        print(f"✅ get_project_stats returned: {len(stats) if isinstance(stats, str) else 'result'} characters")
        
    except Exception as e:
        print(f"❌ MCP function test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Test MCP server as subprocess
    print("\n3️⃣ Testing MCP server as subprocess...")
    try:
        # Start MCP server process
        cmd = [sys.executable, "-m", "claude_code_indexer.mcp_server"]
        print(f"Starting: {' '.join(cmd)}")
        
        # Run with timeout to avoid hanging
        result = subprocess.run(cmd, 
                               input='{"method": "tools/list", "id": 1, "jsonrpc": "2.0"}\n',
                               capture_output=True, text=True, timeout=10)
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout[:200]}...")
        print(f"Stderr: {result.stderr[:200]}...")
        
    except subprocess.TimeoutExpired:
        print("⏰ MCP server test timed out (expected behavior)")
    except Exception as e:
        print(f"❌ Subprocess test failed: {e}")
    
    # Test 4: Check MCP configuration
    print("\n4️⃣ Checking MCP configuration...")
    
    # Check if mcp_config.json exists and is valid
    config_files = [
        Path.cwd() / "mcp_config.json",
        Path.home() / ".claude-code-indexer" / "mcp_config.json"
    ]
    
    for config_file in config_files:
        if config_file.exists():
            print(f"📄 Found config: {config_file}")
            try:
                with open(config_file) as f:
                    config = json.load(f)
                print(f"✅ Config is valid JSON")
                if "mcpServers" in config:
                    servers = config["mcpServers"]
                    print(f"📋 Found {len(servers)} MCP servers configured")
                    for name, server_config in servers.items():
                        print(f"   {name}: {server_config.get('command', 'no command')}")
            except Exception as e:
                print(f"❌ Config error: {e}")
        else:
            print(f"❌ Config not found: {config_file}")

def test_claude_desktop_integration():
    """Test integration with Claude Desktop"""
    
    print("\n🖥️  CLAUDE DESKTOP INTEGRATION TEST")
    print("=" * 40)
    
    # Check Claude Desktop config locations
    claude_config_paths = [
        Path.home() / "Library/Application Support/Claude/claude_desktop_config.json",
        Path.home() / ".config/claude/claude_desktop_config.json",
        Path.cwd() / "claude_desktop_config.json"
    ]
    
    for config_path in claude_config_paths:
        if config_path.exists():
            print(f"📄 Found Claude Desktop config: {config_path}")
            try:
                with open(config_path) as f:
                    config = json.load(f)
                
                if "mcpServers" in config:
                    servers = config["mcpServers"]
                    if "claude-code-indexer" in servers:
                        server_config = servers["claude-code-indexer"]
                        print(f"✅ claude-code-indexer found in config")
                        print(f"   Command: {server_config.get('command', 'N/A')}")
                        print(f"   Args: {server_config.get('args', 'N/A')}")
                        
                        # Test if the command exists
                        command = server_config.get('command', [''])[0]
                        if Path(command).exists():
                            print(f"✅ Command executable exists: {command}")
                        else:
                            print(f"❌ Command executable missing: {command}")
                    else:
                        print(f"❌ claude-code-indexer not found in MCP servers")
                        print(f"Available servers: {list(servers.keys())}")
                else:
                    print(f"❌ No mcpServers section in config")
                    
            except Exception as e:
                print(f"❌ Error reading config: {e}")
        else:
            print(f"❌ Config not found: {config_path}")

if __name__ == "__main__":
    test_mcp_server()
    test_claude_desktop_integration()