"""
Display utilities for formatting command suggestions.
"""

from enum import Enum
from typing import List, Optional
import sys

try:
    from colorama import Fore, Back, Style, init
    init()  # Initialize colorama
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback color codes
    class Fore:
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'
    
    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        NORMAL = '\033[22m'
        RESET_ALL = '\033[0m'


class ColorScheme(Enum):
    """Color schemes for displaying suggestions."""
    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    MINIMAL = "minimal"


class SuggestionFormatter:
    """Formatter for displaying command suggestions in a nice format."""
    
    def __init__(self, 
                 color_enabled: bool = True,
                 color_scheme: ColorScheme = ColorScheme.DEFAULT,
                 compact_mode: bool = False,
                 show_confidence: bool = False,
                 show_source: bool = False):
        """
        Initialize SuggestionFormatter.
        
        Args:
            color_enabled: Whether to use colors
            color_scheme: Color scheme to use
            compact_mode: Whether to use compact display
            show_confidence: Whether to show confidence scores
            show_source: Whether to show suggestion sources
        """
        self.color_enabled = color_enabled and self._supports_color()
        self.color_scheme = color_scheme
        self.compact_mode = compact_mode
        self.show_confidence = show_confidence
        self.show_source = show_source
        
        self._setup_colors()
    
    def _supports_color(self) -> bool:
        """Check if terminal supports colors."""
        if not sys.stdout.isatty():
            return False
        
        # Check for color support
        try:
            import os
            if os.environ.get('NO_COLOR'):
                return False
            
            term = os.environ.get('TERM', '')
            if 'color' in term or term in ['xterm', 'xterm-256color', 'screen']:
                return True
                
            # Windows color support
            if sys.platform == 'win32':
                return COLORAMA_AVAILABLE
                
            return True
        except Exception:
            return False
    
    def _setup_colors(self) -> None:
        """Setup color scheme."""
        if not self.color_enabled:
            self.colors = {
                'command': '',
                'description': '',
                'confidence': '',
                'source': '',
                'highlight': '',
                'border': '',
                'reset': '',
                'dim': '',
                'bright': '',
            }
            return
        
        if self.color_scheme == ColorScheme.DEFAULT:
            self.colors = {
                'command': Fore.CYAN + Style.BRIGHT,
                'description': Fore.WHITE,
                'confidence': Fore.GREEN,
                'source': Fore.YELLOW,
                'highlight': Fore.MAGENTA + Style.BRIGHT,
                'border': Fore.BLUE,
                'reset': Style.RESET_ALL,
                'dim': Style.DIM,
                'bright': Style.BRIGHT,
            }
        elif self.color_scheme == ColorScheme.DARK:
            self.colors = {
                'command': Fore.GREEN + Style.BRIGHT,
                'description': Fore.WHITE + Style.DIM,
                'confidence': Fore.CYAN,
                'source': Fore.MAGENTA,
                'highlight': Fore.YELLOW + Style.BRIGHT,
                'border': Fore.WHITE + Style.DIM,
                'reset': Style.RESET_ALL,
                'dim': Style.DIM,
                'bright': Style.BRIGHT,
            }
        elif self.color_scheme == ColorScheme.LIGHT:
            self.colors = {
                'command': Fore.BLUE + Style.BRIGHT,
                'description': Fore.BLACK,
                'confidence': Fore.GREEN,
                'source': Fore.RED,
                'highlight': Fore.MAGENTA + Style.BRIGHT,
                'border': Fore.BLACK + Style.DIM,
                'reset': Style.RESET_ALL,
                'dim': Style.DIM,
                'bright': Style.BRIGHT,
            }
        else:  # MINIMAL
            self.colors = {
                'command': Style.BRIGHT,
                'description': Style.DIM,
                'confidence': '',
                'source': '',
                'highlight': Style.BRIGHT,
                'border': '',
                'reset': Style.RESET_ALL,
                'dim': Style.DIM,
                'bright': Style.BRIGHT,
            }
    
    def format_command(self, command: str, highlight_text: str = "") -> str:
        """Format a command with optional highlighting."""
        if not highlight_text or highlight_text.lower() not in command.lower():
            return f"{self.colors['command']}{command}{self.colors['reset']}"
        
        # Highlight matching part
        command_lower = command.lower()
        highlight_lower = highlight_text.lower()
        
        start_idx = command_lower.find(highlight_lower)
        if start_idx >= 0:
            end_idx = start_idx + len(highlight_text)
            
            before = command[:start_idx]
            match = command[start_idx:end_idx]
            after = command[end_idx:]
            
            return (f"{self.colors['command']}{before}"
                   f"{self.colors['highlight']}{match}"
                   f"{self.colors['command']}{after}{self.colors['reset']}")
        
        return f"{self.colors['command']}{command}{self.colors['reset']}"
    
    def format_confidence(self, confidence: float) -> str:
        """Format confidence score."""
        if not self.show_confidence:
            return ""
        
        percentage = int(confidence * 100)
        color = self.colors['confidence']
        
        if confidence >= 0.8:
            bar = "████▌"
        elif confidence >= 0.6:
            bar = "███▌ "
        elif confidence >= 0.4:
            bar = "██▌  "
        elif confidence >= 0.2:
            bar = "█▌   "
        else:
            bar = "▌    "
        
        return f"{color}[{bar}] {percentage:2d}%{self.colors['reset']}"
    
    def format_description(self, description: str) -> str:
        """Format description text."""
        if not description:
            return ""
        
        # Truncate long descriptions
        max_length = 60 if self.compact_mode else 80
        if len(description) > max_length:
            description = description[:max_length-3] + "..."
        
        return f"{self.colors['description']}{description}{self.colors['reset']}"
    
    def format_source(self, source: str) -> str:
        """Format source information."""
        if not self.show_source or not source:
            return ""
        
        source_map = {
            'command_scanner': '📋',
            'history_exact': '🎯',
            'history_partial': '📚',
            'frequent_commands': '⭐',
            'recent_commands': '🕒',
            'sequential': '🔗',
        }
        
        icon = source_map.get(source, '💡')
        return f"{self.colors['source']}{icon} {source}{self.colors['reset']}"
    
    def format_suggestion_line(self, 
                             suggestion, 
                             index: int, 
                             highlight_text: str = "") -> str:
        """Format a single suggestion line."""
        from ..core.suggestion_engine import SuggestionResult
        
        if isinstance(suggestion, SuggestionResult):
            command = suggestion.command
            confidence = suggestion.confidence
            description = suggestion.description
            source = suggestion.source
        else:
            # Backward compatibility
            command = suggestion.get('command', '')
            confidence = suggestion.get('confidence', 0.0)
            description = suggestion.get('description', '')
            source = suggestion.get('source', '')
        
        # Format components
        formatted_command = self.format_command(command, highlight_text)
        formatted_confidence = self.format_confidence(confidence)
        formatted_description = self.format_description(description)
        formatted_source = self.format_source(source)
        
        if self.compact_mode:
            # Compact format: "1. command - description"
            parts = [f"{self.colors['dim']}{index}.{self.colors['reset']}", formatted_command]
            
            if formatted_description:
                parts.append(f"{self.colors['dim']}-{self.colors['reset']}")
                parts.append(formatted_description)
            
            if formatted_confidence:
                parts.append(formatted_confidence)
            
            return " ".join(parts)
        else:
            # Full format with proper alignment
            line = f"{self.colors['dim']}{index:2d}.{self.colors['reset']} {formatted_command}"
            
            if formatted_confidence:
                line += f" {formatted_confidence}"
            
            if formatted_description:
                line += f"\n     {formatted_description}"
            
            if formatted_source:
                line += f" {formatted_source}"
            
            return line
    
    def format_suggestions(self, 
                          suggestions: List, 
                          title: str = "Suggestions",
                          highlight_text: str = "") -> str:
        """Format a list of suggestions."""
        if not suggestions:
            return f"{self.colors['dim']}No suggestions available{self.colors['reset']}"
        
        lines = []
        
        # Add title if not compact
        if not self.compact_mode and title:
            border = self.colors['border'] + "─" * len(title) + self.colors['reset']
            lines.append(f"{self.colors['bright']}{title}{self.colors['reset']}")
            lines.append(border)
        
        # Format each suggestion
        for i, suggestion in enumerate(suggestions, 1):
            formatted_line = self.format_suggestion_line(suggestion, i, highlight_text)
            lines.append(formatted_line)
        
        # Add footer if not compact
        if not self.compact_mode and len(suggestions) > 1:
            lines.append(f"{self.colors['dim']}Press Tab to accept, Ctrl+C to cancel{self.colors['reset']}")
        
        return "\n".join(lines)
    
    def format_stats(self, stats: dict) -> str:
        """Format statistics information."""
        lines = []
        
        # Engine status
        enabled = stats.get('config_enabled', False)
        status_color = self.colors['command'] if enabled else self.colors['dim']
        status_text = "ENABLED" if enabled else "DISABLED"
        
        lines.append(f"{self.colors['bright']}SugCommand Status:{self.colors['reset']} "
                    f"{status_color}{status_text}{self.colors['reset']}")
        
        # Configuration
        max_suggestions = stats.get('max_suggestions', 0)
        threshold = stats.get('min_confidence_threshold', 0)
        
        lines.append(f"{self.colors['description']}Max suggestions:{self.colors['reset']} {max_suggestions}")
        lines.append(f"{self.colors['description']}Min confidence:{self.colors['reset']} {threshold:.1%}")
        
        # Scanner stats
        scanner_stats = stats.get('command_scanner_stats', {})
        if scanner_stats:
            total_commands = scanner_stats.get('total_commands', 0)
            scan_dirs = scanner_stats.get('scan_directories', 0)
            lines.append(f"{self.colors['description']}Commands found:{self.colors['reset']} "
                        f"{self.colors['command']}{total_commands}{self.colors['reset']} "
                        f"(from {scan_dirs} directories)")
        
        # History stats
        history_stats = stats.get('history_analyzer_stats', {})
        if history_stats:
            unique_commands = history_stats.get('unique_commands', 0)
            total_analyzed = history_stats.get('total_commands_analyzed', 0)
            
            lines.append(f"{self.colors['description']}History analyzed:{self.colors['reset']} "
                        f"{self.colors['command']}{total_analyzed}{self.colors['reset']} commands "
                        f"({unique_commands} unique)")
        
        return "\n".join(lines)
    
    def format_error(self, message: str) -> str:
        """Format error message."""
        return f"{Fore.RED}Error: {message}{self.colors['reset']}"
    
    def format_warning(self, message: str) -> str:
        """Format warning message."""
        return f"{Fore.YELLOW}Warning: {message}{self.colors['reset']}"
    
    def format_success(self, message: str) -> str:
        """Format success message."""
        return f"{Fore.GREEN}✓ {message}{self.colors['reset']}" 