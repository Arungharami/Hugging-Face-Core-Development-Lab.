"""
Logging configuration setup for hf_core_lab.
"""

import logging
import sys


def setup_logger(name: str = "hf_core_lab", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a structured console logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
