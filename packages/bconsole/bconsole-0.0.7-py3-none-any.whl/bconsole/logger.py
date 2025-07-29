import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path
from sys import stderr, stdout
from typing import Final, Literal, Self, TextIO, override

from .core import Foreground, Modifier

__all__ = ["LogLevel", "LogLevelLike", "Logger", "ColoredLogger"]

"""Type alias for a log level or a string representing a log level."""
type LogLevelLike = (
    LogLevel | Literal["verbose", "debug", "info", "warning", "error", "critical"]
)


class LogLevel(Enum):
    """Logging levels."""

    Verbose = "verbose"
    Debug = "debug"
    Info = "info"
    Warning = "warning"
    Error = "error"
    Critical = "critical"

    @classmethod
    def ensure(cls, level: LogLevelLike) -> Self:
        """
        Converts a string to a LogLevel if necessary.

        ### Args:
            level (LogLevelLike): The log level to convert.

        ### Returns:
            Self@LogLevel: The log level.
        """
        if isinstance(level, str):
            return cls[level.title()]
        return level  # type: ignore


class Logger:
    """Logger class."""

    def log(
        self,
        message: str,
        /,
        level: LogLevelLike = LogLevel.Info,
        *,
        end: str = "\n",
        flush: bool = False,
    ) -> None:
        """
        Logs a message with the specified log level to the console.

        ### Args:
            message (str): The message to log.
            level (LogLevelLike, optional): The log level. Defaults to LogLevel.INFO.
            end (str, optional): The end to use. Defaults to "\n".
        """
        level = LogLevel.ensure(level)
        file = self._get_file(level)

        file.write(self._format(message, level) + end)

        if flush:
            file.flush()

    def verbose(self, message: str) -> None:
        """
        Logs a message with LogLevel.VERBOSE to the console.

        ### Args:
            message (str): The message to log.
        """
        self.log(message, LogLevel.Verbose)

    def debug(self, message: str) -> None:
        """
        Logs a message with LogLevel.DEBUG to the console.

        ### Args:
            message (str): The message to log.
        """
        self.log(message, LogLevel.Debug)

    def info(self, message: str) -> None:
        """
        Logs a message with LogLevel.INFO to the console.

        ### Args:
            message (str): The message to log.
        """
        self.log(message, LogLevel.Info)

    def warning(self, message: Warning | str) -> None:
        """
        Logs a message with LogLevel.WARNING to the console.

        ### Args:
            message (str): The message to log.
        """
        self.log(str(message), LogLevel.Warning)

    def error(self, message: Exception | str) -> None:
        """
        Logs a message with LogLevel.ERROR to the console.

        ### Args:
            message (Exception | str): The message or exception to log.
        """
        self.log(str(message), LogLevel.Error)

    def critical(self, message: Exception | str) -> None:
        """
        Logs a message with LogLevel.CRITICAL to the console.

        ### Args:
            message (Exception | str): The message or exception to log.
        """
        self.log(str(message), LogLevel.Critical)

    def _get_file(self, level: LogLevelLike = LogLevel.Info, /) -> TextIO:
        """
        Gets the file to write the log message to based on the specified log level.\n
        Can be overriden to write to a different file for different log levels.

        ### Args:
            level (LogLevelLike, optional): The log level. Defaults to LogLevel.INFO.

        ### Returns:
            TextIO: The file to write the log message to.
        """
        return (
            stderr
            if LogLevel.ensure(level) in (LogLevel.Error, LogLevel.Critical)
            else stdout
        )

    def _format(self, message: str, level: LogLevelLike = LogLevel.Info, /) -> str:
        """
        Formats the log message with the specified log level.\n
        Can be overriden to provide different formatting styles based on the log level.

        ### Args:
            message (str): The message to format.
            level (LogLevelLike, optional): The log level. Defaults to LogLevel.INFO.

        ### Returns:
            str: The formatted log message.
        """
        return f"[{LogLevel.ensure(level).name}] {message}"


class ColoredLogger(Logger):
    """An example of how to override the Logger class to provide colored logging with timestamps and stack information."""

    _color_mapping: Final = {
        LogLevel.Verbose: Foreground.CYAN,
        LogLevel.Debug: Foreground.GREEN,
        LogLevel.Info: Foreground.WHITE,
        LogLevel.Warning: Foreground.make_rgb(255, 164, 0),  # orange
        LogLevel.Error: Foreground.RED,
        LogLevel.Critical: Foreground.RED,
    }

    _modifier_mapping: Final = {
        LogLevel.Verbose: Modifier.ITALIC,
        LogLevel.Debug: Modifier.ITALIC,
        LogLevel.Info: Modifier.NONE,
        LogLevel.Warning: Modifier.BOLD,
        LogLevel.Error: Modifier.BOLD,
        LogLevel.Critical: Modifier.INVERSE,
    }

    @override
    def _format(self, message: str, level: LogLevelLike = LogLevel.Info, /) -> str:
        frame = traceback.extract_stack(limit=5)[0]

        level = LogLevel.ensure(level)
        dt = datetime.now().strftime("%Y-%m-%d｜%H:%M:%S")
        file = Path(frame.filename or "").stem
        loc = frame.lineno or 0

        return (
            f"{Foreground.CYAN}({dt}){Modifier.RESET} "
            f"{Foreground.YELLOW}[{file}@L{loc}]{Modifier.RESET} "
            f"{self._modifier_mapping[level]}{self._color_mapping[level]}{super()._format(message, level)}{Modifier.RESET}"
        )
