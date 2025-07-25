# Multi-Project MCP Daemon Analysis

## Current Behavior

### Single Shared Daemon
- **One daemon** serves all projects
- Port: 8765 (fixed)
- PID: `~/.claude-code-indexer/mcp_daemon.pid`

### How it works now:
```
Project A → MCP Proxy → Daemon (8765) → Process request A
Project B → MCP Proxy → Daemon (8765) → Process request B
Project C → MCP Proxy → Daemon (8765) → Process request C
```

## Pros & Cons

### ✅ Advantages:
1. **Resource efficient** - Only one daemon process
2. **Warm cache** - Shared cache benefits all projects
3. **Simple management** - One daemon to rule them all
4. **No port conflicts** - Fixed port for all

### ❌ Potential Issues:
1. **Security concern** - Projects could theoretically access each other's data
2. **Performance bottleneck** - Heavy load from one project affects others
3. **Cache pollution** - Large project can evict small project's cache
4. **Single point of failure** - Daemon crash affects all projects

## Recommended Solutions

### Option 1: Keep Single Daemon (Current) ✅
**Best for most users**
- Simple and efficient
- Projects already isolated by `project_path` parameter
- StorageManager keeps data separate

### Option 2: Per-Project Daemons
```python
# Use project hash in port
port = 8765 + (hash(project_path) % 1000)
pid_file = f"mcp_daemon_{project_id}.pid"
```

### Option 3: Daemon Pool
```python
# Round-robin across multiple daemons
daemons = [8765, 8766, 8767, 8768]
port = daemons[hash(project_path) % len(daemons)]
```

## Current Isolation Mechanisms

1. **Database Isolation**:
   ```
   ~/.claude-code-indexer/projects/{project_id}/code_index.db
   ```

2. **Cache Isolation**:
   ```
   ~/.claude-code-indexer/projects/{project_id}/cache/
   ```

3. **Request Isolation**:
   - Every MCP call includes `project_path`
   - Server validates and uses correct database

## Recommendations

### For Most Users: Keep Current Design ✅
- Single daemon is fine
- Data is already isolated by design
- Simple and efficient

### For High Security/Performance:
1. Add `--port` option to daemon
2. Allow multiple daemons on different ports
3. Config can specify custom port per project

### Implementation (if needed):
```json
{
  "mcpServers": {
    "project-a": {
      "command": "python",
      "args": ["-m", "claude_code_indexer.mcp_proxy"],
      "env": {
        "MCP_SERVER_URL": "ws://127.0.0.1:8765"
      }
    },
    "project-b": {
      "command": "python", 
      "args": ["-m", "claude_code_indexer.mcp_proxy"],
      "env": {
        "MCP_SERVER_URL": "ws://127.0.0.1:8766"
      }
    }
  }
}
```

## Conclusion

**Current design is good for 99% use cases**:
- ✅ Data already isolated by StorageManager
- ✅ Simple daemon management
- ✅ Resource efficient
- ✅ No port conflicts

**Only need changes if**:
- Running 10+ projects simultaneously
- Strict security requirements
- Performance isolation needed