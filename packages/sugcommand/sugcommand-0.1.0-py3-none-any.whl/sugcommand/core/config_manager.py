"""
Configuration Manager Module

Manages user settings and preferences for the sugcommand tool.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manager for user configuration and settings."""
    
    DEFAULT_CONFIG = {
        'enabled': True,
        'max_suggestions': 10,
        'suggestion_delay': 0.1,  # seconds
        'show_descriptions': True,
        'show_confidence': False,
        'history_analysis_enabled': True,
        'command_scan_enabled': True,
        'cache_duration': 3600,  # seconds
        'history_cache_duration': 1800,  # seconds
        'min_confidence_threshold': 0.1,
        'fuzzy_search_enabled': True,
        'recent_commands_weight': 1.5,
        'frequent_commands_weight': 1.2,
        'color_enabled': True,
        'compact_display': False,
        'custom_directories': [],
        'excluded_commands': [
            'history', 'clear', 'exit', 'logout',
            'sudo -s', 'su -', 'passwd'
        ],
        'shell_integration_enabled': False,
        'auto_complete_enabled': True,
        'keyboard_shortcuts': {
            'accept_suggestion': 'Tab',
            'next_suggestion': 'Ctrl+N',
            'prev_suggestion': 'Ctrl+P',
            'dismiss_suggestions': 'Escape'
        }
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize ConfigManager.
        
        Args:
            config_dir: Custom config directory (defaults to ~/.config/sugcommand)
        """
        if config_dir is None:
            config_dir = Path.home() / '.config' / 'sugcommand'
        
        self.config_dir = config_dir
        self.config_file = config_dir / 'config.json'
        self.cache_dir = config_dir / 'cache'
        
        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self._config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # Merge with defaults
                self._config = self.DEFAULT_CONFIG.copy()
                self._config.update(user_config)
                
                logger.debug(f"Loaded configuration from {self.config_file}")
            else:
                # Use default config
                self._config = self.DEFAULT_CONFIG.copy()
                self.save_config()  # Save default config
                logger.info(f"Created default configuration at {self.config_file}")
                
        except Exception as e:
            logger.warning(f"Failed to load config, using defaults: {e}")
            self._config = self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, sort_keys=True)
            logger.debug(f"Saved configuration to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
        self.save_config()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self._config.update(updates)
        self.save_config()
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save_config()
        logger.info("Configuration reset to defaults")
    
    def is_enabled(self) -> bool:
        """Check if suggestions are enabled."""
        return self.get('enabled', True)
    
    def enable(self) -> None:
        """Enable suggestions."""
        self.set('enabled', True)
        logger.info("Suggestions enabled")
    
    def disable(self) -> None:
        """Disable suggestions."""
        self.set('enabled', False)
        logger.info("Suggestions disabled")
    
    def toggle(self) -> bool:
        """Toggle suggestions on/off."""
        current = self.is_enabled()
        self.set('enabled', not current)
        status = "enabled" if not current else "disabled"
        logger.info(f"Suggestions {status}")
        return not current
    
    def get_max_suggestions(self) -> int:
        """Get maximum number of suggestions to show."""
        return self.get('max_suggestions', 10)
    
    def set_max_suggestions(self, count: int) -> None:
        """Set maximum number of suggestions."""
        if 1 <= count <= 50:
            self.set('max_suggestions', count)
        else:
            raise ValueError("Max suggestions must be between 1 and 50")
    
    def get_cache_duration(self) -> int:
        """Get cache duration in seconds."""
        return self.get('cache_duration', 3600)
    
    def get_history_cache_duration(self) -> int:
        """Get history cache duration in seconds."""
        return self.get('history_cache_duration', 1800)
    
    def is_history_analysis_enabled(self) -> bool:
        """Check if history analysis is enabled."""
        return self.get('history_analysis_enabled', True)
    
    def is_command_scan_enabled(self) -> bool:
        """Check if command scanning is enabled."""
        return self.get('command_scan_enabled', True)
    
    def is_fuzzy_search_enabled(self) -> bool:
        """Check if fuzzy search is enabled."""
        return self.get('fuzzy_search_enabled', True)
    
    def is_color_enabled(self) -> bool:
        """Check if colored output is enabled."""
        return self.get('color_enabled', True)
    
    def get_min_confidence_threshold(self) -> float:
        """Get minimum confidence threshold for suggestions."""
        return self.get('min_confidence_threshold', 0.1)
    
    def get_custom_directories(self) -> list:
        """Get list of custom directories to scan."""
        return self.get('custom_directories', [])
    
    def add_custom_directory(self, directory: str) -> None:
        """Add a custom directory to scan."""
        directories = self.get_custom_directories()
        if directory not in directories:
            directories.append(directory)
            self.set('custom_directories', directories)
    
    def remove_custom_directory(self, directory: str) -> None:
        """Remove a custom directory from scanning."""
        directories = self.get_custom_directories()
        if directory in directories:
            directories.remove(directory)
            self.set('custom_directories', directories)
    
    def get_excluded_commands(self) -> list:
        """Get list of excluded commands."""
        return self.get('excluded_commands', [])
    
    def add_excluded_command(self, command: str) -> None:
        """Add a command to the exclusion list."""
        excluded = self.get_excluded_commands()
        if command not in excluded:
            excluded.append(command)
            self.set('excluded_commands', excluded)
    
    def remove_excluded_command(self, command: str) -> None:
        """Remove a command from the exclusion list."""
        excluded = self.get_excluded_commands()
        if command in excluded:
            excluded.remove(command)
            self.set('excluded_commands', excluded)
    
    def get_keyboard_shortcuts(self) -> dict:
        """Get keyboard shortcuts configuration."""
        return self.get('keyboard_shortcuts', {})
    
    def set_keyboard_shortcut(self, action: str, shortcut: str) -> None:
        """Set a keyboard shortcut for an action."""
        shortcuts = self.get_keyboard_shortcuts()
        shortcuts[action] = shortcut
        self.set('keyboard_shortcuts', shortcuts)
    
    def export_config(self, file_path: Path) -> None:
        """Export configuration to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, sort_keys=True)
            logger.info(f"Configuration exported to {file_path}")
        except Exception as e:
            logger.error(f"Failed to export configuration: {e}")
            raise
    
    def import_config(self, file_path: Path) -> None:
        """Import configuration from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validate imported config
            if not isinstance(imported_config, dict):
                raise ValueError("Invalid configuration format")
            
            # Merge with current config
            self._config.update(imported_config)
            self.save_config()
            logger.info(f"Configuration imported from {file_path}")
        except Exception as e:
            logger.error(f"Failed to import configuration: {e}")
            raise
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration."""
        return {
            'enabled': self.is_enabled(),
            'max_suggestions': self.get_max_suggestions(),
            'history_analysis_enabled': self.is_history_analysis_enabled(),
            'command_scan_enabled': self.is_command_scan_enabled(),
            'fuzzy_search_enabled': self.is_fuzzy_search_enabled(),
            'color_enabled': self.is_color_enabled(),
            'custom_directories_count': len(self.get_custom_directories()),
            'excluded_commands_count': len(self.get_excluded_commands()),
            'config_file': str(self.config_file),
            'cache_dir': str(self.cache_dir),
        }
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration and return issues."""
        issues = []
        warnings = []
        
        # Check required boolean settings
        bool_settings = ['enabled', 'show_descriptions', 'history_analysis_enabled']
        for setting in bool_settings:
            if not isinstance(self.get(setting), bool):
                issues.append(f"Setting '{setting}' must be a boolean")
        
        # Check numeric settings
        if not isinstance(self.get('max_suggestions'), int) or self.get('max_suggestions') < 1:
            issues.append("max_suggestions must be a positive integer")
        
        if not isinstance(self.get('cache_duration'), int) or self.get('cache_duration') < 0:
            issues.append("cache_duration must be a non-negative integer")
        
        # Check threshold
        threshold = self.get('min_confidence_threshold')
        if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
            issues.append("min_confidence_threshold must be a number between 0 and 1")
        
        # Check custom directories
        for directory in self.get_custom_directories():
            if not Path(directory).exists():
                warnings.append(f"Custom directory does not exist: {directory}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        } 