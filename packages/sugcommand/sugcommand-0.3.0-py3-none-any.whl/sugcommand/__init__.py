"""
sugcommand - Intelligent terminal command suggestion tool

A Python library that provides intelligent command suggestions based on:
- Available system commands
- Command history analysis
- Context-aware completions
- Real-time shell integration
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.command_scanner import CommandScanner
from .core.history_analyzer import HistoryAnalyzer
from .core.suggestion_engine import SuggestionEngine
from .core.config_manager import ConfigManager

__all__ = [
    "CommandScanner",
    "HistoryAnalyzer", 
    "SuggestionEngine",
    "ConfigManager",
] 