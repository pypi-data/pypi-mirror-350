"""
Fish shell integration for sugcommand.
"""

import os
from pathlib import Path
from typing import List
import logging

from .realtime_daemon import DaemonClient

logger = logging.getLogger(__name__)


class FishIntegration:
    """Fish shell integration for sugcommand."""
    
    def __init__(self):
        """Initialize fish integration."""
        self.daemon_client = DaemonClient()
        self.completion_script_path = self._get_completion_script_path()
    
    def _get_completion_script_path(self) -> Path:
        """Get path for fish completion script."""
        fish_config_dir = Path.home() / '.config' / 'fish'
        if fish_config_dir.exists():
            return fish_config_dir / 'completions' / 'sugcommand.fish'
        
        from ..core.config_manager import ConfigManager
        config = ConfigManager()
        return config.config_dir / 'fish_completion.fish'
    
    def install(self) -> bool:
        """Install fish integration."""
        try:
            completion_script = self._generate_completion_script()
            
            self.completion_script_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.completion_script_path, 'w') as f:
                f.write(completion_script)
            
            os.chmod(self.completion_script_path, 0o755)
            logger.info(f"Fish completion script installed at {self.completion_script_path}")
            
            self._show_install_instructions()
            return True
            
        except Exception as e:
            logger.error(f"Failed to install fish integration: {e}")
            return False
    
    def _generate_completion_script(self) -> str:
        """Generate fish completion script."""
        return f'''# SugCommand fish completion script

# Check if daemon is available
function __sugcommand_daemon_available
    python3 -c "
import sys
sys.path.insert(0, '{Path(__file__).parent.parent.parent}')
from sugcommand.integrations.realtime_daemon import DaemonClient
client = DaemonClient()
exit(0 if client.is_daemon_running() else 1)
" 2>/dev/null
end

# Get suggestions from daemon
function __sugcommand_get_suggestions
    set current_command $argv[1]
    if __sugcommand_daemon_available
        python3 -c "
import sys
sys.path.insert(0, '{Path(__file__).parent.parent.parent}')
from sugcommand.integrations.realtime_daemon import DaemonClient
client = DaemonClient()
suggestions = client.get_suggestions('$current_command', timeout=0.5)
for suggestion in suggestions[:8]:
    print(suggestion['command'] + '\\t' + suggestion.get('description', ''))
" 2>/dev/null
    end
end

# Enhanced completion for common commands
function __sugcommand_complete_enhanced
    set current_line (commandline -cp)
    __sugcommand_get_suggestions "$current_line"
end

# Main sugcommand completions
complete -c sugcommand -f
complete -c sugcommand -n '__fish_use_subcommand' -a 'suggest' -d 'Get command suggestions'
complete -c sugcommand -n '__fish_use_subcommand' -a 'enable' -d 'Enable suggestions'
complete -c sugcommand -n '__fish_use_subcommand' -a 'disable' -d 'Disable suggestions'
complete -c sugcommand -n '__fish_use_subcommand' -a 'toggle' -d 'Toggle suggestions'
complete -c sugcommand -n '__fish_use_subcommand' -a 'stats' -d 'Show statistics'
complete -c sugcommand -n '__fish_use_subcommand' -a 'config' -d 'Configuration management'
complete -c sugcommand -n '__fish_use_subcommand' -a 'refresh' -d 'Refresh cached data'
complete -c sugcommand -n '__fish_use_subcommand' -a 'version' -d 'Show version'
complete -c sugcommand -n '__fish_use_subcommand' -a 'daemon' -d 'Daemon management'

# Config subcommands
complete -c sugcommand -n '__fish_seen_subcommand_from config' -a 'get set reset export import max-suggestions'

# Stats options
complete -c sugcommand -n '__fish_seen_subcommand_from stats' -l performance -d 'Show performance statistics'
complete -c sugcommand -n '__fish_seen_subcommand_from stats' -l engine -d 'Show engine statistics'

# Daemon subcommands
complete -c sugcommand -n '__fish_seen_subcommand_from daemon' -a 'start stop status'

# Install enhanced completions for common commands if daemon is available
if __sugcommand_daemon_available
    # Git completions
    complete -c git -f -a '(__sugcommand_complete_enhanced)'
    
    # Apt completions
    complete -c apt -f -a '(__sugcommand_complete_enhanced)'
    complete -c apt-get -f -a '(__sugcommand_complete_enhanced)'
    
    # Docker completions
    complete -c docker -f -a '(__sugcommand_complete_enhanced)'
    
    # Python/pip completions
    complete -c python -f -a '(__sugcommand_complete_enhanced)'
    complete -c python3 -f -a '(__sugcommand_complete_enhanced)'
    complete -c pip -f -a '(__sugcommand_complete_enhanced)'
    complete -c pip3 -f -a '(__sugcommand_complete_enhanced)'
    
    # Node/npm completions
    complete -c npm -f -a '(__sugcommand_complete_enhanced)'
    complete -c node -f -a '(__sugcommand_complete_enhanced)'
end

# Key binding for real-time suggestions (Ctrl+X)
function __sugcommand_show_suggestions
    set current_line (commandline -b)
    if test (string length "$current_line") -gt 2
        set suggestions (__sugcommand_get_suggestions "$current_line")
        if test (count $suggestions) -gt 0
            echo ""
            echo "💡 Suggestions:"
            for suggestion in $suggestions[1..3]
                echo "  $suggestion"
            end
            commandline -f repaint
        end
    end
end

# Bind Ctrl+X to show suggestions
bind \\cx __sugcommand_show_suggestions
'''
    
    def _show_install_instructions(self) -> None:
        """Show installation instructions."""
        if self.completion_script_path.parent.name == 'completions':
            print(f"""
🎉 Fish integration installed successfully!

The completion script has been installed to fish's completions directory.
Fish will automatically load it.

To start using enhanced completions:

1. Start the daemon: sugcommand daemon start
2. Restart fish or run: source {self.completion_script_path}
3. Try typing commands like 'git c<TAB>' or 'apt u<TAB>'

Key binding:
- Ctrl+X: Show real-time suggestions for current command
""")
        else:
            print(f"""
🎉 Fish integration installed successfully!

Add this line to your ~/.config/fish/config.fish:

    source {self.completion_script_path}

Then restart fish or run:

    source ~/.config/fish/config.fish
""")
    
    def is_installed(self) -> bool:
        """Check if installed."""
        return self.completion_script_path.exists()
    
    def get_status(self) -> dict:
        """Get status."""
        return {
            'installed': self.is_installed(),
            'completion_script': str(self.completion_script_path),
            'daemon_running': self.daemon_client.is_daemon_running(),
            'shell': 'fish'
        } 