#!/usr/bin/env python3
"""Demo script for GOD Mode Tmux Integration."""
import asyncio
import time
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_code_indexer.commands.tmux_orchestrator import TmuxOrchestrator
from rich.console import Console

console = Console()


async def demo_tmux_god_mode():
    """Demonstrate GOD Mode with tmux integration."""
    console.print("[bold cyan]🚀 GOD Mode Tmux Integration Demo[/bold cyan]\n")
    
    # Create orchestrator
    orchestrator = TmuxOrchestrator("god-mode-demo")
    
    # Check tmux availability
    if not orchestrator.check_tmux_available():
        console.print("[red]❌ Tmux is not installed![/red]")
        console.print("Please install tmux:")
        console.print("  Ubuntu/Debian: sudo apt-get install tmux")
        console.print("  macOS: brew install tmux")
        return
    
    # Kill any existing session
    orchestrator.kill_session()
    
    # Create new session
    console.print("📦 Creating tmux session...")
    if not orchestrator.create_session():
        console.print("[red]Failed to create session[/red]")
        return
    
    # Create layout
    console.print("🎨 Setting up 6-pane layout...")
    if not orchestrator.create_layout():
        console.print("[red]Failed to create layout[/red]")
        return
    
    console.print("[green]✓ Layout created successfully![/green]\n")
    
    # Demonstrate pane interactions
    console.print("🎭 Running demo tasks...\n")
    
    # Update status pane
    orchestrator.update_status_pane()
    
    # Execute tasks in different agents
    tasks = [
        ("architect", "Design a REST API for user management"),
        ("developer", "Implement user authentication module"),
        ("architect", "Review security considerations"),
        ("developer", "Add unit tests for auth module")
    ]
    
    for agent, task in tasks:
        console.print(f"📋 Sending to {agent}: {task}")
        task_id = orchestrator.execute_agent_task(agent, task)
        console.print(f"   └─ Task ID: {task_id}")
        time.sleep(1)
        
        # Update status after each task
        orchestrator.update_status_pane()
    
    # Demonstrate audit logging
    console.print("\n📝 Writing to audit trail...")
    orchestrator.send_command("audit", "echo '📝 New audit entry: Task execution started'")
    orchestrator.send_command("audit", "echo '✅ All agents initialized successfully'")
    orchestrator.send_command("audit", "echo '🔍 Monitoring agent activities...'")
    
    # Show MCP server status
    console.print("\n🔌 Updating MCP server status...")
    orchestrator.send_command("mcp", "echo '🟢 MCP Server: Active'")
    orchestrator.send_command("mcp", "echo 'Connections: 2'")
    orchestrator.send_command("mcp", "echo 'Requests handled: 42'")
    
    # Final status update
    time.sleep(2)
    orchestrator.update_status_pane()
    
    # Get and display status report
    console.print("\n📊 Final Status Report:")
    status = orchestrator.get_status_report()
    for agent, info in status['agents'].items():
        if agent != 'status':
            state = "🟢 Active" if info['active'] else "⭕ Idle"
            console.print(f"  {agent}: {state}")
    
    console.print("\n" + "="*60)
    console.print("[bold green]✅ Demo completed![/bold green]")
    console.print("\n[cyan]To interact with the session:[/cyan]")
    console.print(f"  tmux attach -t {orchestrator.session_name}")
    console.print("\n[yellow]To kill the session:[/yellow]")
    console.print(f"  tmux kill-session -t {orchestrator.session_name}")
    console.print("="*60)


async def monitor_demo():
    """Demonstrate monitoring capabilities."""
    orchestrator = TmuxOrchestrator("god-mode-demo")
    
    if not orchestrator.session_exists():
        console.print("[red]No demo session found. Run the demo first![/red]")
        return
    
    console.print("[cyan]📡 Starting monitor mode...[/cyan]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")
    
    def on_architect_change(output):
        lines = output.strip().split('\n')
        if lines and len(lines) > 2:
            last_line = lines[-1]
            if last_line and not last_line.startswith("Waiting"):
                console.print(f"[blue]🏗️ Architect: {last_line[:60]}...[/blue]")
    
    def on_developer_change(output):
        lines = output.strip().split('\n')
        if lines and len(lines) > 2:
            last_line = lines[-1]
            if last_line and not last_line.startswith("Waiting"):
                console.print(f"[green]💻 Developer: {last_line[:60]}...[/green]")
    
    # Start monitoring
    tasks = [
        orchestrator.monitor_pane("architect", on_architect_change, interval=0.5),
        orchestrator.monitor_pane("developer", on_developer_change, interval=0.5)
    ]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped[/yellow]")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        asyncio.run(monitor_demo())
    else:
        asyncio.run(demo_tmux_god_mode())