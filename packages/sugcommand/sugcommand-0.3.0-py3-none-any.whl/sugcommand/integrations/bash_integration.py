"""
Bash shell integration for sugcommand.

Provides bash completion scripts and integration hooks.
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional
import logging

from .realtime_daemon import DaemonClient

logger = logging.getLogger(__name__)


class BashIntegration:
    """Bash shell integration for sugcommand."""
    
    def __init__(self):
        """Initialize bash integration."""
        self.daemon_client = DaemonClient()
        self.completion_script_path = self._get_completion_script_path()
    
    def _get_completion_script_path(self) -> Path:
        """Get path for bash completion script."""
        # Try user completion directory first
        user_completion_dir = Path.home() / '.bash_completion.d'
        if user_completion_dir.exists():
            return user_completion_dir / 'sugcommand'
        
        # Fallback to config directory
        from ..core.config_manager import ConfigManager
        config = ConfigManager()
        return config.config_dir / 'bash_completion.sh'
    
    def install(self) -> bool:
        """Install bash integration."""
        try:
            # Create completion script
            completion_script = self._generate_completion_script()
            
            # Write completion script
            self.completion_script_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.completion_script_path, 'w') as f:
                f.write(completion_script)
            
            # Make executable
            os.chmod(self.completion_script_path, 0o755)
            
            logger.info(f"Bash completion script installed at {self.completion_script_path}")
            
            # Show installation instructions
            self._show_install_instructions()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to install bash integration: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall bash integration."""
        try:
            if self.completion_script_path.exists():
                os.unlink(self.completion_script_path)
                logger.info("Bash completion script removed")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall bash integration: {e}")
            return False
    
    def is_installed(self) -> bool:
        """Check if bash integration is installed."""
        return self.completion_script_path.exists()
    
    def _generate_completion_script(self) -> str:
        """Generate bash completion script."""
        return f'''#!/bin/bash
# SugCommand bash completion script
# Generated automatically - do not edit manually

# Check if sugcommand daemon is available
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
import json
sys.path.insert(0, '{Path(__file__).parent.parent.parent}')
from sugcommand.integrations.realtime_daemon import DaemonClient
client = DaemonClient()
suggestions = client.get_suggestions('$current_command', timeout=0.5)
for suggestion in suggestions[:5]:  # Limit to top 5
    print(suggestion['command'])
" 2>/dev/null
    fi
}}

# Bash completion function
_sugcommand_complete() {{
    local cur prev words cword
    _init_completion || return
    
    # Get current command line
    local current_line="${{COMP_LINE:0:$COMP_POINT}}"
    
    # Get suggestions
    local suggestions
    suggestions=$(_sugcommand_get_suggestions "$current_line")
    
    if [[ -n "$suggestions" ]]; then
        # Convert suggestions to completion array
        readarray -t COMPREPLY < <(compgen -W "$suggestions" -- "$cur")
    else
        # Fallback to default completion
        _default_complete "$@"
    fi
}}

# Enhanced completion with real-time suggestions
_sugcommand_enhanced_complete() {{
    local cur="${{COMP_WORDS[COMP_CWORD]}}"
    local current_line="${{COMP_LINE:0:$COMP_POINT}}"
    
    # Only enhance if we have a partial command
    if [[ ${{#cur}} -gt 0 ]]; then
        local suggestions
        suggestions=$(_sugcommand_get_suggestions "$current_line")
        
        if [[ -n "$suggestions" ]]; then
            readarray -t COMPREPLY < <(echo "$suggestions")
            return 0
        fi
    fi
    
    # Fallback to normal completion
    return 1
}}

# Real-time suggestion display (experimental)
_sugcommand_realtime_display() {{
    # This function can be bound to a key for real-time suggestions
    local current_line="${{READLINE_LINE}}"
    
    if [[ ${{#current_line}} -gt 2 ]]; then
        local suggestions
        suggestions=$(_sugcommand_get_suggestions "$current_line")
        
        if [[ -n "$suggestions" ]]; then
            echo
            echo "💡 Suggestions:"
            echo "$suggestions" | head -3 | sed 's/^/  /'
            echo -n "$ $current_line"
        fi
    fi
}}

# Install completion for common commands
_sugcommand_install_completions() {{
    # List of common commands to enhance
    local commands=(
        "git" "apt" "apt-get" "yum" "dnf" "pacman"
        "docker" "kubectl" "npm" "pip" "pip3" 
        "python" "python3" "node" "java" "mvn"
        "systemctl" "service" "sudo" "ssh" "scp"
        "find" "grep" "awk" "sed" "sort" "uniq"
        "ls" "cd" "cp" "mv" "rm" "mkdir" "chmod"
    )
    
    # Install completion for each command
    for cmd in "${{commands[@]}}"; do
        if command -v "$cmd" >/dev/null 2>&1; then
            complete -F _sugcommand_complete "$cmd"
        fi
    done
}}

# Completion for sugcommand itself
_sugcommand_main_complete() {{
    local cur prev words cword
    _init_completion || return
    
    case ${{cword}} in
        1)
            COMPREPLY=($(compgen -W "suggest enable disable toggle stats config refresh version" -- "$cur"))
            ;;
        2)
            case ${{prev}} in
                config)
                    COMPREPLY=($(compgen -W "get set reset export import max-suggestions" -- "$cur"))
                    ;;
                stats)
                    COMPREPLY=($(compgen -W "--performance --engine" -- "$cur"))
                    ;;
                suggest)
                    # For suggest command, don't provide specific completions
                    return 0
                    ;;
            esac
            ;;
    esac
}}

# Install completions
complete -F _sugcommand_main_complete sugcommand
complete -F _sugcommand_main_complete scmd

# Install enhanced completions if daemon is available
if _sugcommand_daemon_available; then
    _sugcommand_install_completions
    
    # Bind Ctrl+Space for real-time suggestions (optional)
    bind -x '"\\C- ": _sugcommand_realtime_display'
    
    # You can also bind other keys:
    # bind -x '"\\C-@": _sugcommand_realtime_display'  # Ctrl+@
    # bind -x '"\\C-]": _sugcommand_realtime_display'  # Ctrl+]
    # bind -x '"\\C-^": _sugcommand_realtime_display'  # Ctrl+^
    # bind -x '"\\C-_": _sugcommand_realtime_display'  # Ctrl+_
fi

# Export functions for use in subshells
export -f _sugcommand_get_suggestions
export -f _sugcommand_daemon_available
export -f _sugcommand_complete
'''
    
    def _show_install_instructions(self) -> None:
        """Show installation instructions to user."""
        print(f"""
🎉 Bash integration installed successfully!

To enable auto-completion, add this line to your ~/.bashrc:

    source {self.completion_script_path}

Then restart your shell or run:

    source ~/.bashrc

To start the suggestion daemon (for real-time suggestions):

    sugcommand daemon start

For best experience:
1. Start the daemon: sugcommand daemon start
2. Restart your shell
3. Try typing commands like 'git c<TAB>' or 'apt u<TAB>'

The integration will enhance tab completion for common commands!
""")
    
    def get_suggestions_for_completion(self, command_line: str, limit: int = 5) -> List[str]:
        """Get suggestions for bash completion."""
        try:
            suggestions = self.daemon_client.get_suggestions(command_line, timeout=0.5)
            return [s['command'] for s in suggestions[:limit]]
        except Exception as e:
            logger.debug(f"Error getting suggestions for completion: {e}")
            return []
    
    def test_completion(self, command: str) -> None:
        """Test completion for a command."""
        print(f"Testing completion for: '{command}'")
        suggestions = self.get_suggestions_for_completion(command)
        
        if suggestions:
            print("Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("No suggestions found")
    
    def check_daemon_status(self) -> bool:
        """Check if daemon is running."""
        return self.daemon_client.is_daemon_running()
    
    def get_status(self) -> dict:
        """Get integration status."""
        return {
            'installed': self.is_installed(),
            'completion_script': str(self.completion_script_path),
            'daemon_running': self.check_daemon_status(),
            'shell': 'bash'
        } 