"""A simple module to make it a little less painful to make console applications."""

__title__ = "bconsole"
__author__ = "BetaKors"
__version__ = "0.0.7"
__license__ = "MIT"
__url__ = "https://github.com/BetaKors/bconsole"

from colorama import just_fix_windows_console

from .console import Console
from .core import (
    Background,
    Cursor,
    Erase,
    Foreground,
    Modifier,
)
from .logger import ColoredLogger, Logger, LogLevel, LogLevelLike

just_fix_windows_console()
del just_fix_windows_console

__all__ = [
    "Background",
    "Console",
    "ColoredLogger",
    "Cursor",
    "Erase",
    "Foreground",
    "Logger",
    "LogLevel",
    "LogLevelLike",
    "Modifier",
]
