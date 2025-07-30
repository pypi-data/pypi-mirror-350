"""ClipClean - A simple GUI tool for cleaning LLM outputs"""

__version__ = "1.0.0"
__author__ = "ClipClean Team"
__description__ = "A simple GUI tool for cleaning text copied from LLM outputs"

from .cleaner import LLMTextCleaner
from .gui import ClipCleanGUI
from .themes import ThemeManager

__all__ = ["LLMTextCleaner", "ClipCleanGUI", "ThemeManager"]