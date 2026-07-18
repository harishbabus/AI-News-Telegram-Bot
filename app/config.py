"""
Backward compatibility layer.

Existing modules can continue importing configuration
from app.config until they are migrated to app.settings.
"""

from app.settings import settings

BOT_TOKEN: str = settings.bot_token
CHAT_ID: str = settings.chat_id

AI_PROVIDER: str = settings.ai_provider

OPENAI_API_KEY: str = settings.openai_api_key
GEMINI_API_KEY: str = settings.gemini_api_key

SUPPORTED_PROVIDERS: set[str] = settings.supported_providers
