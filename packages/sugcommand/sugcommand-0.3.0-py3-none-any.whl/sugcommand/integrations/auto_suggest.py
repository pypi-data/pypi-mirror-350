import os
import sys
import time
import threading
import queue
import socket
import json
import subprocess
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import signal
import atexit

class TerminalSuggestionDisplay:
    """Display suggestions in terminal using escape sequences"""
    
    def __init__(self):
        self.last_suggestions = []
        self.display_active = False
        
    def show_suggestions(self, suggestions: List[str], current_line: str = "") -> None:
        """Show suggestions below current cursor position"""
        if not suggestions:
            self.hide_suggestions()
            return
            
        # Save cursor position and clear suggestions area
        sys.stdout.write('\033[s')  # Save cursor
        sys.stdout.write('\033[B')  # Move down one line
        
        # Clear multiple lines if needed
        for i in range(len(self.last_suggestions) + 1):
            sys.stdout.write('\033[2K\033[B')  # Clear line and move down
            
        # Move back up
        for i in range(len(self.last_suggestions) + 1):
            sys.stdout.write('\033[A')  # Move up
            
        sys.stdout.write('\033[B')  # Move down one line
        
        # Display new suggestions
        sys.stdout.write('\033[90m')  # Gray color
        for i, suggestion in enumerate(suggestions[:5]):  # Show max 5 suggestions
            if i > 0:
                sys.stdout.write('\033[B\033[2K')  # Move down and clear line
            sys.stdout.write(f"  💡 {suggestion}")
            
        sys.stdout.write('\033[0m')  # Reset color
        sys.stdout.write('\033[u')  # Restore cursor
        sys.stdout.flush()
        
        self.last_suggestions = suggestions[:5]
        self.display_active = True
        
    def hide_suggestions(self) -> None:
        """Hide currently displayed suggestions"""
        if not self.display_active:
            return
            
        sys.stdout.write('\033[s')  # Save cursor
        sys.stdout.write('\033[B')  # Move down one line
        
        # Clear suggestion lines
        for i in range(len(self.last_suggestions)):
            sys.stdout.write('\033[2K')  # Clear line
            if i < len(self.last_suggestions) - 1:
                sys.stdout.write('\033[B')  # Move down
                
        sys.stdout.write('\033[u')  # Restore cursor
        sys.stdout.flush()
        
        self.last_suggestions = []
        self.display_active = False

