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

    # Email
    email_enabled: bool
    email_smtp_host: str
    email_smtp_port: int
    email_from: str
    email_to: str
    email_app_password: str


def _load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    ai_provider = os.getenv("AI_PROVIDER", "gemini").lower()

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    email_smtp_host = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    email_smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    email_from = os.getenv("EMAIL_FROM", "")
    email_to = os.getenv("EMAIL_TO", "")
    email_app_password = os.getenv("EMAIL_APP_PASSWORD", "")

    if email_enabled:
        if not email_from or not email_to or not email_app_password:
            raise ValueError(
                "EMAIL_FROM, EMAIL_TO and EMAIL_APP_PASSWORD "
                "must be configured when EMAIL_ENABLED=true."
            )
        
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
        email_enabled=email_enabled,
        email_smtp_host=email_smtp_host,
        email_smtp_port=email_smtp_port,
        email_from=email_from,
        email_to=email_to,
        email_app_password=email_app_password,
    )


settings = _load_settings()
