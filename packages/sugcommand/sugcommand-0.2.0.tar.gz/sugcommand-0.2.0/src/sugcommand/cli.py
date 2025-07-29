"""
Command Line Interface for sugcommand.
"""

import sys
import time
import logging
import subprocess
import threading
import os
from pathlib import Path
from typing import Optional

import click
from .core import SuggestionEngine, ConfigManager
from .utils.display import SuggestionFormatter, ColorScheme
from .utils.performance import get_performance_summary
from .integrations.realtime_daemon import RealtimeDaemon, DaemonClient
from .integrations.bash_integration import BashIntegration
from .integrations.zsh_integration import ZshIntegration
from .integrations.fish_integration import FishIntegration

# Setup logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@click.group(invoke_without_command=True)
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--config-dir', type=click.Path(), help='Custom configuration directory')
@click.pass_context
def main(ctx: click.Context, debug: bool, config_dir: Optional[str]) -> None:
    """
    SugCommand - Intelligent terminal command suggestion tool.
    
    Provides intelligent command suggestions based on available system commands
    and command history analysis.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Setup context
    ctx.ensure_object(dict)
    
    # Initialize configuration
    config_path = Path(config_dir) if config_dir else None
    ctx.obj['config'] = ConfigManager(config_path)
    ctx.obj['formatter'] = SuggestionFormatter(
        color_enabled=ctx.obj['config'].is_color_enabled(),
        compact_mode=ctx.obj['config'].get('compact_display', False),
        show_confidence=ctx.obj['config'].get('show_confidence', False),
        show_source=ctx.obj['config'].get('show_source', False)
    )
    
    # If no subcommand is provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.argument('input_text', required=False)
@click.option('--limit', '-l', default=None, type=int, help='Maximum number of suggestions')
@click.option('--compact', '-c', is_flag=True, help='Use compact display format')
@click.option('--show-confidence', is_flag=True, help='Show confidence scores')
@click.option('--show-source', is_flag=True, help='Show suggestion sources')
@click.option('--no-color', is_flag=True, help='Disable colored output')
@click.pass_context
def suggest(ctx: click.Context, 
           input_text: Optional[str],
           limit: Optional[int],
           compact: bool,
           show_confidence: bool,
           show_source: bool,
           no_color: bool) -> None:
    """Get command suggestions for the given input text."""
    
    config: ConfigManager = ctx.obj['config']
    
    if not config.is_enabled():
        formatter = ctx.obj['formatter']
        click.echo(formatter.format_warning("Command suggestions are disabled. Use 'sugcommand enable' to enable them."))
        sys.exit(1)
    
    # Get input text
    if not input_text:
        try:
            input_text = click.prompt("Enter command text", type=str)
        except click.Abort:
            click.echo("\nAborted.")
            sys.exit(0)
    
    if not input_text.strip():
        click.echo("No input provided.")
        sys.exit(1)
    
    # Setup formatter with overrides
    formatter = SuggestionFormatter(
        color_enabled=not no_color and config.is_color_enabled(),
        compact_mode=compact or config.get('compact_display', False),
        show_confidence=show_confidence or config.get('show_confidence', False),
        show_source=show_source or config.get('show_source', False)
    )
    
    try:
        # Try daemon first, fallback to direct engine
        client = DaemonClient()
        suggestions_data = client.get_suggestions(input_text)
        
        if suggestions_data:
            # Convert daemon response to suggestion objects
            from .core.suggestion_engine import SuggestionResult
            suggestions = []
            for s in suggestions_data:
                suggestions.append(SuggestionResult(
                    command=s['command'],
                    confidence=s['confidence'],
                    source=s['source'],
                    description=s['description'],
                    full_command=s['full_command']
                ))
        else:
            # Fallback to direct engine
            engine = SuggestionEngine(config)
            start_time = time.time()
            suggestions = engine.get_suggestions(input_text)
            elapsed_time = time.time() - start_time
        
        # Apply limit if specified
        if limit is not None:
            suggestions = suggestions[:limit]
        
        # Format and display suggestions
        if suggestions:
            output = formatter.format_suggestions(
                suggestions, 
                title=f"Suggestions for '{input_text}'",
                highlight_text=input_text
            )
            click.echo(output)
            
            if not compact and 'elapsed_time' in locals():
                click.echo(f"\n{formatter.colors.get('dim', '')}Generated {len(suggestions)} suggestions in {elapsed_time:.3f}s{formatter.colors.get('reset', '')}")
        else:
            click.echo(formatter.format_warning(f"No suggestions found for '{input_text}'"))
            
    except Exception as e:
        formatter = ctx.obj['formatter']
        click.echo(formatter.format_error(f"Failed to generate suggestions: {e}"))
        if ctx.obj['config'].get('debug', False):
            raise
        sys.exit(1)


@main.command()
@click.pass_context
def enable(ctx: click.Context) -> None:
    """Enable command suggestions."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    config.enable()
    click.echo(formatter.format_success("Command suggestions enabled"))


