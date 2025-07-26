# GOD Mode Tmux Integration Design

## Overview
Tích hợp tmux vào GOD Mode để cung cấp giao diện multi-pane cho việc theo dõi và điều khiển các agent autonomous.

## Kiến trúc

### 1. Tmux Session Layout
```
┌─────────────────────────────────────┬─────────────────────────┐
│          Main Control Panel         │     Agent Status        │
│  - GOD Mode Status                  │  - Active Agents        │
│  - Task Queue                       │  - Token Usage          │
│  - Commands                         │  - Performance Metrics  │
├─────────────────────────────────────┼─────────────────────────┤
│       Architect Agent               │    Developer Agent      │
│  - Current Planning                 │  - Implementation       │
│  - Task Decomposition               │  - Code Generation      │
│  - Output Logs                      │  - Output Logs          │
├─────────────────────────────────────┼─────────────────────────┤
│          Audit Trail                │      MCP Server         │
│  - Real-time Audit Logs             │  - Server Status        │
│  - Token Usage                      │  - Active Connections   │
│  - Executed Commands                │  - Request/Response     │
└─────────────────────────────────────┴─────────────────────────┘
```

### 2. Components

#### TmuxOrchestrator Class
```python
class TmuxOrchestrator:
    def __init__(self, session_name="god-mode"):
        self.session_name = session_name
        self.panes = {}
        
    def create_session(self):
        """Create tmux session with predefined layout"""
        
    def create_pane(self, name: str, command: str):
        """Create a new pane for an agent"""
        
    def send_command(self, pane: str, command: str):
        """Send command to specific pane"""
        
    def capture_output(self, pane: str) -> str:
        """Capture output from pane"""
        
    def monitor_pane(self, pane: str, callback):
        """Monitor pane for changes"""
```

### 3. Integration Points

#### A. GOD Mode Startup
```python
# In god_mode.py
def enable_with_tmux(self):
    """Enable GOD mode with tmux interface"""
    if self.check_tmux_available():
        self.tmux = TmuxOrchestrator()
        self.tmux.create_session()
        self.tmux.create_layout()
    else:
        console.print("[yellow]Tmux not found, using standard mode[/yellow]")
```

#### B. Agent Execution
```python
# Each agent runs in its own pane
def execute_agent_in_tmux(self, agent_name: str, task: str):
    pane_id = self.tmux.create_pane(
        name=f"agent-{agent_name}",
        command=f"python -m claude_code_indexer.agents.{agent_name} --task '{task}'"
    )
    self.monitor_agent_output(pane_id, agent_name)
```

#### C. Real-time Monitoring
```python
# Monitor all panes for updates
async def monitor_all_agents(self):
    tasks = []
    for agent, pane_id in self.agent_panes.items():
        task = asyncio.create_task(
            self.monitor_pane_output(pane_id, agent)
        )
        tasks.append(task)
    await asyncio.gather(*tasks)
```

## Implementation Steps

### Phase 1: Basic Tmux Integration
1. **Tmux availability check**
   ```python
   def check_tmux_available() -> bool:
       return shutil.which('tmux') is not None
   ```

2. **Session management**
   ```python
   def create_god_mode_session():
       subprocess.run(['tmux', 'new-session', '-d', '-s', 'god-mode'])
   ```

3. **Layout creation**
   ```python
   def create_layout():
       # Create 6-pane layout
       commands = [
           'tmux split-window -h -p 30',  # Split for status
           'tmux split-window -v -p 66',  # Split for agents
           'tmux split-window -v -p 50',  # Split for audit
           'tmux select-pane -t 0',
           'tmux split-window -v -p 66',  # Split main
           'tmux split-window -v -p 50',  # Split for developer
       ]
   ```

### Phase 2: Agent Integration
1. **Agent wrapper scripts**
   ```python
   # agents/architect.py
   class ArchitectAgent:
       def __init__(self, pane_id: str):
           self.pane_id = pane_id
           self.output_file = f"/tmp/god-mode-{pane_id}.log"
   ```

2. **Output capturing**
   ```python
   def capture_and_parse_output(pane_id: str):
       output = subprocess.check_output([
           'tmux', 'capture-pane', '-t', pane_id, '-p'
       ])
       return parse_agent_output(output)
   ```

### Phase 3: Interactive Features
1. **Command routing**
   ```python
   def route_command_to_agent(agent: str, command: str):
       pane_id = self.agent_panes[agent]
       subprocess.run([
           'tmux', 'send-keys', '-t', pane_id, command, 'Enter'
       ])
   ```

2. **Status dashboard**
   ```python
   def update_status_pane():
       status = generate_status_report()
       write_to_pane(self.status_pane, status)
   ```

## Commands

### New CLI Commands
```bash
# Start GOD mode with tmux
claude-code-indexer god-mode start --tmux

# Attach to existing session
claude-code-indexer god-mode attach

# Send command to specific agent
claude-code-indexer god-mode send --agent architect --command "analyze project structure"

# View agent output
claude-code-indexer god-mode logs --agent developer --tail 50
```

### Tmux Key Bindings
```
Ctrl-b + g : Switch to GOD mode session
Ctrl-b + 1-6 : Switch between panes
Ctrl-b + s : Show session list
Ctrl-b + d : Detach from session
```

## Benefits

1. **Multi-tasking**: Các agent chạy song song trong các pane riêng
2. **Real-time monitoring**: Theo dõi output của tất cả agents cùng lúc
3. **Persistence**: Session vẫn chạy ngay cả khi disconnect
4. **Interactive control**: Có thể tương tác trực tiếp với từng agent
5. **Visual feedback**: Thấy rõ trạng thái và tiến độ của mỗi agent

## Security Considerations

1. **Session isolation**: Mỗi GOD mode session có namespace riêng
2. **Permission control**: Chỉ user tạo session mới có quyền attach
3. **Audit logging**: Tất cả commands được log với timestamp
4. **Resource limits**: Giới hạn số lượng panes và memory usage

## Configuration

```yaml
# god-mode-config.yaml
tmux:
  enabled: true
  session_name: "god-mode"
  layout: "6-pane"  # or "4-pane", "custom"
  pane_config:
    main_control:
      size: "40%"
      command: "claude-code-indexer god-mode monitor"
    architect:
      size: "30%"
      command: "claude-code-indexer agent architect --watch"
    developer:
      size: "30%"
      command: "claude-code-indexer agent developer --watch"
  key_bindings:
    switch_agent: "Ctrl-b g"
    emergency_stop: "Ctrl-b x"
```

## Error Handling

1. **Tmux not installed**: Fallback to standard CLI mode
2. **Session conflicts**: Auto-generate unique session names
3. **Pane crashes**: Auto-restart với exponential backoff
4. **Output overflow**: Rotate logs và archive old outputs

## Future Enhancements

1. **Web UI**: Tmux session accessible via web browser (using gotty/ttyd)
2. **Recording**: Record sessions for replay and analysis
3. **Multi-user**: Multiple users can view (read-only) same session
4. **AI-powered layout**: Tự động adjust layout based on workload
5. **Integration with VSCode**: Embed tmux panes in VSCode terminal