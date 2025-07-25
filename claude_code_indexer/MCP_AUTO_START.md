# MCP Daemon Auto-Start Feature

## 🚀 Tính năng mới: MCP Daemon tự động khởi động

### Cách hoạt động

1. **Khi Claude Desktop gọi MCP tool lần đầu**:
   - MCP proxy kiểm tra daemon đã chạy chưa
   - Nếu chưa → tự động start daemon
   - Chờ 1 giây để daemon sẵn sàng
   - Xử lý request như bình thường

2. **Các lần gọi sau**:
   - Daemon đã chạy → không cần start
   - Direct WebSocket connection
   - Performance tối ưu

### Configuration

Chỉ cần config Claude Desktop một lần:

```json
{
  "mcpServers": {
    "claude-code-indexer": {
      "command": "python",
      "args": ["-m", "claude_code_indexer.mcp_proxy"],
      "env": {
        "MCP_SERVER_URL": "ws://127.0.0.1:8765"
      }
    }
  }
}
```

### Benefits

- ✅ **Zero manual setup** - Không cần start daemon thủ công
- ✅ **Automatic recovery** - Tự restart nếu daemon crash
- ✅ **Transparent** - User không cần biết về daemon
- ✅ **Performance** - Sau lần đầu, mọi request đều nhanh

### File Locations

- PID file: `~/.claude-code-indexer/mcp_daemon.pid`
- Log file: `~/.claude-code-indexer/mcp_daemon.log`

### Manual Control (Optional)

Vẫn có thể control daemon thủ công nếu muốn:

```bash
# Check status
claude-code-indexer mcp-daemon status

# View logs
claude-code-indexer mcp-daemon logs

# Stop daemon
claude-code-indexer mcp-daemon stop

# Restart daemon
claude-code-indexer mcp-daemon restart
```

### How It Works

```python
def ensure_daemon_running():
    # 1. Check PID file
    if pid_file.exists():
        # 2. Verify process is running
        if process_exists(pid):
            return  # Already running
    
    # 3. Start daemon
    subprocess.Popen([
        'python', '-m', 'claude_code_indexer.mcp_persistent_server'
    ])
    
    # 4. Save PID
    save_pid_file(process.pid)
```

### Troubleshooting

1. **Daemon không start**:
   - Check log file: `~/.claude-code-indexer/mcp_daemon.log`
   - Ensure port 8765 không bị occupied

2. **Performance không cải thiện**:
   - Run `mcp-daemon status` để verify daemon running
   - Check Claude Desktop console for errors

3. **Reset everything**:
   ```bash
   claude-code-indexer mcp-daemon stop
   rm ~/.claude-code-indexer/mcp_daemon.pid
   # Let auto-start handle it next time
   ```

### Summary

MCP daemon giờ **tự động start** khi cần → không cần setup gì thêm! 🎉