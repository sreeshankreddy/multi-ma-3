"""
Logging configuration for Multimodal Document Analyzer.
Sets up logging across the application.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_FILE


def setup_logging(name: str, log_file: str = None) -> logging.Logger:
    """
    Set up logger for a module.

    Args:
        name (str): Logger name (usually __name__).
        log_file (str): Log file path (optional).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log file specified)
    if log_file or LOG_FILE:
        file_path = log_file or LOG_FILE
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")

    return logger
