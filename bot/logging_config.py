"""
Logging configuration for the trading bot.
Sets up both file and console handlers with structured formatting.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.DEBUG) -> logging.Logger:
    """
    Configure and return the root logger for the trading bot.

    - File handler : DEBUG and above → logs/trading_bot.log (rotating, 5 MB × 3)
    - Console handler : INFO and above → stdout
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    root_logger = logging.getLogger("trading_bot")
    root_logger.setLevel(level)

    # Avoid adding duplicate handlers if called more than once
    if root_logger.handlers:
        return root_logger

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # --- Rotating file handler (full verbosity) ---
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # --- Console handler (INFO+) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger
