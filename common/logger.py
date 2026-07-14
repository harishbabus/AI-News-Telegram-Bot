"""
Application logging configuration.

This module configures the application's logging behavior and exposes
a shared logger instance for use throughout the project.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("ai_news_bot")