@main.command()
@click.pass_context
def disable(ctx: click.Context) -> None:
    """Disable command suggestions."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    config.disable()
    click.echo(formatter.format_success("Command suggestions disabled"))


@main.command()
@click.pass_context
def toggle(ctx: click.Context) -> None:
    """Toggle command suggestions on/off."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    enabled = config.toggle()
    status = "enabled" if enabled else "disabled"
    click.echo(formatter.format_success(f"Command suggestions {status}"))


@main.command()
@click.option('--performance', '-p', is_flag=True, help='Show performance statistics')
@click.option('--engine', '-e', is_flag=True, help='Show engine statistics')
@click.pass_context
def stats(ctx: click.Context, performance: bool, engine: bool) -> None:
    """Show statistics and performance information."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    try:
        if performance:
            # Show performance stats
            perf_summary = get_performance_summary()
            
            lines = [
                f"{formatter.colors.get('bright', '')}Performance Statistics:{formatter.colors.get('reset', '')}",
                f"Total requests: {perf_summary['total_requests']}",
                f"Cache hit rate: {perf_summary['cache_hit_rate']:.1%}",
                f"Avg suggestion time: {perf_summary['avg_suggestion_time']:.3f}s",
                f"Avg scan time: {perf_summary['avg_scan_time']:.3f}s",
                f"Avg history time: {perf_summary['avg_history_time']:.3f}s",
            ]
            
            click.echo("\n".join(lines))
        
        elif engine:
            # Show engine stats
            engine_obj = SuggestionEngine(config)
            engine_stats = engine_obj.get_engine_stats()
            
            output = formatter.format_stats(engine_stats)
            click.echo(output)
        
        else:
            # Show general config summary
            summary = config.get_config_summary()
            
            lines = [
                f"{formatter.colors.get('bright', '')}SugCommand Configuration:{formatter.colors.get('reset', '')}",
                f"Status: {formatter.colors.get('command' if summary['enabled'] else 'dim', '')}"
                f"{'ENABLED' if summary['enabled'] else 'DISABLED'}{formatter.colors.get('reset', '')}",
                f"Max suggestions: {summary['max_suggestions']}",
                f"History analysis: {'✓' if summary['history_analysis_enabled'] else '✗'}",
                f"Command scanning: {'✓' if summary['command_scan_enabled'] else '✗'}",
                f"Fuzzy search: {'✓' if summary['fuzzy_search_enabled'] else '✗'}",
                f"Colors: {'✓' if summary['color_enabled'] else '✗'}",
                f"Custom directories: {summary['custom_directories_count']}",
                f"Excluded commands: {summary['excluded_commands_count']}",
                f"Config file: {summary['config_file']}",
            ]
            
            # Add daemon status
            client = DaemonClient()
            daemon_status = "RUNNING" if client.is_daemon_running() else "STOPPED"
            daemon_color = formatter.colors.get('command' if client.is_daemon_running() else 'dim', '')
            lines.insert(-1, f"Daemon: {daemon_color}{daemon_status}{formatter.colors.get('reset', '')}")
            
            click.echo("\n".join(lines))
            
    except Exception as e:
        click.echo(formatter.format_error(f"Failed to get statistics: {e}"))
        sys.exit(1)


@main.group()
def config() -> None:
    """Configuration management commands."""
    pass


@config.command()
@click.argument('key')
@click.argument('value')
@click.pass_context
def set(ctx: click.Context, key: str, value: str) -> None:
    """Set a configuration value."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    try:
        # Convert value to appropriate type
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        elif '.' in value and value.replace('.', '').isdigit():
            value = float(value)
        
        config.set(key, value)
        click.echo(formatter.format_success(f"Set {key} = {value}"))
        
    except Exception as e:
        click.echo(formatter.format_error(f"Failed to set configuration: {e}"))
        sys.exit(1)


