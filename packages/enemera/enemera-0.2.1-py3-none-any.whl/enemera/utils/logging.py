"""
Logging utilities for the Enemera API client.
"""

import logging
import sys
from typing import Optional


class EnemeraLogger:
    """
    Logger class for the Enemera API client.

    Provides structured logging with consistent formatting and log level management.
    """

    # Log levels mapping
    LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def __init__(self, name: str = "enemera", level: str = "info"):
        """
        Initialize the logger.

        Args:
            name: Logger name
            level: Log level (debug, info, warning, error, critical)
        """
        self.logger = logging.getLogger(name)
        self.set_level(level)

        # Check if handlers already exist to avoid duplicate handlers
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stderr)

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def set_level(self, level: str) -> None:
        """
        Set the logging level.

        Args:
            level: Log level (debug, info, warning, error, critical)
        """
        if level.lower() not in self.LEVELS:
            raise ValueError(
                f"Invalid log level: {level}. Available levels: {', '.join(self.LEVELS.keys())}")

        self.logger.setLevel(self.LEVELS[level.lower()])

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with optional structured data"""
        self._log(self.logger.debug, message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message with optional structured data"""
        self._log(self.logger.info, message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with optional structured data"""
        self._log(self.logger.warning, message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message with optional structured data"""
        self._log(self.logger.error, message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with optional structured data"""
        self._log(self.logger.critical, message, **kwargs)

    def _log(self, log_func, message: str, **kwargs) -> None:
        """
        Internal method for structured logging.

        Args:
            log_func: Logging function to use
            message: Log message
            **kwargs: Additional structured data to include in the log
        """
        if kwargs:
            # Format structured data
            structured_data = " | ".join(f"{k}={v}" for k, v in kwargs.items())
            log_func(f"{message} | {structured_data}")
        else:
            log_func(message)


# Create default logger instance
logger = EnemeraLogger()


def configure_logging(
        level: Optional[str] = None,
        handler: Optional[logging.Handler] = None,
        formatter: Optional[logging.Formatter] = None
) -> None:
    """
    Configure the global Enemera logger.

    Args:
        level: Log level (debug, info, warning, error, critical)
        handler: Custom log handler to add (e.g., FileHandler)
        formatter: Custom formatter for the handler
    """
    if level:
        logger.set_level(level)

    if handler:
        if formatter:
            handler.setFormatter(formatter)
        logger.logger.addHandler(handler)


def get_logger(name: str = "enemera", level: Optional[str] = None) -> EnemeraLogger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name
        level: Log level (debug, info, warning, error, critical)

    Returns:
        EnemeraLogger instance
    """
    new_logger = EnemeraLogger(name)
    if level:
        new_logger.set_level(level)
    return new_logger