class AutoSuggestionServer:
    """Server that provides suggestions via Unix socket"""
    
    def __init__(self, socket_path: str = None):
        if socket_path is None:
            socket_path = str(Path.home() / ".config" / "sugcommand" / "auto_suggest.sock")
        self.socket_path = socket_path
        self.socket = None
        self.is_running = False
        self.suggestion_engine = None
        
    def start(self):
        """Start the suggestion server"""
        # Remove existing socket file
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
            
        # Create socket directory
        Path(self.socket_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create Unix socket
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(self.socket_path)
        self.socket.listen(5)
        
        # Set permissions for socket
        os.chmod(self.socket_path, 0o600)
        
        self.is_running = True
        
        # Initialize suggestion engine
        try:
            from sugcommand.core import SuggestionEngine, ConfigManager
            config = ConfigManager()
            self.suggestion_engine = SuggestionEngine(config)
        except ImportError:
            # Fallback for testing
            print("Warning: Could not import suggestion engine, using dummy responses")
            self.suggestion_engine = None
        
        print(f"Auto-suggestion server listening on {self.socket_path}")
        
        # Handle cleanup on exit (only if in main thread)
        try:
            atexit.register(self.stop)
            signal.signal(signal.SIGTERM, lambda s, f: self.stop())
            signal.signal(signal.SIGINT, lambda s, f: self.stop())
        except ValueError:
            # Ignore signal errors when not in main thread
            pass
        
        while self.is_running:
            try:
                client_socket, addr = self.socket.accept()
                threading.Thread(
                    target=self._handle_client, 
                    args=(client_socket,),
                    daemon=True
                ).start()
            except OSError:
                break
                
    def stop(self):
        """Stop the suggestion server"""
        self.is_running = False
        if self.socket:
            self.socket.close()
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
            
    def _handle_client(self, client_socket):
        """Handle client connection"""
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                return
                
            request = json.loads(data)
            command = request.get('command', '')
            
            if command and self.suggestion_engine:
                suggestions = self.suggestion_engine.get_suggestions(command)
                response = {
                    'suggestions': [s.command for s in suggestions[:5]],
                    'status': 'success'
                }
            elif command:
                # Dummy suggestions for testing
                dummy_suggestions = [
                    f"{command} --help",
                    f"{command} status",
                    f"{command} version",
                    f"{command} config",
                    f"{command} list"
                ]
                response = {
                    'suggestions': dummy_suggestions[:5],
                    'status': 'success'
                }
            else:
                response = {
                    'suggestions': [],
                    'status': 'no_command'
                }
                
            client_socket.send(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {
                'suggestions': [],
                'status': 'error',
                'error': str(e)
            }
            client_socket.send(json.dumps(error_response).encode('utf-8'))
        finally:
            client_socket.close()

class AutoSuggestionClient:
    """Client to communicate with suggestion server"""
    
    def __init__(self, socket_path: str = None):
        if socket_path is None:
            socket_path = str(Path.home() / ".config" / "sugcommand" / "auto_suggest.sock")
        self.socket_path = socket_path
        
    def get_suggestions(self, command: str) -> List[str]:
        """Get suggestions from server"""
        if not command or len(command) < 2:
            return []
            
        try:
            client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client_socket.settimeout(0.1)  # 100ms timeout
            client_socket.connect(self.socket_path)
            
            request = {'command': command}
            client_socket.send(json.dumps(request).encode('utf-8'))
            
            response_data = client_socket.recv(1024).decode('utf-8')
            response = json.loads(response_data)
            
            client_socket.close()
            
            if response.get('status') == 'success':
                return response.get('suggestions', [])
            return []
            
        except (socket.error, json.JSONDecodeError, FileNotFoundError):
            return []

class AutoSuggestionHandler:
    """Main handler for auto-suggestions"""
    
    def __init__(self):
        self.client = AutoSuggestionClient()
        self.display = TerminalSuggestionDisplay()
        self.last_command = ""
        self.suggestion_timer = None
        
    def handle_command_input(self, current_line: str) -> None:
        """Handle command input and show suggestions"""
        current_line = current_line.strip()
        
        # Cancel previous timer
        if self.suggestion_timer:
            self.suggestion_timer.cancel()
            
        # Don't show suggestions for very short commands or if line hasn't changed
        if len(current_line) < 2 or current_line == self.last_command:
            return
            
        self.last_command = current_line
        
        # Debounce suggestions with a short delay
        self.suggestion_timer = threading.Timer(0.3, self._show_suggestions, [current_line])
        self.suggestion_timer.start()
        
    def _show_suggestions(self, command: str) -> None:
        """Show suggestions for command"""
        suggestions = self.client.get_suggestions(command)
        if suggestions:
            self.display.show_suggestions(suggestions, command)
        else:
            self.display.hide_suggestions()
            
    def hide_suggestions(self) -> None:
        """Hide current suggestions"""
        self.display.hide_suggestions()
        if self.suggestion_timer:
            self.suggestion_timer.cancel()

def create_shell_integration():
    """Create shell integration files"""
    config_dir = Path.home() / ".config" / "sugcommand"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Bash integration
    bash_script = '''# SugCommand Auto-Suggestion Integration
# Add this to your ~/.bashrc

_sugcommand_auto_suggest() {
    local current_command="${READLINE_LINE}"
    if [[ ${#current_command} -ge 2 ]]; then
        # Send current command to suggestion handler
        echo "$current_command" | python3 -c "
import sys
from sugcommand.integrations.auto_suggest import AutoSuggestionHandler
handler = AutoSuggestionHandler()
line = sys.stdin.read().strip()
handler.handle_command_input(line)
" 2>/dev/null &
    fi
}

# Bind to key events
bind -x '"\\e[A": _sugcommand_auto_suggest'  # Up arrow
bind -x '"\\e[B": _sugcommand_auto_suggest'  # Down arrow

# Hook into command prompt
PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND; }_sugcommand_auto_suggest"
'''
    
    # Zsh integration  
    zsh_script = '''# SugCommand Auto-Suggestion Integration
# Add this to your ~/.zshrc

autoload -U add-zsh-hook

_sugcommand_auto_suggest() {
    local current_command="$BUFFER"
    if [[ ${#current_command} -ge 2 ]]; then
        echo "$current_command" | python3 -c "
import sys
from sugcommand.integrations.auto_suggest import AutoSuggestionHandler
handler = AutoSuggestionHandler()
line = sys.stdin.read().strip()
handler.handle_command_input(line)
" 2>/dev/null &
    fi
}

# Hook into zsh line editor
add-zsh-hook preexec _sugcommand_auto_suggest
'''
    
    # Write integration files
    with open(config_dir / "bash_auto_suggest.sh", "w") as f:
        f.write(bash_script)
        
    with open(config_dir / "zsh_auto_suggest.zsh", "w") as f:
        f.write(zsh_script)
        
    # Make files executable
    os.chmod(config_dir / "bash_auto_suggest.sh", 0o755)
    os.chmod(config_dir / "zsh_auto_suggest.zsh", 0o755)
    
    return config_dir 