from app.config import AI_PROVIDER

from providers.openai_provider import OpenAIProvider
from providers.gemini_provider import GeminiProvider


class ProviderFactory:

    @staticmethod
    def get_provider():

        if AI_PROVIDER == "openai":
            return OpenAIProvider()

        if AI_PROVIDER == "gemini":
            return GeminiProvider()

        raise ValueError(f"Unknown provider: {AI_PROVIDER}")