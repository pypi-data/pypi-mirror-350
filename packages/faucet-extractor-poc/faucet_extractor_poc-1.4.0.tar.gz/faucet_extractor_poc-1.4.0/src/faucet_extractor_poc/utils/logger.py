"""
Common logging utilities for the faucet extractor.

This module provides functions to set up consistent logging across the application.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name, log_to_file=True):
    """
    Set up and return a logger with consistent formatting for console and file output.

    Args:
        name (str): Logger name (used both for the logger and log file name)
        log_to_file (bool): Whether to log to a file (default: True)

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create a logger
    logger = logging.getLogger(f"faucet_extractor.{name}")

    # Only set up handlers if they don't exist already
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Always add console handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Add file handler if requested
        if log_to_file:
            # Create logs directory if it doesn't exist
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)

            # Create a log file with date in the name
            today = datetime.now().strftime("%Y-%m-%d")
            log_file = logs_dir / f"{name.lower()}_{today}.log"

            # Create and add file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
