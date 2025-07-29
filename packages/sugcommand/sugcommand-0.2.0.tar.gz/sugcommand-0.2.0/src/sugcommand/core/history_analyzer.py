"""
History Analyzer Module

Analyzes command history from various shells to understand usage patterns
and provide intelligent suggestions based on past behavior.
"""

import os
import re
import threading
import time
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class HistoryAnalyzer:
    """Analyzer for shell command history patterns."""
    
    def __init__(self, cache_duration: int = 1800):
        """
        Initialize HistoryAnalyzer.
        
        Args:
            cache_duration: How long to cache history analysis (seconds)
        """
        self.cache_duration = cache_duration
        self._command_sequences: Dict[str, Counter] = {}
        self._command_frequencies: Counter = Counter()
        self._command_pairs: Dict[str, Counter] = {}
        self._recent_commands: List[str] = []
        self._last_analysis_time = 0
        self._analysis_lock = threading.Lock()
        
        # Shell history files to check
        self.history_files = self._get_history_files()
        
    def _get_history_files(self) -> List[Path]:
        """Get list of shell history files to analyze."""
        home = Path.home()
        history_files = []
        
        # Common shell history files
        potential_files = [
            home / '.bash_history',
            home / '.zsh_history', 
            home / '.history',
            home / '.fish' / 'fish_history',
            home / '.local' / 'share' / 'fish' / 'fish_history',
            home / '.tcsh_history',
            home / '.csh_history',
        ]
        
        for file_path in potential_files:
            if file_path.exists() and file_path.is_file():
                history_files.append(file_path)
        
        return history_files
    
    def _parse_bash_history(self, file_path: Path) -> List[str]:
        """Parse bash history file."""
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        commands.append(line)
        except Exception as e:
            logger.warning(f"Failed to parse bash history {file_path}: {e}")
        
        return commands
    
    def _parse_zsh_history(self, file_path: Path) -> List[str]:
        """Parse zsh history file."""
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Zsh history format: : timestamp:elapsed;command
                        if line.startswith(':') and ';' in line:
                            command = line.split(';', 1)[1]
                            commands.append(command)
                        elif not line.startswith(':'):
                            commands.append(line)
        except Exception as e:
            logger.warning(f"Failed to parse zsh history {file_path}: {e}")
        
        return commands
    
    def _parse_fish_history(self, file_path: Path) -> List[str]:
        """Parse fish shell history file."""
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_command = ""
                for line in f:
                    line = line.strip()
                    if line.startswith('- cmd: '):
                        current_command = line[7:]  # Remove '- cmd: '
                        if current_command:
                            commands.append(current_command)
        except Exception as e:
            logger.warning(f"Failed to parse fish history {file_path}: {e}")
        
        return commands
    
    def _extract_command_from_line(self, line: str) -> Optional[str]:
        """Extract the base command from a command line."""
        # Remove leading/trailing whitespace
        line = line.strip()
        
        if not line:
            return None
        
        # Split by pipes, redirections, and logical operators
        # to get the first command
        separators = ['|', '>', '>>', '<', '&&', '||', ';']
        first_part = line
        
        for sep in separators:
            if sep in first_part:
                first_part = first_part.split(sep)[0].strip()
        
        # Extract the first word (the command)
        parts = first_part.split()
        if not parts:
            return None
        
        command = parts[0]
        
        # Remove common prefixes
        prefixes = ['sudo', 'nohup', 'nice', 'ionice', 'time']
        while command in prefixes and len(parts) > 1:
            parts = parts[1:]
            command = parts[0]
        
        return command
    
    def _analyze_command_sequences(self, commands: List[str]) -> None:
        """Analyze command sequences to find patterns."""
        # Analyze command pairs (what command typically follows another)
        for i in range(len(commands) - 1):
            current_cmd = self._extract_command_from_line(commands[i])
            next_cmd = self._extract_command_from_line(commands[i + 1])
            
            if current_cmd and next_cmd:
                if current_cmd not in self._command_pairs:
                    self._command_pairs[current_cmd] = Counter()
                self._command_pairs[current_cmd][next_cmd] += 1
        
        # Analyze command arguments patterns
        for command_line in commands:
            command = self._extract_command_from_line(command_line)
            if command:
                # Store full command line for this command
                if command not in self._command_sequences:
                    self._command_sequences[command] = Counter()
                self._command_sequences[command][command_line] += 1
                
                # Count command frequency
                self._command_frequencies[command] += 1
    
    def analyze_history(self, force_refresh: bool = False) -> None:
        """
        Analyze shell history to extract patterns.
        
        Args:
            force_refresh: Force re-analysis even if cache is valid
        """
        current_time = time.time()
        
        with self._analysis_lock:
            if (not force_refresh and 
                self._command_frequencies and 
                current_time - self._last_analysis_time < self.cache_duration):
                return
            
            logger.info("Analyzing shell history...")
            
            # Reset data
            self._command_sequences.clear()
            self._command_frequencies.clear()
            self._command_pairs.clear()
            self._recent_commands.clear()
            
            all_commands = []
            
            # Parse all history files
            for history_file in self.history_files:
                file_commands = []
                
                if 'fish' in str(history_file):
                    file_commands = self._parse_fish_history(history_file)
                elif 'zsh' in str(history_file):
                    file_commands = self._parse_zsh_history(history_file)
                else:
                    file_commands = self._parse_bash_history(history_file)
                
                all_commands.extend(file_commands)
                logger.debug(f"Parsed {len(file_commands)} commands from {history_file}")
            
            if all_commands:
                # Keep recent commands (last 100)
                self._recent_commands = all_commands[-100:]
                
                # Analyze patterns
                self._analyze_command_sequences(all_commands)
                
                logger.info(f"Analyzed {len(all_commands)} total commands")
                logger.info(f"Found {len(self._command_frequencies)} unique commands")
            
            self._last_analysis_time = current_time
    
    def get_command_suggestions_after(self, command: str, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get commands that typically follow the given command.
        
        Args:
            command: The command to get suggestions for
            limit: Maximum number of suggestions
            
        Returns:
            List of (command, confidence_score) tuples
        """
        self.analyze_history()
        
        if command not in self._command_pairs:
            return []
        
        suggestions = []
        total_count = sum(self._command_pairs[command].values())
        
        for next_cmd, count in self._command_pairs[command].most_common(limit):
            confidence = count / total_count
            suggestions.append((next_cmd, confidence))
        
        return suggestions
    
    def get_argument_suggestions(self, command: str, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get argument patterns for a command based on history.
        
        Args:
            command: The command to get argument suggestions for
            limit: Maximum number of suggestions
            
        Returns:
            List of (full_command_line, usage_frequency) tuples
        """
        self.analyze_history()
        
        if command not in self._command_sequences:
            return []
        
        suggestions = []
        total_count = sum(self._command_sequences[command].values())
        
        for cmd_line, count in self._command_sequences[command].most_common(limit):
            frequency = count / total_count
            suggestions.append((cmd_line, frequency))
        
        return suggestions
    
    def get_frequent_commands(self, limit: int = 20) -> List[Tuple[str, int]]:
        """
        Get most frequently used commands.
        
        Args:
            limit: Maximum number of commands to return
            
        Returns:
            List of (command, frequency) tuples
        """
        self.analyze_history()
        return self._command_frequencies.most_common(limit)
    
    def get_recent_commands(self, limit: int = 10) -> List[str]:
        """
        Get recently used commands.
        
        Args:
            limit: Maximum number of recent commands
            
        Returns:
            List of recent command names
        """
        self.analyze_history()
        
        recent_unique = []
        seen = set()
        
        for cmd_line in reversed(self._recent_commands):
            cmd = self._extract_command_from_line(cmd_line)
            if cmd and cmd not in seen:
                recent_unique.append(cmd)
                seen.add(cmd)
                if len(recent_unique) >= limit:
                    break
        
        return recent_unique
    
    def get_context_suggestions(self, current_input: str, limit: int = 10) -> List[Tuple[str, float, str]]:
        """
        Get context-aware suggestions based on current input and history.
        
        Args:
            current_input: Current command line input
            limit: Maximum number of suggestions
            
        Returns:
            List of (suggestion, confidence, source) tuples
        """
        self.analyze_history()
        
        suggestions = []
        current_command = self._extract_command_from_line(current_input)
        
        if not current_command:
            return suggestions
        
        # Get argument suggestions based on exact command match
        arg_suggestions = self.get_argument_suggestions(current_command, limit)
        for cmd_line, freq in arg_suggestions:
            if cmd_line.startswith(current_input):
                suggestions.append((cmd_line, freq * 0.9, "history_exact"))
            elif current_input in cmd_line:
                suggestions.append((cmd_line, freq * 0.7, "history_partial"))
        
        # Get command sequence suggestions
        recent_commands = self.get_recent_commands(5)
        if recent_commands:
            last_command = recent_commands[0]
            next_suggestions = self.get_command_suggestions_after(last_command, 5)
            for next_cmd, conf in next_suggestions:
                if next_cmd == current_command:
                    # Boost confidence if this command often follows the recent one
                    for suggestion in suggestions:
                        if suggestion[0].startswith(current_command):
                            # Update confidence
                            old_conf = suggestion[1]
                            new_conf = min(1.0, old_conf + conf * 0.3)
                            suggestions[suggestions.index(suggestion)] = (
                                suggestion[0], new_conf, suggestion[2]
                            )
        
        # Sort by confidence and limit results
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:limit]
    
    def get_history_stats(self) -> Dict[str, Any]:
        """Get statistics about analyzed history."""
        self.analyze_history()
        
        return {
            'total_commands_analyzed': sum(self._command_frequencies.values()),
            'unique_commands': len(self._command_frequencies),
            'history_files_found': len(self.history_files),
            'recent_commands_count': len(self._recent_commands),
            'command_pairs_learned': len(self._command_pairs),
            'last_analysis_time': self._last_analysis_time,
        } 