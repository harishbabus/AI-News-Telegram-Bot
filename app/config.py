"""
Configuration module for the AI News Telegram Bot application.

This module loads environment variables from a .env file (if present)
and exposes configuration values used throughout the application.
"""

import os

from dotenv import load_dotenv

load_dotenv()

SUPPORTED_PROVIDERS = {"gemini", "openai"}

BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
CHAT_ID: str | None = os.getenv("CHAT_ID")
AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini").lower()
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN and CHAT_ID must be configured.")

if AI_PROVIDER not in SUPPORTED_PROVIDERS:
    raise ValueError(
        f"Unsupported AI_PROVIDER '{AI_PROVIDER}'. "
        f"Supported values: {', '.join(sorted(SUPPORTED_PROVIDERS))}."
    )

if AI_PROVIDER == "gemini" and not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be configured when AI_PROVIDER=gemini.")

if AI_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be configured when AI_PROVIDER=openai.")
