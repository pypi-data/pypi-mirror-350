"""
Shell integration modules for sugcommand.
"""

from .bash_integration import BashIntegration
from .zsh_integration import ZshIntegration
from .fish_integration import FishIntegration
from .realtime_daemon import RealtimeDaemon

__all__ = [
    "BashIntegration",
    "ZshIntegration", 
    "FishIntegration",
    "RealtimeDaemon",
] 