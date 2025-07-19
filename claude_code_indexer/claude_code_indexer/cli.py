#!/usr/bin/env python3
"""
Command-line interface for Claude Code Indexer
"""

import click
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.text import Text

from .indexer import CodeGraphIndexer
from .updater import Updater, check_and_notify_update
from . import __version__
from .security import validate_file_path, SecurityError


console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """Claude Code Indexer - Index source code as graph database"""
    pass


@cli.command()
@click.option('--force', is_flag=True, help='Force overwrite existing files')
def init(force):
    """Initialize Claude Code Indexer in current directory"""
    cwd = Path.cwd()
    claude_md_path = cwd / "CLAUDE.md"
    
    console.print("🚀 [bold blue]Initializing Claude Code Indexer...[/bold blue]")
    
    # Check if CLAUDE.md exists
    if claude_md_path.exists():
        console.print(f"✓ Found existing CLAUDE.md at {claude_md_path}")
        
        # Read existing content
        with open(claude_md_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Check if our section already exists
        if "## Code Indexing with Graph Database" in existing_content:
            if not force:
                console.print("⚠️  Code indexing section already exists in CLAUDE.md")
                console.print("Use --force to overwrite, or manually remove the section")
                return
            else:
                console.print("🔄 Updating existing section...")
                # Remove existing section
                lines = existing_content.split('\n')
                new_lines = []
                skip_section = False
                
                for line in lines:
                    if line.strip() == "## Code Indexing with Graph Database":
                        skip_section = True
                        continue
                    elif skip_section and line.startswith("## ") and "Code Indexing" not in line:
                        skip_section = False
                        new_lines.append(line)
                    elif not skip_section:
                        new_lines.append(line)
                
                existing_content = '\n'.join(new_lines)
        
        # Append our template
        template_path = Path(__file__).parent / "templates" / "claude_md_template.md"
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Combine content
        updated_content = existing_content.rstrip() + '\n\n' + template_content
        
        # Write back
        with open(claude_md_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        console.print("✓ Updated CLAUDE.md with code indexing instructions")
    
    else:
        console.print("⚠️  CLAUDE.md not found")
        create_new = click.confirm("Create new CLAUDE.md with code indexing setup?")
        
        if create_new:
            # Create new CLAUDE.md with basic structure
            template_path = Path(__file__).parent / "templates" / "claude_md_template.md"
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            basic_header = """# Claude Coding Assistant - Setup Rules

## Core Workflow Rules

1. **First think through the problem**, read the codebase for relevant files, and write a plan.
2. **Make every task and code change as simple as possible**.
3. **Prioritize simplicity over complexity**.

"""
            
            full_content = basic_header + template_content
            
            with open(claude_md_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            console.print(f"✓ Created new CLAUDE.md at {claude_md_path}")
        else:
            console.print("❌ Initialization cancelled")
            return
    
    # Create initial database in centralized storage
    from .storage_manager import get_storage_manager
    storage = get_storage_manager()
    project_path = storage.get_project_from_cwd()
    
    indexer = CodeGraphIndexer(project_path=project_path)
    console.print(f"✓ Initialized code index database in {storage.app_home}")
    
    # Create .gitignore entry
    gitignore_path = cwd / ".gitignore"
    gitignore_entry = "code_index.db"
    
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        
        if gitignore_entry not in gitignore_content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write(f"\n# Claude Code Indexer\n{gitignore_entry}\n")
            console.print("✓ Added code_index.db to .gitignore")
    else:
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(f"# Claude Code Indexer\n{gitignore_entry}\n")
        console.print("✓ Created .gitignore with code_index.db")
    
    console.print("\n🎉 [bold green]Initialization complete![/bold green]")
    console.print("Next steps:")
    console.print("1. Run [bold]claude-code-indexer index .[/bold] to index current directory")
    console.print("2. Run [bold]claude-code-indexer query --important[/bold] to see key components")
    console.print("3. Run [bold]claude-code-indexer stats[/bold] to view indexing statistics")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--patterns', default=None, 
              help='File patterns to index (comma-separated) [default: auto-detect from supported languages]')
@click.option('--db', default=None, help='Database file path (default: centralized storage)')
@click.option('--no-cache', is_flag=True, help='Disable caching for faster re-indexing')
@click.option('--force', is_flag=True, help='Force re-index all files (ignore cache)')
@click.option('--workers', type=int, help='Number of parallel workers (default: auto)')
@click.option('--no-optimize', is_flag=True, help='Disable database optimizations')
@click.option('--benchmark', is_flag=True, help='Run performance benchmark')
@click.option('--custom-ignore', multiple=True, help='Additional ignore patterns (can be used multiple times)')
@click.option('--show-ignored', is_flag=True, help='Show what patterns are being ignored')
@click.option('--verbose', is_flag=True, help='Show detailed parsing progress and errors')
def index(path, patterns, db, no_cache, force, workers, no_optimize, benchmark, custom_ignore, show_ignored, verbose):
    """Index source code in the specified directory with performance optimizations"""
    # Validate path for security
    try:
        safe_path = validate_file_path(path)
    except SecurityError as e:
        console.print(f"❌ [red]Security error: {e}[/red]")
        sys.exit(1)
    
    console.print(f"📁 [bold blue]Indexing code in {safe_path}...[/bold blue]")
    
    # Parse patterns - use None to auto-detect from supported languages
    pattern_list = None if patterns is None else [p.strip() for p in patterns.split(',')]
    
    # Show performance settings
    if not no_cache:
        console.print("💾 [green]Caching enabled[/green] - unchanged files will be skipped")
    if not no_optimize:
        console.print("🚀 [green]Database optimizations enabled[/green] - using APSW and connection pooling")
    if workers:
        console.print(f"⚡ [green]Parallel processing enabled[/green] - using {workers} workers")
    elif not no_optimize:
        console.print("⚡ [green]Auto parallel processing enabled[/green] - workers will be determined automatically")
    
    # Show ignore patterns if requested
    if show_ignored:
        from .ignore_handler import IgnoreHandler
        ignore_handler = IgnoreHandler(path, list(custom_ignore) if custom_ignore else None)
        console.print("\n📝 [bold blue]Active Ignore Patterns:[/bold blue]")
        patterns = ignore_handler.get_patterns()
        console.print(f"Total patterns: {len(patterns)}")
        console.print("\nTop patterns:")
        for pattern in patterns[:20]:
            console.print(f"  • {pattern}")
        if len(patterns) > 20:
            console.print(f"  ... and {len(patterns) - 20} more")
        console.print()
    
    # Run benchmark if requested
    if benchmark:
        from .db_optimizer import DatabaseBenchmark
        console.print("🔥 [yellow]Running performance benchmark...[/yellow]")
        DatabaseBenchmark.benchmark_insert_performance(db + "_benchmark")
    
    # Create indexer with performance options
    project_path = Path(safe_path).resolve()
    indexer = CodeGraphIndexer(
        db_path=db,  # Can be None to use centralized storage
        use_cache=not no_cache,
        parallel_workers=workers,
        enable_optimizations=not no_optimize,
        project_path=project_path
    )
    
    # Index with progress
    with Progress() as progress:
        task = progress.add_task("Indexing files...", total=None)
        
        try:
            # Pass verbose flag to indexer
            indexer.verbose = verbose
            indexer.index_directory(safe_path, patterns=pattern_list, force_reindex=force, 
                                  custom_ignore=list(custom_ignore) if custom_ignore else None)
            progress.update(task, completed=100)
            
            # Show parsing errors if verbose mode
            if verbose and hasattr(indexer, 'parsing_errors') and indexer.parsing_errors:
                console.print("\n⚠️  [yellow]Parsing Warnings:[/yellow]")
                for error in indexer.parsing_errors[:10]:  # Show first 10 errors
                    console.print(f"  • {error}")
                if len(indexer.parsing_errors) > 10:
                    console.print(f"  ... and {len(indexer.parsing_errors) - 10} more")
                    
        except Exception as e:
            console.print(f"❌ [bold red]Error during indexing: {e}[/bold red]")
            if verbose:
                import traceback
                console.print("[dim]" + traceback.format_exc() + "[/dim]")
            sys.exit(1)
    
    console.print(f"✅ [bold green]Indexing complete![/bold green]")


@cli.command()
@click.option('--important', is_flag=True, help='Show only important nodes')
@click.option('--type', help='Filter by node type (file, class, method, function)')
@click.option('--limit', default=20, help='Maximum number of results')
@click.option('--db', default=None, help='Database file path (default: centralized storage)')
@click.option('--project', help='Project name/path to query (default: current directory)')
def query(important, type, limit, db, project):
    """Query indexed code entities"""
    # Determine project path
    from .storage_manager import get_storage_manager
    storage = get_storage_manager()
    
    if project:
        # Find project by name or path
        project_info = storage.find_project_by_name(project)
        if project_info:
            project_path = Path(project_info['path'])
        else:
            project_path = Path(project).resolve()
    else:
        project_path = storage.get_project_from_cwd()
    
    # Create indexer with project path
    indexer = CodeGraphIndexer(db_path=db, project_path=project_path)
    
    # Check if database exists
    actual_db_path = db or indexer.db_path
    if not os.path.exists(actual_db_path):
        console.print(f"❌ [bold red]Database not found for {project_path}. Run 'claude-code-indexer index' first.[/bold red]")
        sys.exit(1)
    
    if important:
        console.print("🔍 [bold blue]Most important code entities:[/bold blue]")
        # Get all nodes first, then take top by importance
        all_nodes = indexer.query_important_nodes(min_score=0.0, limit=1000)
        
        # Sort by importance score, but prioritize classes and functions
        def sort_key(node):
            type_priority = {
                'class': 1000,
                'function': 100,
                'method': 10,
                'file': 1,
                'import': 0
            }.get(node['node_type'], 0)
            return node['importance_score'] + type_priority
        
        # Sort by combined score and take top N
        nodes = sorted(all_nodes, key=sort_key, reverse=True)[:limit]
    else:
        console.print("📋 [bold blue]All code entities:[/bold blue]")
        nodes = indexer.query_important_nodes(min_score=0.0, limit=limit)
    
    if type:
        nodes = [n for n in nodes if n['node_type'] == type]
    
    if not nodes:
        if important:
            console.print("⚠️  No high-importance entities found. Showing top entities by score...")
            # Fallback: get any nodes sorted by importance
            nodes = indexer.query_important_nodes(min_score=0.0, limit=limit)
            if nodes:
                console.print(f"ℹ️  Highest score: {nodes[0]['importance_score']:.3f}")
        else:
            console.print("No entities found matching criteria.")
            return
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Importance", style="green")
    table.add_column("Tags", style="yellow")
    table.add_column("Path", style="dim")
    
    for node in nodes:
        importance = f"{node['importance_score']:.3f}"
        tags = ", ".join(node['relevance_tags']) if node['relevance_tags'] else "-"
        table.add_row(
            node['name'],
            node['node_type'],
            importance,
            tags,
            node['path']
        )
    
    console.print(table)


@cli.command()
@click.argument('terms', nargs=-1, required=True)
@click.option('--db', default=None, help='Database file path (default: centralized storage)')
@click.option('--mode', type=click.Choice(['any', 'all']), default='any', help='Search mode: any (OR) or all (AND)')
@click.option('--limit', default=20, help='Maximum number of results')
@click.option('--type', type=click.Choice(['file', 'class', 'method', 'function', 'import', 'interface']), 
              help='Filter by node type')
@click.option('--project', help='Project name/path to search (default: current directory)')
def search(terms, db, mode, limit, type, project):
    """Search for code entities by name. Supports multiple keywords.
    
    Examples:
        claude-code-indexer search auth
        claude-code-indexer search auth user login --mode any
        claude-code-indexer search database connection --mode all
        claude-code-indexer search service firestore --type class --limit 10
        claude-code-indexer search process --type function
    """
    # Determine project path
    from .storage_manager import get_storage_manager
    storage = get_storage_manager()
    
    if project:
        # Find project by name or path
        project_info = storage.find_project_by_name(project)
        if project_info:
            project_path = Path(project_info['path'])
        else:
            project_path = Path(project).resolve()
    else:
        project_path = storage.get_project_from_cwd()
    
    # Create indexer with project path
    indexer = CodeGraphIndexer(db_path=db, project_path=project_path)
    
    # Check if database exists
    actual_db_path = db or indexer.db_path
    if not os.path.exists(actual_db_path):
        console.print(f"❌ [bold red]Database not found for {project_path}. Run 'claude-code-indexer index' first.[/bold red]")
        sys.exit(1)
    
    import sqlite3
    conn = sqlite3.connect(actual_db_path)
    cursor = conn.cursor()
    
    # Build query based on mode
    if mode == 'any':
        # OR logic - match any keyword
        conditions = []
        params = []
        for term in terms:
            conditions.append("(name LIKE ? OR path LIKE ? OR summary LIKE ?)")
            params.extend([f'%{term}%', f'%{term}%', f'%{term}%'])
        where_clause = " OR ".join(conditions)
    else:
        # AND logic - must match all keywords
        conditions = []
        params = []
        for term in terms:
            conditions.append("(name LIKE ? OR path LIKE ? OR summary LIKE ?)")
            params.extend([f'%{term}%', f'%{term}%', f'%{term}%'])
        where_clause = " AND ".join(conditions)
    
    # Add type filter if specified
    where_conditions = [f"({where_clause})"]
    if type:
        where_conditions.append("node_type = ?")
        params.append(type)
    
    final_where_clause = " AND ".join(where_conditions)
    
    query = f'''
    SELECT name, node_type, path, importance_score, relevance_tags
    FROM code_nodes
    WHERE {final_where_clause}
    ORDER BY importance_score DESC
    LIMIT {limit}
    '''
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    search_desc = ' '.join(terms)
    filter_desc = f"mode: {mode}"
    if type:
        filter_desc += f", type: {type}"
    
    if not results:
        console.print(f"No entities found matching '{search_desc}' ({filter_desc})")
        return
    
    console.print(f"🔍 [bold blue]Search results for '{search_desc}' ({filter_desc}):[/bold blue]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Importance", style="green")
    table.add_column("Path", style="dim")
    
    for name, node_type, path, importance, tags in results:
        table.add_row(
            name,
            node_type,
            f"{importance:.3f}",
            path
        )
    
    console.print(table)


@cli.command()
@click.option('--db', default=None, help='Database file path (default: centralized storage)')
@click.option('--cache', is_flag=True, help='Show cache statistics')
@click.option('--project', help='Project name/path for stats (default: current directory)')
def stats(db, cache, project):
    """Show indexing statistics"""
    # Determine project path
    from .storage_manager import get_storage_manager
    storage = get_storage_manager()
    
    if project:
        # Find project by name or path
        project_info = storage.find_project_by_name(project)
        if project_info:
            project_path = Path(project_info['path'])
        else:
            project_path = Path(project).resolve()
    else:
        project_path = storage.get_project_from_cwd()
    
    # Create indexer with project path
    indexer = CodeGraphIndexer(db_path=db, project_path=project_path)
    
    # Check if database exists
    actual_db_path = db or indexer.db_path
    if not os.path.exists(actual_db_path):
        console.print(f"❌ [bold red]Database not found for {project_path}. Run 'claude-code-indexer index' first.[/bold red]")
        sys.exit(1)
    
    # Show cache stats if requested
    if cache:
        from .cache_manager import CacheManager
        cache_manager = CacheManager(project_path=project_path)
        cache_manager.print_cache_stats()
        console.print()  # Add spacing
    stats = indexer.get_stats()
    
    console.print("📊 [bold blue]Code Indexing Statistics[/bold blue]")
    
    # Basic stats
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Metric", style="cyan")
    info_table.add_column("Value", style="bold green")
    
    info_table.add_row("Last indexed", stats.get('last_indexed', 'Never'))
    info_table.add_row("Total nodes", stats.get('total_nodes', '0'))
    info_table.add_row("Total edges", stats.get('total_edges', '0'))
    
    console.print(info_table)
    
    # Node types
    if 'node_types' in stats:
        console.print("\n📋 [bold blue]Node Types:[/bold blue]")
        type_table = Table(show_header=True, header_style="bold magenta")
        type_table.add_column("Type", style="cyan")
        type_table.add_column("Count", style="bold green")
        
        for node_type, count in stats['node_types'].items():
            type_table.add_row(node_type, str(count))
        
        console.print(type_table)
    
    # Relationship types
    if 'relationship_types' in stats:
        console.print("\n🔗 [bold blue]Relationship Types:[/bold blue]")
        rel_table = Table(show_header=True, header_style="bold magenta")
        rel_table.add_column("Type", style="cyan")
        rel_table.add_column("Count", style="bold green")
        
        for rel_type, count in stats['relationship_types'].items():
            rel_table.add_row(rel_type, str(count))
        
        console.print(rel_table)


@cli.command()
@click.option('--clear', is_flag=True, help='Clear old cache entries (older than 30 days)')
@click.option('--days', type=int, default=30, help='Days threshold for clearing cache')
def cache(clear, days):
    """Manage indexing cache for faster re-indexing"""
    from .cache_manager import CacheManager
    
    cache_manager = CacheManager()
    
    if clear:
        console.print(f"🗑️ [yellow]Clearing cache entries older than {days} days...[/yellow]")
        cache_manager.clear_cache(older_than_days=days)
        console.print("✅ [green]Cache cleared successfully![/green]")
    
    console.print("💾 [bold blue]Cache Statistics[/bold blue]")
    cache_manager.print_cache_stats()


@cli.command()
@click.option('--records', type=int, default=1000, help='Number of test records')
def benchmark(records):
    """Run performance benchmarks"""
    from .db_optimizer import DatabaseBenchmark
    
    console.print(f"🔥 [bold blue]Running performance benchmark with {records} records...[/bold blue]")
    
    sqlite3_time, optimized_time = DatabaseBenchmark.benchmark_insert_performance(
        "benchmark_test.db", num_records=records
    )
    
    console.print(f"\n📊 [bold blue]Benchmark Results:[/bold blue]")
    
    benchmark_table = Table(show_header=True, header_style="bold magenta")
    benchmark_table.add_column("Database Type", style="cyan")
    benchmark_table.add_column("Time (seconds)", style="bold green")
    benchmark_table.add_column("Records/second", style="bold yellow")
    
    benchmark_table.add_row("Standard SQLite3", f"{sqlite3_time:.2f}", f"{records/sqlite3_time:.0f}")
    benchmark_table.add_row("Optimized APSW", f"{optimized_time:.2f}", f"{records/optimized_time:.0f}")
    
    console.print(benchmark_table)
    
    speedup = sqlite3_time / optimized_time
    console.print(f"\n🚀 [bold green]Speedup: {speedup:.1f}x faster with optimizations![/bold green]")


@cli.command()
@click.option('--check-only', is_flag=True, help='Only check for updates without installing')
def update(check_only):
    """Check for and install updates"""
    updater = Updater()
    
    if check_only:
        updater.auto_update(check_only=True)
    else:
        if updater.auto_update(check_only=False):
            # Also sync CLAUDE.md after update
            updater.sync_claude_md()
            console.print("\n🎉 [bold green]Update complete![/bold green]")


@cli.group()
def background():
    """Manage background indexing service"""
    pass


@background.command()
def start():
    """Start the background indexing service"""
    from .background_service import get_background_service
    
    service = get_background_service()
    service.start()
    
    if service.is_running():
        console.print("✅ [green]Background indexing service started successfully![/green]")
    else:
        console.print("❌ [red]Failed to start background indexing service[/red]")


@background.command()
def stop():
    """Stop the background indexing service"""
    from .background_service import get_background_service
    
    service = get_background_service()
    service.stop()
    console.print("✅ [green]Background indexing service stopped[/green]")


@background.command()
def restart():
    """Restart the background indexing service"""
    from .background_service import get_background_service
    
    service = get_background_service()
    service.restart()
    console.print("✅ [green]Background indexing service restarted[/green]")


@background.command()
def status():
    """Show background indexing service status"""
    from .background_service import get_background_service
    
    service = get_background_service()
    status = service.get_status()
    
    console.print("\n📊 [bold blue]Background Indexing Service Status[/bold blue]\n")
    
    # General status
    console.print(f"Enabled: {'✅ Yes' if status['enabled'] else '❌ No'}")
    console.print(f"Running: {'✅ Yes' if status['running'] else '❌ No'}")
    console.print(f"Default interval: {status['default_interval']}s ({status['default_interval'] / 60:.1f} minutes)")
    
    if status['projects']:
        console.print("\n📁 [bold blue]Project Status:[/bold blue]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Project", style="cyan")
        table.add_column("Interval", style="green")
        table.add_column("Last Indexed", style="yellow")
        table.add_column("Next Index", style="blue")
        table.add_column("Status", style="bold")
        
        for project_path, project_status in status['projects'].items():
            interval_str = f"{project_status['interval']}s" if project_status['interval'] > 0 else "Disabled"
            status_str = "🔄 Indexing..." if project_status['indexing'] else "⏸️  Waiting"
            
            # Show full path for managed projects
            project_display = project_path if len(project_path) < 40 else "..." + project_path[-37:]
            
            table.add_row(
                project_display,
                interval_str,
                project_status['last_indexed'][:16] + "…" if len(project_status['last_indexed']) > 16 else project_status['last_indexed'],
                project_status['next_index'][:16] + "…" if len(project_status['next_index']) > 16 else project_status['next_index'],
                status_str
            )
        
        console.print(table)
    else:
        console.print("\n[dim]No projects configured for background indexing[/dim]")


@background.command()
@click.option('--enable/--disable', default=True, help='Enable or disable the service')
def config(enable):
    """Enable or disable background indexing service"""
    from .background_service import get_background_service
    
    service = get_background_service()
    
    if enable:
        service.enable()
        console.print("✅ [green]Background indexing service enabled[/green]")
    else:
        service.disable()
        console.print("❌ [yellow]Background indexing service disabled[/yellow]")


@background.command()
@click.option('--project', help='Project path (default: current directory)')
@click.option('--interval', type=int, default=300, help='Interval in seconds (default: 300, -1 to disable)')
def set_interval(project, interval):
    """Set background indexing interval for a project"""
    from .background_service import get_background_service
    from .storage_manager import get_storage_manager
    
    service = get_background_service()
    
    if project:
        # Set for specific project
        project_path = Path(project).resolve()
        if not project_path.exists():
            console.print(f"❌ [red]Project path does not exist: {project}[/red]")
            return
        
        service.set_project_interval(str(project_path), interval)
        
        if interval == -1:
            console.print(f"❌ [yellow]Disabled background indexing for {project_path}[/yellow]")
        else:
            console.print(f"✅ [green]Set background indexing interval to {interval}s for {project_path}[/green]")
    else:
        # Set default interval
        service.set_default_interval(interval)
        console.print(f"✅ [green]Set default background indexing interval to {interval}s[/green]")
def sync():
    """Sync CLAUDE.md with latest template"""
    updater = Updater()
    if updater.sync_claude_md(force=True):
        console.print("✅ [bold green]CLAUDE.md synchronized![/bold green]")
    else:
        console.print("✓ CLAUDE.md is already up to date")


@cli.group()
def mcp():
    """MCP (Model Context Protocol) management commands"""
    pass


@mcp.command("install")
@click.option("--force", is_flag=True, help="Force installation even if Claude Desktop not found")
def mcp_install(force):
    """Install MCP server for Claude Desktop integration"""
    from .mcp_installer import install_mcp
    install_mcp(force=force)


@mcp.command("uninstall")
def mcp_uninstall():
    """Remove MCP server from Claude Desktop"""
    from .mcp_installer import uninstall_mcp
    uninstall_mcp()


@mcp.command("status")
def mcp_status():
    """Show MCP installation status"""
    from .mcp_installer import show_mcp_status
    show_mcp_status()


@cli.command()
@click.option('--all', is_flag=True, help='Show all projects including non-existent')
def projects(all):
    """List all indexed projects"""
    from .storage_manager import get_storage_manager
    storage = get_storage_manager()
    
    projects = storage.list_projects()
    
    if not projects:
        console.print("📭 [yellow]No indexed projects found.[/yellow]")
        console.print("Run 'claude-code-indexer index <path>' to index a project.")
        return
    
    console.print("📚 [bold blue]Indexed Projects[/bold blue]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Path", style="green")
    table.add_column("Last Indexed", style="yellow")
    table.add_column("Size", style="blue")
    table.add_column("Status", style="white")
    
    for project in projects:
        if not all and not project.get('exists', True):
            continue
            
        name = project['name']
        path = project['path']
        last_indexed = project.get('last_indexed', 'Never')
        if last_indexed and last_indexed != 'Never':
            # Format date nicely
            from datetime import datetime
            dt = datetime.fromisoformat(last_indexed)
            last_indexed = dt.strftime('%Y-%m-%d %H:%M')
        
        size = project.get('db_size', 0)
        size_str = f"{size / 1024 / 1024:.1f} MB" if size > 0 else "-"
        
        status = "✓" if project.get('exists', True) else "✗ Missing"
        
        table.add_row(name, path, last_indexed, size_str, status)
    
    console.print(table)
    
    # Show storage stats
    stats = storage.get_storage_stats()
    console.print(f"\n💾 Storage: {stats['app_home']}")
    console.print(f"   Total projects: {stats['project_count']}")
    console.print(f"   Total size: {stats['total_size_mb']:.1f} MB")


@cli.command()
@click.argument('project', required=True)
@click.option('--force', is_flag=True, help='Force removal without confirmation')
def remove(project, force):
    """Remove an indexed project"""
    from .storage_manager import get_storage_manager
    storage = get_storage_manager()
    
    # Find project
    project_info = storage.find_project_by_name(project)
    if not project_info:
        # Try as path
        project_path = Path(project).resolve()
        if storage.get_project_id(project_path) in storage.metadata['projects']:
            project_info = {
                'path': str(project_path),
                'name': project_path.name
            }
        else:
            console.print(f"❌ [bold red]Project '{project}' not found.[/bold red]")
            return
    
    # Confirm
    if not force:
        confirm = click.confirm(f"Remove index for '{project_info['name']}' ({project_info['path']})?")
        if not confirm:
            console.print("❌ Removal cancelled.")
            return
    
    # Remove
    removed = storage.remove_project(Path(project_info['path']))
    if removed:
        console.print(f"✅ [bold green]Removed index for '{project_info['name']}'[/bold green]")
    else:
        console.print(f"❌ [bold red]Failed to remove project.[/bold red]")


@cli.command()
def clean():
    """Clean up orphaned project indexes"""
    from .storage_manager import get_storage_manager
    storage = get_storage_manager()
    
    console.print("🔍 [bold blue]Scanning for orphaned projects...[/bold blue]")
    
    removed = storage.clean_orphaned_projects()
    
    if removed:
        console.print(f"✅ [bold green]Cleaned {len(removed)} orphaned projects:[/bold green]")
        for path in removed:
            console.print(f"   • {path}")
    else:
        console.print("✨ [green]No orphaned projects found.[/green]")


def main():
    """Main CLI entry point"""
    # Check for updates on startup (non-blocking)
    check_and_notify_update()
    cli()


if __name__ == "__main__":
    main()