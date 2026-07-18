"""
Application settings.

Loads environment variables from a .env file and validates them.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


SUPPORTED_PROVIDERS = {"gemini", "openai"}


@dataclass(frozen=True)
class Settings:
    bot_token: str
    chat_id: str
    ai_provider: str
    openai_api_key: str
    gemini_api_key: str
    supported_providers: set[str]


def _load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    ai_provider = os.getenv("AI_PROVIDER", "gemini").lower()

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    if not bot_token or not chat_id:
        raise ValueError("BOT_TOKEN and CHAT_ID must be configured.")

    if ai_provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported AI_PROVIDER '{ai_provider}'. "
            f"Supported values: {', '.join(sorted(SUPPORTED_PROVIDERS))}."
        )

    if ai_provider == "gemini" and not gemini_api_key:
        raise ValueError("GEMINI_API_KEY must be configured when AI_PROVIDER=gemini.")

    if ai_provider == "openai" and not openai_api_key:
        raise ValueError("OPENAI_API_KEY must be configured when AI_PROVIDER=openai.")

    return Settings(
        bot_token=bot_token,
        chat_id=chat_id,
        ai_provider=ai_provider,
        openai_api_key=openai_api_key,
        gemini_api_key=gemini_api_key,
        supported_providers=SUPPORTED_PROVIDERS,
    )


settings = _load_settings()
