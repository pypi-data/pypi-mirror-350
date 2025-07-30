"""
Realtime suggestion daemon for shell integration.

This daemon runs in the background and provides fast command suggestions
through a Unix socket interface.
"""

import asyncio
import json
import os
import signal
import socket
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional
import logging

from ..core import SuggestionEngine, ConfigManager
from ..utils.performance import timer

logger = logging.getLogger(__name__)


class RealtimeDaemon:
    """Realtime suggestion daemon for shell integration."""
    
    def __init__(self, socket_path: Optional[Path] = None):
        """
        Initialize the realtime daemon.
        
        Args:
            socket_path: Path to Unix socket (defaults to ~/.config/sugcommand/daemon.sock)
        """
        self.config = ConfigManager()
        self.engine = SuggestionEngine(self.config)
        
        # Socket setup
        if socket_path is None:
            socket_path = self.config.config_dir / "daemon.sock"
        self.socket_path = socket_path
        
        # State
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.clients: List[socket.socket] = []
        
        # Performance tracking
        self.request_count = 0
        self.total_response_time = 0.0
        
        # Warm up the engine
        logger.info("Warming up suggestion engine...")
        self.engine.warm_up()
        logger.info("Daemon initialized")
    
    def start(self) -> None:
        """Start the daemon server."""
        if self.running:
            logger.warning("Daemon is already running")
            return
        
        self._setup_socket()
        self._setup_signal_handlers()
        
        self.running = True
        logger.info(f"Starting daemon on {self.socket_path}")
        
        try:
            self._server_loop()
        except KeyboardInterrupt:
            logger.info("Daemon interrupted by user")
        except Exception as e:
            logger.error(f"Daemon error: {e}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the daemon server."""
        if not self.running:
            return
        
        logger.info("Stopping daemon...")
        self.running = False
        
        # Close client connections
        for client in self.clients[:]:
            self._close_client(client)
        
        # Close server socket
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        
        # Remove socket file
        if self.socket_path.exists():
            try:
                os.unlink(self.socket_path)
            except OSError:
                pass
        
        logger.info("Daemon stopped")
    
    def _setup_socket(self) -> None:
        """Setup Unix socket server."""
        # Remove existing socket file
        if self.socket_path.exists():
            os.unlink(self.socket_path)
        
        # Ensure directory exists
        self.socket_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create socket
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_socket.bind(str(self.socket_path))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1.0)  # Non-blocking with timeout
        
        # Set permissions (readable/writable by owner only)
        os.chmod(self.socket_path, 0o600)
    
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}")
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def _server_loop(self) -> None:
        """Main server loop."""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                logger.debug("New client connected")
                
                # Handle client in background
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()
                
            except socket.timeout:
                # Normal timeout, continue loop
                continue
            except Exception as e:
                if self.running:
                    logger.error(f"Error accepting connections: {e}")
                break
    
    def _handle_client(self, client_socket: socket.socket) -> None:
        """Handle individual client connection."""
        self.clients.append(client_socket)
        
        try:
            client_socket.settimeout(30.0)  # 30 second timeout
            
            while self.running:
                try:
                    # Read request
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    
                    # Process request
                    response = self._process_request(data.decode('utf-8'))
                    
                    # Send response
                    response_data = json.dumps(response).encode('utf-8')
                    client_socket.send(response_data + b'\n')
                    
                except socket.timeout:
                    # Client timeout
                    break
                except Exception as e:
                    logger.error(f"Error handling client: {e}")
                    break
        
        finally:
            self._close_client(client_socket)
    
    def _close_client(self, client_socket: socket.socket) -> None:
        """Close client connection."""
        try:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            logger.debug("Client disconnected")
        except Exception:
            pass
    
    def _process_request(self, request_data: str) -> Dict:
        """Process suggestion request."""
        try:
            request = json.loads(request_data.strip())
            command = request.get('command', '').strip()
            
            if not command:
                return {
                    'suggestions': [],
                    'error': 'No command provided'
                }
            
            # Check if suggestions are enabled
            if not self.config.is_enabled():
                return {
                    'suggestions': [],
                    'error': 'Suggestions disabled'
                }
            
            # Get suggestions with timing
            start_time = time.time()
            
            with timer('daemon_suggestion'):
                suggestions = self.engine.get_suggestions(command)
            
            response_time = time.time() - start_time
            
            # Update stats
            self.request_count += 1
            self.total_response_time += response_time
            
            # Limit suggestions for fast response
            max_suggestions = min(self.config.get_max_suggestions(), 10)
            limited_suggestions = suggestions[:max_suggestions]
            
            # Format suggestions for response
            suggestion_data = []
            for suggestion in limited_suggestions:
                suggestion_data.append({
                    'command': suggestion.command,
                    'full_command': suggestion.full_command,
                    'confidence': suggestion.confidence,
                    'source': suggestion.source,
                    'description': suggestion.description,
                })
            
            return {
                'suggestions': suggestion_data,
                'response_time': response_time,
                'stats': {
                    'total_requests': self.request_count,
                    'avg_response_time': self.total_response_time / self.request_count
                }
            }
            
        except json.JSONDecodeError:
            return {
                'suggestions': [],
                'error': 'Invalid JSON request'
            }
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return {
                'suggestions': [],
                'error': f'Internal error: {str(e)}'
            }
    
    def is_running(self) -> bool:
        """Check if daemon is running."""
        if not self.socket_path.exists():
            return False
        
        try:
            # Try to connect to the socket
            test_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            test_socket.settimeout(1.0)
            test_socket.connect(str(self.socket_path))
            test_socket.close()
            return True
        except (socket.error, OSError):
            return False
    
    def get_suggestions_sync(self, command: str) -> List[Dict]:
        """Get suggestions synchronously (for testing)."""
        if not self.config.is_enabled():
            return []
        
        suggestions = self.engine.get_suggestions(command)
        
        result = []
        for suggestion in suggestions:
            result.append({
                'command': suggestion.command,
                'full_command': suggestion.full_command,
                'confidence': suggestion.confidence,
                'source': suggestion.source,
                'description': suggestion.description,
            })
        
        return result


class DaemonClient:
    """Client for communicating with the daemon."""
    
    def __init__(self, socket_path: Optional[Path] = None):
        """Initialize daemon client."""
        if socket_path is None:
            config = ConfigManager()
            socket_path = config.config_dir / "daemon.sock"
        self.socket_path = socket_path
    
    def get_suggestions(self, command: str, timeout: float = 5.0) -> List[Dict]:
        """Get suggestions from daemon."""
        if not self.is_daemon_running():
            return []
        
        try:
            # Connect to daemon
            client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)
            client_socket.connect(str(self.socket_path))
            
            # Send request
            request = {'command': command}
            request_data = json.dumps(request).encode('utf-8')
            client_socket.send(request_data)
            
            # Receive response
            response_data = client_socket.recv(8192)
            client_socket.close()
            
            # Parse response
            response = json.loads(response_data.decode('utf-8'))
            
            if 'error' in response:
                logger.warning(f"Daemon error: {response['error']}")
                return []
            
            return response.get('suggestions', [])
            
        except Exception as e:
            logger.debug(f"Error communicating with daemon: {e}")
            return []
    
    def is_daemon_running(self) -> bool:
        """Check if daemon is running."""
        if not self.socket_path.exists():
            return False
        
        try:
            test_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            test_socket.settimeout(1.0)
            test_socket.connect(str(self.socket_path))
            test_socket.close()
            return True
        except (socket.error, OSError):
            return False 