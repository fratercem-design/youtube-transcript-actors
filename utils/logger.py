"""Logging configuration."""

from loguru import logger
import sys
import os
from config.settings import LOG_LEVEL, LOG_FILE

# Remove default handler
logger.remove()

# Add console handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=LOG_LEVEL,
)

# Add file handler
logger.add(
    LOG_FILE,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=LOG_LEVEL,
    rotation="500 MB",
    retention="7 days",
)


def get_logger(name: str):
    """Get logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logger.bind(name=name)
