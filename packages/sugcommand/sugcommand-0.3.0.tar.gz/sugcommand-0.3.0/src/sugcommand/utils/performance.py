"""
Performance monitoring utilities.
"""

import time
import threading
from typing import Dict, List, Optional
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor performance metrics for the suggestion engine."""
    
    def __init__(self, max_samples: int = 1000):
        """
        Initialize PerformanceMonitor.
        
        Args:
            max_samples: Maximum number of samples to keep for each metric
        """
        self.max_samples = max_samples
        self._metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_samples))
        self._counters: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()
        
        # Active timers
        self._active_timers: Dict[str, float] = {}
    
    def start_timer(self, name: str) -> None:
        """Start a timer for a named operation."""
        with self._lock:
            self._active_timers[name] = time.time()
    
    def end_timer(self, name: str) -> float:
        """End a timer and record the duration."""
        with self._lock:
            if name not in self._active_timers:
                logger.warning(f"Timer '{name}' was not started")
                return 0.0
            
            duration = time.time() - self._active_timers[name]
            del self._active_timers[name]
            
            self._metrics[name].append(duration)
            return duration
    
    def record_metric(self, name: str, value: float) -> None:
        """Record a metric value."""
        with self._lock:
            self._metrics[name].append(value)
    
    def increment_counter(self, name: str, amount: int = 1) -> None:
        """Increment a counter."""
        with self._lock:
            self._counters[name] += amount
    
    def get_metric_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        with self._lock:
            if name not in self._metrics or not self._metrics[name]:
                return {}
            
            values = list(self._metrics[name])
            
            return {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values),
                'latest': values[-1] if values else 0.0,
            }
    
    def get_counter_value(self, name: str) -> int:
        """Get current counter value."""
        with self._lock:
            return self._counters[name]
    
    def get_all_stats(self) -> Dict[str, any]:
        """Get all performance statistics."""
        with self._lock:
            stats = {
                'metrics': {},
                'counters': dict(self._counters),
                'active_timers': list(self._active_timers.keys()),
            }
            
            for name in self._metrics:
                stats['metrics'][name] = self.get_metric_stats(name)
            
            return stats
    
    def reset(self) -> None:
        """Reset all metrics and counters."""
        with self._lock:
            self._metrics.clear()
            self._counters.clear()
            self._active_timers.clear()
    
    def reset_metric(self, name: str) -> None:
        """Reset a specific metric."""
        with self._lock:
            if name in self._metrics:
                self._metrics[name].clear()
    
    def reset_counter(self, name: str) -> None:
        """Reset a specific counter."""
        with self._lock:
            self._counters[name] = 0


class TimerContext:
    """Context manager for timing operations."""
    
    def __init__(self, monitor: PerformanceMonitor, name: str):
        self.monitor = monitor
        self.name = name
        self.duration = 0.0
    
    def __enter__(self):
        self.monitor.start_timer(self.name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = self.monitor.end_timer(self.name)


# Global performance monitor instance
_global_monitor = PerformanceMonitor()


def get_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    return _global_monitor


def timer(name: str) -> TimerContext:
    """Create a timer context for the given operation name."""
    return TimerContext(_global_monitor, name)


def record_suggestion_time(duration: float) -> None:
    """Record time taken to generate suggestions."""
    _global_monitor.record_metric('suggestion_time', duration)


def record_scan_time(duration: float) -> None:
    """Record time taken to scan commands."""
    _global_monitor.record_metric('command_scan_time', duration)


def record_history_analysis_time(duration: float) -> None:
    """Record time taken to analyze history."""
    _global_monitor.record_metric('history_analysis_time', duration)


def increment_suggestion_requests() -> None:
    """Increment the suggestion request counter."""
    _global_monitor.increment_counter('suggestion_requests')


def increment_cache_hits() -> None:
    """Increment the cache hit counter."""
    _global_monitor.increment_counter('cache_hits')


def increment_cache_misses() -> None:
    """Increment the cache miss counter."""
    _global_monitor.increment_counter('cache_misses')


def get_performance_summary() -> Dict[str, any]:
    """Get a summary of performance metrics."""
    stats = _global_monitor.get_all_stats()
    
    summary = {
        'total_requests': _global_monitor.get_counter_value('suggestion_requests'),
        'cache_hit_rate': 0.0,
        'avg_suggestion_time': 0.0,
        'avg_scan_time': 0.0,
        'avg_history_time': 0.0,
    }
    
    # Calculate cache hit rate
    hits = _global_monitor.get_counter_value('cache_hits')
    misses = _global_monitor.get_counter_value('cache_misses')
    if hits + misses > 0:
        summary['cache_hit_rate'] = hits / (hits + misses)
    
    # Get average times
    if 'suggestion_time' in stats['metrics']:
        summary['avg_suggestion_time'] = stats['metrics']['suggestion_time'].get('avg', 0.0)
    
    if 'command_scan_time' in stats['metrics']:
        summary['avg_scan_time'] = stats['metrics']['command_scan_time'].get('avg', 0.0)
    
    if 'history_analysis_time' in stats['metrics']:
        summary['avg_history_time'] = stats['metrics']['history_analysis_time'].get('avg', 0.0)
    
    return summary 