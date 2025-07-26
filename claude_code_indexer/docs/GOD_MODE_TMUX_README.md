# GOD Mode Tmux Integration

## Overview
GOD Mode Tmux Integration provides a powerful multi-pane interface for monitoring and controlling autonomous agents in real-time.

## Installation

### Prerequisites
1. Install tmux:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tmux
   
   # macOS
   brew install tmux
   
   # Check installation
   tmux -V
   ```

2. Ensure claude-code-indexer is installed:
   ```bash
   pip install claude-code-indexer
   ```

## Quick Start

### 1. Start GOD Mode with Tmux
```bash
# Start with tmux interface
claude-code-indexer god-mode start --tmux

# Or use the shortcut
cci god-mode tmux
```

### 2. Attach to Existing Session
```bash
# Via CLI
claude-code-indexer god-mode tmux --attach

# Or directly with tmux
tmux attach -t god-mode
```

### 3. Check Status
```bash
claude-code-indexer god-mode tmux --status
```

## Layout Overview

The tmux interface creates a 6-pane layout:

```
┌─────────────────────────┬─────────────────────┐
│   Control Panel (0)     │   Agent Status (1)  │
├─────────────────────────┼─────────────────────┤
│   Architect Agent (2)   │   Audit Trail (4)   │
├─────────────────────────┼─────────────────────┤
│   Developer Agent (3)   │   MCP Server (5)    │
└─────────────────────────┴─────────────────────┘
```

### Pane Functions:
- **Control Panel**: Main command interface
- **Agent Status**: Real-time status of all agents
- **Architect Agent**: Planning and task decomposition
- **Developer Agent**: Code implementation
- **Audit Trail**: Real-time audit logging
- **MCP Server**: MCP server status and logs

## Key Bindings

### Navigation
- `Ctrl-b + 0-5`: Switch to pane by number
- `Ctrl-b + arrow`: Navigate between panes
- `Ctrl-b + z`: Zoom/unzoom current pane
- `Ctrl-b + d`: Detach from session

### Window Management
- `Ctrl-b + c`: Create new window
- `Ctrl-b + n/p`: Next/previous window
- `Ctrl-b + w`: List windows

### Session Control
- `Ctrl-b + s`: List sessions
- `Ctrl-b + $`: Rename session
- `Ctrl-b + x`: Kill current pane (confirm with 'y')

## Commands

### Execute Agent Tasks
```bash
# Execute task with specific agent in tmux
claude-code-indexer god-mode agent architect "Design REST API" --tmux
claude-code-indexer god-mode agent developer "Implement auth module" --tmux
```

### Monitor Agents
```bash
# Run the demo monitor
python examples/god_mode_tmux_demo.py monitor
```

### Kill Session
```bash
# Via CLI
claude-code-indexer god-mode tmux --kill

# Or with tmux
tmux kill-session -t god-mode
```

## Advanced Usage

### Custom Layouts
Create a custom tmux configuration file `~/.tmux-god-mode.conf`:

```tmux
# GOD Mode custom layout
new-session -d -s god-mode

# Create custom pane arrangement
split-window -h -p 40
split-window -v -p 75
select-pane -t 0
split-window -v -p 50

# Set pane titles
select-pane -t 0 -T "Control"
select-pane -t 1 -T "Status"
select-pane -t 2 -T "Agents"
select-pane -t 3 -T "Logs"
```

Load with:
```bash
tmux -f ~/.tmux-god-mode.conf
```

### Scripting Integration
```python
from claude_code_indexer.commands.tmux_orchestrator import TmuxOrchestrator

# Create orchestrator
orchestrator = TmuxOrchestrator("my-session")

# Create session and layout
orchestrator.create_session()
orchestrator.create_layout()

# Execute tasks
task_id = orchestrator.execute_agent_task("architect", "Design feature X")

# Monitor output
output = orchestrator.capture_output("architect", lines=20)
print(output)

# Send commands
orchestrator.send_command("developer", "pytest tests/")
```

### Continuous Monitoring
```python
import asyncio

async def monitor_agent(orchestrator, agent_name):
    def on_output_change(output):
        print(f"{agent_name}: {output.strip()[-100:]}")
    
    await orchestrator.monitor_pane(agent_name, on_output_change)

# Run monitoring
asyncio.run(monitor_agent(orchestrator, "architect"))
```

## Tips & Tricks

### 1. Persistent Sessions
Tmux sessions persist even when disconnected. Use this for long-running tasks:
```bash
# Start in background
claude-code-indexer god-mode start --tmux
# Detach with Ctrl-b + d
# Reattach later
tmux attach -t god-mode
```

### 2. Logging
Capture all output to a file:
```bash
# Start logging
tmux pipe-pane -t god-mode:0.0 -o 'cat >> ~/god-mode.log'
```

### 3. Synchronize Panes
Execute same command in multiple panes:
```bash
# Enable synchronization
tmux setw synchronize-panes on
# Type commands (will go to all panes)
# Disable
tmux setw synchronize-panes off
```

### 4. Save Layout
Save your custom layout:
```bash
# Install tmux-resurrect
git clone https://github.com/tmux-plugins/tmux-resurrect ~/tmux-resurrect

# Save session
tmux run-shell ~/tmux-resurrect/resurrect.tmux save

# Restore session
tmux run-shell ~/tmux-resurrect/resurrect.tmux restore
```

## Troubleshooting

### Session Already Exists
```bash
# Kill existing session
claude-code-indexer god-mode tmux --kill
# Or force kill
tmux kill-session -t god-mode
```

### Pane Not Responding
```bash
# Respawn pane
tmux respawn-pane -t god-mode:0.2 -k
```

### Lost in Tmux
```bash
# List all sessions
tmux ls
# Detach from current
Ctrl-b + d
# Kill all tmux
tmux kill-server
```

## Demo

Run the interactive demo:
```bash
# Start demo
python examples/god_mode_tmux_demo.py

# Monitor demo (in another terminal)
python examples/god_mode_tmux_demo.py monitor
```

## Integration with VSCode

Add to VSCode settings.json:
```json
{
  "terminal.integrated.profiles.linux": {
    "god-mode": {
      "path": "tmux",
      "args": ["attach", "-t", "god-mode"]
    }
  }
}
```

Then use Ctrl+Shift+P → "Terminal: Create New Terminal With Profile" → "god-mode"

## Best Practices

1. **Use descriptive task IDs**: Include timestamp and agent name
2. **Monitor audit trail**: Keep audit pane visible for important operations
3. **Regular status checks**: Use the status pane to monitor agent health
4. **Clean up sessions**: Kill unused sessions to free resources
5. **Use zoom feature**: Ctrl-b + z to focus on specific pane

## Future Enhancements

- [ ] Web-based tmux viewer (ttyd integration)
- [ ] Automated layout templates
- [ ] Multi-project session management
- [ ] Integration with CI/CD pipelines
- [ ] Real-time metrics dashboard
- [ ] Session recording and replay