@config.command()
@click.argument('key')
@click.pass_context
def get(ctx: click.Context, key: str) -> None:
    """Get a configuration value."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    value = config.get(key)
    if value is not None:
        click.echo(f"{key} = {value}")
    else:
        click.echo(formatter.format_warning(f"Configuration key '{key}' not found"))


@config.command()
@click.option('--count', '-c', default=10, help='Number of suggestions to show')
@click.pass_context
def max_suggestions(ctx: click.Context, count: int) -> None:
    """Set maximum number of suggestions."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    try:
        config.set_max_suggestions(count)
        click.echo(formatter.format_success(f"Max suggestions set to {count}"))
    except ValueError as e:
        click.echo(formatter.format_error(str(e)))
        sys.exit(1)


@config.command()
@click.pass_context
def reset(ctx: click.Context) -> None:
    """Reset configuration to defaults."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    if click.confirm("Are you sure you want to reset configuration to defaults?"):
        config.reset_to_defaults()
        click.echo(formatter.format_success("Configuration reset to defaults"))
    else:
        click.echo("Reset cancelled")


@config.command()
@click.argument('file_path', type=click.Path())
@click.pass_context
def export(ctx: click.Context, file_path: str) -> None:
    """Export configuration to a file."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    try:
        config.export_config(Path(file_path))
        click.echo(formatter.format_success(f"Configuration exported to {file_path}"))
    except Exception as e:
        click.echo(formatter.format_error(f"Failed to export configuration: {e}"))
        sys.exit(1)


