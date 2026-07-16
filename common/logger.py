"""
Application logging configuration.

This module configures the application's logging behavior and exposes
a shared logger instance for use throughout the project.
"""
from common.constants import LOGGER_NAME
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(LOGGER_NAME)