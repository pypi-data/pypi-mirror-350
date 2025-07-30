"""
Suggestion Engine Module

Main engine that combines command scanning, history analysis, and user preferences
to provide intelligent command suggestions.
"""

import time
from typing import Dict, List, Set, Optional, Tuple, Any
import logging

from .command_scanner import CommandScanner
from .history_analyzer import HistoryAnalyzer
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class SuggestionResult:
    """Represents a single command suggestion."""
    
    def __init__(self, 
                 command: str, 
                 confidence: float, 
                 source: str, 
                 description: str = "",
                 full_command: str = ""):
        self.command = command
        self.confidence = confidence
        self.source = source
        self.description = description
        self.full_command = full_command or command
        
    def __repr__(self) -> str:
        return f"SuggestionResult(command={self.command}, confidence={self.confidence:.2f}, source={self.source})"


class SuggestionEngine:
    """Main engine for generating command suggestions."""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        Initialize SuggestionEngine.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager or ConfigManager()
        
        # Initialize components based on configuration
        cache_duration = self.config.get_cache_duration()
        history_cache_duration = self.config.get_history_cache_duration()
        
        self.command_scanner = CommandScanner(cache_duration) if self.config.is_command_scan_enabled() else None
        self.history_analyzer = HistoryAnalyzer(history_cache_duration) if self.config.is_history_analysis_enabled() else None
        
        logger.info("SuggestionEngine initialized")
    
    def _normalize_confidence(self, confidence: float, max_confidence: float = 1.0) -> float:
        """Normalize confidence score to 0-1 range."""
        return min(confidence / max_confidence, 1.0) if max_confidence > 0 else 0.0
    
    def _should_exclude_command(self, command: str) -> bool:
        """Check if command should be excluded from suggestions."""
        excluded = self.config.get_excluded_commands()
        return command in excluded
    
    def _get_command_suggestions(self, input_text: str) -> List[SuggestionResult]:
        """Get command suggestions based on available commands."""
        suggestions = []
        
        if not self.command_scanner or not input_text.strip():
            return suggestions
        
        try:
            # Search for matching commands
            matches = self.command_scanner.search_commands(input_text.strip(), limit=20)
            
            for command, score in matches:
                if self._should_exclude_command(command):
                    continue
                
                confidence = self._normalize_confidence(score, 100.0)
                
                # Skip low confidence matches
                if confidence < self.config.get_min_confidence_threshold():
                    continue
                
                suggestion = SuggestionResult(
                    command=command,
                    confidence=confidence,
                    source="command_scanner",
                    description=f"Available command: {command}"
                )
                suggestions.append(suggestion)
                
        except Exception as e:
            logger.warning(f"Error getting command suggestions: {e}")
        
        return suggestions
    
    def _get_history_suggestions(self, input_text: str) -> List[SuggestionResult]:
        """Get suggestions based on command history."""
        suggestions = []
        
        if not self.history_analyzer or not input_text.strip():
            return suggestions
        
        try:
            # Get context-aware suggestions from history
            history_suggestions = self.history_analyzer.get_context_suggestions(
                input_text.strip(), 
                limit=15
            )
            
            for cmd_line, confidence, source in history_suggestions:
                if self._should_exclude_command(cmd_line.split()[0] if cmd_line.split() else ""):
                    continue
                
                # Skip low confidence matches
                if confidence < self.config.get_min_confidence_threshold():
                    continue
                
                suggestion = SuggestionResult(
                    command=cmd_line.split()[0] if cmd_line.split() else cmd_line,
                    confidence=confidence,
                    source=f"history_{source}",
                    description="From command history",
                    full_command=cmd_line
                )
                suggestions.append(suggestion)
                
        except Exception as e:
            logger.warning(f"Error getting history suggestions: {e}")
        
        return suggestions
    
    def _get_frequent_command_suggestions(self, input_text: str) -> List[SuggestionResult]:
        """Get suggestions based on frequently used commands."""
        suggestions = []
        
        if not self.history_analyzer:
            return suggestions
        
        try:
            input_lower = input_text.lower().strip()
            if not input_lower:
                return suggestions
            
            # Get frequent commands
            frequent_commands = self.history_analyzer.get_frequent_commands(30)
            
            for command, frequency in frequent_commands:
                if self._should_exclude_command(command):
                    continue
                
                command_lower = command.lower()
                
                # Check if command matches input
                score = 0.0
                if command_lower == input_lower:
                    score = 1.0
                elif command_lower.startswith(input_lower):
                    score = 0.8
                elif input_lower in command_lower:
                    score = 0.6
                
                if score > 0:
                    # Weight by frequency and recent commands weight
                    weight = self.config.get('frequent_commands_weight', 1.2)
                    confidence = score * min(frequency / 100.0, 1.0) * weight
                    
                    if confidence >= self.config.get_min_confidence_threshold():
                        suggestion = SuggestionResult(
                            command=command,
                            confidence=confidence,
                            source="frequent_commands",
                            description=f"Frequently used ({frequency} times)"
                        )
                        suggestions.append(suggestion)
                        
        except Exception as e:
            logger.warning(f"Error getting frequent command suggestions: {e}")
        
        return suggestions
    
    def _get_recent_command_suggestions(self, input_text: str) -> List[SuggestionResult]:
        """Get suggestions based on recently used commands."""
        suggestions = []
        
        if not self.history_analyzer:
            return suggestions
        
        try:
            input_lower = input_text.lower().strip()
            if not input_lower:
                return suggestions
            
            # Get recent commands
            recent_commands = self.history_analyzer.get_recent_commands(20)
            
            for i, command in enumerate(recent_commands):
                if self._should_exclude_command(command):
                    continue
                
                command_lower = command.lower()
                
                # Check if command matches input
                score = 0.0
                if command_lower == input_lower:
                    score = 1.0
                elif command_lower.startswith(input_lower):
                    score = 0.8
                elif input_lower in command_lower:
                    score = 0.6
                
                if score > 0:
                    # Weight by recency and recent commands weight
                    recency_bonus = (20 - i) / 20.0  # More recent = higher score
                    weight = self.config.get('recent_commands_weight', 1.5)
                    confidence = score * recency_bonus * weight
                    
                    if confidence >= self.config.get_min_confidence_threshold():
                        suggestion = SuggestionResult(
                            command=command,
                            confidence=confidence,
                            source="recent_commands",
                            description=f"Recently used (#{i+1})"
                        )
                        suggestions.append(suggestion)
                        
        except Exception as e:
            logger.warning(f"Error getting recent command suggestions: {e}")
        
        return suggestions
    
    def _get_sequential_suggestions(self, input_text: str) -> List[SuggestionResult]:
        """Get suggestions based on command sequences (what usually comes next)."""
        suggestions = []
        
        if not self.history_analyzer:
            return suggestions
        
        try:
            # Get recent commands to understand context
            recent_commands = self.history_analyzer.get_recent_commands(3)
            
            if recent_commands:
                last_command = recent_commands[0]
                
                # Get commands that typically follow the last command
                next_commands = self.history_analyzer.get_command_suggestions_after(
                    last_command, 
                    limit=10
                )
                
                input_lower = input_text.lower().strip()
                
                for next_cmd, confidence in next_commands:
                    if self._should_exclude_command(next_cmd):
                        continue
                    
                    # Check if the suggested next command matches current input
                    if input_lower and not next_cmd.lower().startswith(input_lower):
                        continue
                    
                    if confidence >= self.config.get_min_confidence_threshold():
                        suggestion = SuggestionResult(
                            command=next_cmd,
                            confidence=confidence * 0.9,  # Slightly lower priority
                            source="sequential",
                            description=f"Often follows '{last_command}'"
                        )
                        suggestions.append(suggestion)
                        
        except Exception as e:
            logger.warning(f"Error getting sequential suggestions: {e}")
        
        return suggestions
    
    def _merge_and_rank_suggestions(self, all_suggestions: List[SuggestionResult]) -> List[SuggestionResult]:
        """Merge suggestions from different sources and rank them."""
        # Group suggestions by command
        command_groups: Dict[str, List[SuggestionResult]] = {}
        
        for suggestion in all_suggestions:
            key = suggestion.full_command if suggestion.full_command else suggestion.command
            if key not in command_groups:
                command_groups[key] = []
            command_groups[key].append(suggestion)
        
        # Merge suggestions for same command
        merged_suggestions = []
        
        for command, group in command_groups.items():
            if len(group) == 1:
                merged_suggestions.append(group[0])
            else:
                # Combine confidences from multiple sources
                total_confidence = sum(s.confidence for s in group)
                best_suggestion = max(group, key=lambda s: s.confidence)
                
                # Create merged suggestion
                sources = list(set(s.source for s in group))
                merged_suggestion = SuggestionResult(
                    command=best_suggestion.command,
                    confidence=min(total_confidence, 1.0),
                    source="+".join(sources),
                    description=best_suggestion.description,
                    full_command=best_suggestion.full_command
                )
                merged_suggestions.append(merged_suggestion)
        
        # Sort by confidence (descending)
        merged_suggestions.sort(key=lambda s: s.confidence, reverse=True)
        
        # Limit results
        max_suggestions = self.config.get_max_suggestions()
        return merged_suggestions[:max_suggestions]
    
    def get_suggestions(self, input_text: str) -> List[SuggestionResult]:
        """
        Get command suggestions for the given input.
        
        Args:
            input_text: Current command line input
            
        Returns:
            List of ranked suggestions
        """
        if not self.config.is_enabled():
            return []
        
        if not input_text or not input_text.strip():
            return []
        
        start_time = time.time()
        all_suggestions = []
        
        # Get suggestions from different sources
        try:
            # Command scanner suggestions
            all_suggestions.extend(self._get_command_suggestions(input_text))
            
            # History-based suggestions
            all_suggestions.extend(self._get_history_suggestions(input_text))
            
            # Frequent commands
            all_suggestions.extend(self._get_frequent_command_suggestions(input_text))
            
            # Recent commands
            all_suggestions.extend(self._get_recent_command_suggestions(input_text))
            
            # Sequential suggestions
            all_suggestions.extend(self._get_sequential_suggestions(input_text))
            
            # Merge and rank
            final_suggestions = self._merge_and_rank_suggestions(all_suggestions)
            
            elapsed_time = time.time() - start_time
            logger.debug(f"Generated {len(final_suggestions)} suggestions in {elapsed_time:.3f}s")
            
            return final_suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return []
    
    def get_engine_stats(self) -> Dict[str, Any]:
        """Get statistics about the suggestion engine."""
        stats = {
            'config_enabled': self.config.is_enabled(),
            'max_suggestions': self.config.get_max_suggestions(),
            'min_confidence_threshold': self.config.get_min_confidence_threshold(),
            'command_scanner_enabled': self.command_scanner is not None,
            'history_analyzer_enabled': self.history_analyzer is not None,
        }
        
        if self.command_scanner:
            stats.update({
                'command_scanner_stats': self.command_scanner.get_command_stats()
            })
        
        if self.history_analyzer:
            stats.update({
                'history_analyzer_stats': self.history_analyzer.get_history_stats()
            })
        
        return stats
    
    def warm_up(self) -> None:
        """Warm up the engine by pre-loading data."""
        logger.info("Warming up suggestion engine...")
        
        if self.command_scanner:
            self.command_scanner.scan_commands()
        
        if self.history_analyzer:
            self.history_analyzer.analyze_history()
        
        logger.info("Suggestion engine warmed up")
    
    def refresh_data(self) -> None:
        """Refresh cached data."""
        logger.info("Refreshing suggestion engine data...")
        
        if self.command_scanner:
            self.command_scanner.scan_commands(force_refresh=True)
        
        if self.history_analyzer:
            self.history_analyzer.analyze_history(force_refresh=True)
        
        logger.info("Suggestion engine data refreshed") 