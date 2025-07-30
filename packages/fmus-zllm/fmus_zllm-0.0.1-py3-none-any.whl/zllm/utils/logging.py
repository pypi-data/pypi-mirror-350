"""
Logging utilities for ZLLM.
"""

import logging
import os
import sys
from typing import Dict, Any, Optional

# ANSI color codes for colored terminal output
COLORS = {
    'DEBUG': '\033[36m',  # Cyan
    'INFO': '\033[32m',   # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',  # Red
    'CRITICAL': '\033[41m\033[37m',  # White on Red background
    'RESET': '\033[0m'    # Reset
}


class ColoredFormatter(logging.Formatter):
    """Custom formatter for colored console output."""

    def format(self, record):
        """Format the record with colors."""
        # Check if we're in a terminal that supports colors
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            levelname = record.levelname
            if levelname in COLORS:
                record.levelname = f"{COLORS[levelname]}{levelname}{COLORS['RESET']}"
                record.msg = f"{COLORS[levelname]}{record.msg}{COLORS['RESET']}"
        return super().format(record)


def setup_logging(config: Optional[Dict[str, Any]] = None) -> None:
    """
    Set up logging based on configuration.

    Args:
        config: Logging configuration dictionary
    """
    if config is None:
        config = {}

    # Get logging configuration
    level_name = config.get('level', 'INFO')
    log_format = config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = config.get('file')

    # Convert level name to logging level
    level = getattr(logging, level_name.upper(), logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = ColoredFormatter(log_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