@config.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.pass_context
def import_config(ctx: click.Context, file_path: str) -> None:
    """Import configuration from a file."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    try:
        config.import_config(Path(file_path))
        click.echo(formatter.format_success(f"Configuration imported from {file_path}"))
    except Exception as e:
        click.echo(formatter.format_error(f"Failed to import configuration: {e}"))
        sys.exit(1)


@main.group()
def daemon() -> None:
    """Daemon management commands."""
    pass


@daemon.command()
@click.option('--background', '-d', is_flag=True, help='Run daemon in background')
@click.pass_context
def start(ctx: click.Context, background: bool) -> None:
    """Start the suggestion daemon."""
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    client = DaemonClient()
    if client.is_daemon_running():
        click.echo(formatter.format_warning("Daemon is already running"))
        return
    
    if background:
        # Start daemon in background
        try:
            subprocess.Popen([
                sys.executable, '-c',
                'from sugcommand.integrations.realtime_daemon import RealtimeDaemon; '
                'daemon = RealtimeDaemon(); daemon.start()'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait a moment and check if it started
            time.sleep(1)
            if client.is_daemon_running():
                click.echo(formatter.format_success("Daemon started in background"))
            else:
                click.echo(formatter.format_error("Failed to start daemon"))
                
        except Exception as e:
            click.echo(formatter.format_error(f"Failed to start daemon: {e}"))
    else:
        # Start daemon in foreground
        try:
            click.echo("Starting suggestion daemon...")
            daemon = RealtimeDaemon()
            daemon.start()
        except KeyboardInterrupt:
            click.echo("\nDaemon stopped by user")
        except Exception as e:
            click.echo(formatter.format_error(f"Daemon error: {e}"))


@daemon.command()
@click.pass_context
def stop(ctx: click.Context) -> None:
    """Stop the suggestion daemon."""
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    client = DaemonClient()
    if not client.is_daemon_running():
        click.echo(formatter.format_warning("Daemon is not running"))
        return
    
    # Send termination signal to daemon
    try:
        import signal
        import psutil
        
        # Find daemon process
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'sugcommand' in ' '.join(proc.info['cmdline']):
                    proc.terminate()
                    proc.wait(timeout=5)
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Check if stopped
        time.sleep(1)
        if not client.is_daemon_running():
            click.echo(formatter.format_success("Daemon stopped"))
        else:
            click.echo(formatter.format_error("Failed to stop daemon"))
            
    except ImportError:
        click.echo(formatter.format_error("psutil not available for daemon management"))
    except Exception as e:
        click.echo(formatter.format_error(f"Failed to stop daemon: {e}"))


@daemon.command()
@click.pass_context  
def status(ctx: click.Context) -> None:
    """Show daemon status."""
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    client = DaemonClient()
    if client.is_daemon_running():
        click.echo(formatter.format_success("Daemon is running"))
        
        # Try to get stats
        try:
            suggestions = client.get_suggestions("test")
            click.echo(f"Daemon is responsive (test query returned {len(suggestions)} suggestions)")
        except Exception as e:
            click.echo(formatter.format_warning(f"Daemon is running but not responsive: {e}"))
    else:
        click.echo(formatter.format_warning("Daemon is not running"))


@main.group()
def integration() -> None:
    """Shell integration management."""
    pass


@integration.command()
@click.option('--shell', type=click.Choice(['bash', 'zsh', 'fish', 'auto']), default='auto',
              help='Shell type to install for')
@click.pass_context
def install(ctx: click.Context, shell: str) -> None:
    """Install shell integration."""
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    if shell == 'auto':
        # Detect shell
        shell_env = os.environ.get('SHELL', '')
        if 'bash' in shell_env:
            shell = 'bash'
        elif 'zsh' in shell_env:
            shell = 'zsh'
        elif 'fish' in shell_env:
            shell = 'fish'
        else:
            click.echo(formatter.format_error("Could not detect shell. Please specify --shell"))
            sys.exit(1)
    
    try:
        if shell == 'bash':
            integration = BashIntegration()
        elif shell == 'zsh':
            integration = ZshIntegration()
        elif shell == 'fish':
            integration = FishIntegration()
        
        if integration.install():
            click.echo(formatter.format_success(f"Shell integration installed for {shell}"))
        else:
            click.echo(formatter.format_error(f"Failed to install {shell} integration"))
            
    except Exception as e:
        click.echo(formatter.format_error(f"Installation failed: {e}"))


@integration.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show integration status for all shells."""
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    integrations = [
        ('bash', BashIntegration()),
        ('zsh', ZshIntegration()),
        ('fish', FishIntegration()),
    ]
    
    click.echo(f"{formatter.colors.get('bright', '')}Shell Integration Status:{formatter.colors.get('reset', '')}")
    
    for shell_name, integration in integrations:
        status = integration.get_status()
        installed = "✓" if status['installed'] else "✗"
        daemon_status = "✓" if status['daemon_running'] else "✗"
        
        click.echo(f"{shell_name.upper():6}: Installed: {installed}  Daemon: {daemon_status}  Script: {status['completion_script']}")


@main.command()
@click.option('--force', '-f', is_flag=True, help='Force refresh even if cache is valid')
@click.pass_context
def refresh(ctx: click.Context, force: bool) -> None:
    """Refresh cached command and history data."""
    config: ConfigManager = ctx.obj['config']
    formatter: SuggestionFormatter = ctx.obj['formatter']
    
    try:
        click.echo("Refreshing cached data...")
        engine = SuggestionEngine(config)
        
        if force:
            engine.refresh_data()
            click.echo(formatter.format_success("Cache forcefully refreshed"))
        else:
            engine.warm_up()
            click.echo(formatter.format_success("Cache warmed up"))
            
    except Exception as e:
        click.echo(formatter.format_error(f"Failed to refresh cache: {e}"))
        sys.exit(1)


@main.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    """Show version information."""
    from . import __version__
    click.echo(f"sugcommand version {__version__}")


if __name__ == "__main__":
    main() 