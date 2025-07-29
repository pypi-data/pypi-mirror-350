"""
Zsh shell integration for sugcommand.
"""

import os
from pathlib import Path
from typing import List
import logging

from .realtime_daemon import DaemonClient

logger = logging.getLogger(__name__)


class ZshIntegration:
    """Zsh shell integration for sugcommand."""
    
    def __init__(self):
        """Initialize zsh integration."""
        self.daemon_client = DaemonClient()
        self.completion_script_path = self._get_completion_script_path()
    
    def _get_completion_script_path(self) -> Path:
        """Get path for zsh completion script."""
        from ..core.config_manager import ConfigManager
        config = ConfigManager()
        return config.config_dir / 'zsh_completion.zsh'
    
    def install(self) -> bool:
        """Install zsh integration."""
        try:
            completion_script = self._generate_completion_script()
            
            self.completion_script_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.completion_script_path, 'w') as f:
                f.write(completion_script)
            
            os.chmod(self.completion_script_path, 0o755)
            logger.info(f"Zsh completion script installed at {self.completion_script_path}")
            
            self._show_install_instructions()
            return True
            
        except Exception as e:
            logger.error(f"Failed to install zsh integration: {e}")
            return False
    
    def _generate_completion_script(self) -> str:
        """Generate zsh completion script."""
        return f'''#!/bin/zsh
# SugCommand zsh completion script

# Check if daemon is available
_sugcommand_daemon_available() {{
    python3 -c "
import sys
sys.path.insert(0, '{Path(__file__).parent.parent.parent}')
from sugcommand.integrations.realtime_daemon import DaemonClient
client = DaemonClient()
exit(0 if client.is_daemon_running() else 1)
" 2>/dev/null
}}

# Get suggestions from daemon
_sugcommand_get_suggestions() {{
    local current_command="$1"
    if _sugcommand_daemon_available; then
        python3 -c "
import sys
sys.path.insert(0, '{Path(__file__).parent.parent.parent}')
from sugcommand.integrations.realtime_daemon import DaemonClient
client = DaemonClient()
suggestions = client.get_suggestions('$current_command', timeout=0.5)
for suggestion in suggestions[:8]:
    print(suggestion['command'] + ':' + suggestion.get('description', ''))
" 2>/dev/null
    fi
}}

# Zsh completion function
_sugcommand_complete() {{
    local context state line
    local current_line="${{BUFFER[1,CURSOR]}}"
    
    local suggestions
    suggestions=($(_sugcommand_get_suggestions "$current_line"))
    
    if [[ ${{#suggestions}} -gt 0 ]]; then
        _describe 'suggestions' suggestions
    fi
}}

# Enhanced widget for real-time suggestions
_sugcommand_widget() {{
    local current_line="$BUFFER"
    
    if [[ ${{#current_line}} -gt 2 ]]; then
        local suggestions
        suggestions=($(_sugcommand_get_suggestions "$current_line"))
        
        if [[ ${{#suggestions}} -gt 0 ]]; then
            zle -M "💡 Suggestions: ${{suggestions[1]}} ${{suggestions[2]}} ${{suggestions[3]}}"
        fi
    fi
}}

# Main sugcommand completion
_sugcommand_main() {{
    local context state line
    
    _arguments -C \\
        '1:command:(suggest enable disable toggle stats config refresh version daemon)' \\
        '*::options:->options'
    
    case "$state" in
        options)
            case "${{words[1]}}" in
                config)
                    _arguments \\
                        '1:action:(get set reset export import max-suggestions)' \\
                        '*::'
                    ;;
                stats)
                    _arguments \\
                        '--performance[Show performance statistics]' \\
                        '--engine[Show engine statistics]'
                    ;;
                suggest)
                    # No specific completion for suggest
                    ;;
            esac
            ;;
    esac
}}

# Register completions
compdef _sugcommand_main sugcommand
compdef _sugcommand_main scmd

# Create widget and bind to key
zle -N _sugcommand_widget
# bindkey '^X^S' _sugcommand_widget  # Ctrl+X Ctrl+S for suggestions

# Install enhanced completions if daemon available
if _sugcommand_daemon_available; then
    # Install for common commands
    local commands=(git apt docker npm python pip find grep)
    for cmd in $commands; do
        if (( $+commands[$cmd] )); then
            compdef _sugcommand_complete $cmd
        fi
    done
fi
'''
    
    def _show_install_instructions(self) -> None:
        """Show installation instructions."""
        print(f"""
🎉 Zsh integration installed successfully!

Add this line to your ~/.zshrc:

    source {self.completion_script_path}

Then restart your shell or run:

    source ~/.zshrc

For real-time suggestions, also add:

    bindkey '^X^S' _sugcommand_widget

This binds Ctrl+X Ctrl+S to show suggestions.
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
            'shell': 'zsh'
        } 