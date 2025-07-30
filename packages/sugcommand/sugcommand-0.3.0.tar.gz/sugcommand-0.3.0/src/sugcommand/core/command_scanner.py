"""
Command Scanner Module

Scans and indexes all available system commands from:
- PATH directories
- Standard system directories
- Custom command locations
"""

import os
import stat
import threading
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


class CommandScanner:
    """Scanner for discovering and managing system commands."""
    
    def __init__(self, cache_duration: int = 3600):
        """
        Initialize CommandScanner.
        
        Args:
            cache_duration: How long to cache commands (seconds)
        """
        self.cache_duration = cache_duration
        self._commands: Dict[str, List[str]] = {}  # command_name -> [paths]
        self._command_descriptions: Dict[str, str] = {}
        self._last_scan_time = 0
        self._scan_lock = threading.Lock()
        
        # Standard directories to scan
        self.scan_directories = self._get_scan_directories()
        
    def _get_scan_directories(self) -> List[Path]:
        """Get list of directories to scan for commands."""
        directories = []
        
        # PATH directories
        path_env = os.environ.get('PATH', '')
        for path_str in path_env.split(os.pathsep):
            if path_str.strip():
                path_obj = Path(path_str)
                if path_obj.exists() and path_obj.is_dir():
                    directories.append(path_obj)
        
        # Standard system directories
        standard_dirs = [
            '/bin', '/usr/bin', '/usr/local/bin',
            '/sbin', '/usr/sbin', '/usr/local/sbin',
            '/opt/bin', '/snap/bin', '/usr/games',
            '/usr/local/games'
        ]
        
        for dir_str in standard_dirs:
            dir_path = Path(dir_str)
            if dir_path.exists() and dir_path.is_dir():
                if dir_path not in directories:
                    directories.append(dir_path)
        
        # User's local bin
        home = Path.home()
        user_dirs = [
            home / '.local' / 'bin',
            home / 'bin',
            home / '.cargo' / 'bin',  # Rust binaries
            home / 'go' / 'bin',      # Go binaries
        ]
        
        for dir_path in user_dirs:
            if dir_path.exists() and dir_path.is_dir():
                if dir_path not in directories:
                    directories.append(dir_path)
        
        return directories
    
    def _is_executable(self, file_path: Path) -> bool:
        """Check if file is executable."""
        try:
            return file_path.is_file() and os.access(file_path, os.X_OK)
        except (OSError, PermissionError):
            return False
    
    def _scan_directory(self, directory: Path) -> Dict[str, List[str]]:
        """Scan a single directory for commands."""
        commands = {}
        
        try:
            for item in directory.iterdir():
                if self._is_executable(item):
                    command_name = item.name
                    
                    # Skip some common non-commands
                    if self._should_skip_command(command_name):
                        continue
                    
                    if command_name not in commands:
                        commands[command_name] = []
                    commands[command_name].append(str(item))
                    
        except (OSError, PermissionError) as e:
            logger.debug(f"Cannot scan directory {directory}: {e}")
        
        return commands
    
    def _should_skip_command(self, command_name: str) -> bool:
        """Determine if command should be skipped."""
        # Skip hidden files, backup files, and common non-commands
        skip_patterns = [
            '.',           # Hidden files
            '~',          # Backup files
            '.bak',       # Backup files
            '.tmp',       # Temporary files
            '.old',       # Old files
        ]
        
        return any(pattern in command_name for pattern in skip_patterns)
    
    def _get_command_description(self, command_path: str) -> str:
        """Try to get a brief description of the command."""
        try:
            # Try to get description from man page
            import subprocess
            result = subprocess.run(
                ['man', '-f', Path(command_path).name],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout:
                # Parse the first line of man output
                first_line = result.stdout.split('\n')[0]
                if ' - ' in first_line:
                    return first_line.split(' - ', 1)[1].strip()
        except Exception:
            pass
        
        # Fallback: try --help
        try:
            import subprocess
            result = subprocess.run(
                [command_path, '--help'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout:
                # Get first meaningful line
                lines = result.stdout.split('\n')
                for line in lines[:5]:  # Check first 5 lines
                    line = line.strip()
                    if line and not line.startswith('-') and len(line) > 10:
                        return line[:100] + ('...' if len(line) > 100 else '')
        except Exception:
            pass
        
        return "Command-line tool"
    
    def scan_commands(self, force_refresh: bool = False) -> Dict[str, List[str]]:
        """
        Scan for all available commands.
        
        Args:
            force_refresh: Force a new scan even if cache is valid
            
        Returns:
            Dictionary mapping command names to their paths
        """
        current_time = time.time()
        
        with self._scan_lock:
            if (not force_refresh and 
                self._commands and 
                current_time - self._last_scan_time < self.cache_duration):
                return self._commands.copy()
            
            logger.info(f"Scanning {len(self.scan_directories)} directories for commands...")
            
            # Use thread pool for parallel scanning
            all_commands = {}
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    executor.submit(self._scan_directory, directory): directory
                    for directory in self.scan_directories
                }
                
                for future in futures:
                    try:
                        directory_commands = future.result(timeout=10)
                        
                        # Merge results
                        for cmd_name, paths in directory_commands.items():
                            if cmd_name not in all_commands:
                                all_commands[cmd_name] = []
                            all_commands[cmd_name].extend(paths)
                    except Exception as e:
                        directory = futures[future]
                        logger.warning(f"Failed to scan {directory}: {e}")
            
            # Remove duplicates and sort paths
            for cmd_name in all_commands:
                all_commands[cmd_name] = sorted(list(set(all_commands[cmd_name])))
            
            self._commands = all_commands
            self._last_scan_time = current_time
            
            logger.info(f"Found {len(self._commands)} unique commands")
            return self._commands.copy()
    
    def get_command_paths(self, command_name: str) -> List[str]:
        """Get all paths for a specific command."""
        commands = self.scan_commands()
        return commands.get(command_name, [])
    
    def command_exists(self, command_name: str) -> bool:
        """Check if a command exists in the system."""
        return len(self.get_command_paths(command_name)) > 0
    
    def search_commands(self, pattern: str, limit: int = 20) -> List[Tuple[str, float]]:
        """
        Search for commands matching a pattern.
        
        Args:
            pattern: Search pattern
            limit: Maximum number of results
            
        Returns:
            List of (command_name, relevance_score) tuples
        """
        commands = self.scan_commands()
        pattern_lower = pattern.lower()
        
        results = []
        
        for cmd_name in commands:
            cmd_lower = cmd_name.lower()
            score = 0.0
            
            # Exact match gets highest score
            if cmd_lower == pattern_lower:
                score = 100.0
            # Starts with pattern gets high score
            elif cmd_lower.startswith(pattern_lower):
                score = 80.0 - len(cmd_name) * 0.1
            # Contains pattern gets medium score
            elif pattern_lower in cmd_lower:
                score = 60.0 - len(cmd_name) * 0.1
            # Fuzzy match gets lower score
            else:
                # Simple fuzzy matching
                match_chars = 0
                pattern_idx = 0
                for char in cmd_lower:
                    if pattern_idx < len(pattern_lower) and char == pattern_lower[pattern_idx]:
                        match_chars += 1
                        pattern_idx += 1
                
                if match_chars == len(pattern_lower):
                    score = 40.0 - len(cmd_name) * 0.1
            
            if score > 0:
                results.append((cmd_name, score))
        
        # Sort by score (descending) and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    def get_command_stats(self) -> Dict[str, any]:
        """Get statistics about scanned commands."""
        commands = self.scan_commands()
        
        return {
            'total_commands': len(commands),
            'total_paths': sum(len(paths) for paths in commands.values()),
            'scan_directories': len(self.scan_directories),
            'last_scan_time': self._last_scan_time,
            'cache_duration': self.cache_duration,
        }
    
    def get_popular_commands(self, limit: int = 50) -> List[str]:
        """Get list of most commonly used commands."""
        # Common commands that users frequently use
        popular = [
            'ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'rm', 'cp', 'mv',
            'cat', 'less', 'more', 'head', 'tail', 'grep', 'find',
            'sort', 'uniq', 'wc', 'cut', 'awk', 'sed',
            'chmod', 'chown', 'ps', 'top', 'htop', 'kill', 'killall',
            'df', 'du', 'free', 'lscpu', 'lsblk', 'mount', 'umount',
            'wget', 'curl', 'ssh', 'scp', 'rsync',
            'git', 'vim', 'nano', 'emacs',
            'python', 'python3', 'pip', 'pip3',
            'node', 'npm', 'yarn',
            'docker', 'kubectl',
            'systemctl', 'service',
            'apt', 'apt-get', 'yum', 'dnf', 'pacman',
            'tar', 'gzip', 'gunzip', 'zip', 'unzip',
        ]
        
        commands = self.scan_commands()
        
        # Filter to only include commands that exist
        existing_popular = [cmd for cmd in popular if cmd in commands]
        
        # Add other commands to reach the limit
        if len(existing_popular) < limit:
            other_commands = [
                cmd for cmd in sorted(commands.keys()) 
                if cmd not in existing_popular
            ]
            existing_popular.extend(other_commands[:limit - len(existing_popular)])
        
        return existing_popular[:limit] 