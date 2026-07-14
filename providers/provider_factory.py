from app.config import AI_PROVIDER
from common.logger import logger
from providers.base_provider import AIProvider
from providers.gemini_provider import GeminiProvider
from providers.openai_provider import OpenAIProvider


class ProviderFactory:
    """Creates AI provider instances."""

    @staticmethod
    def get_provider()  -> AIProvider:
        """
        Factory method to get the configured AI provider.
        """

        _PROVIDERS = {
            "gemini": GeminiProvider,
            "openai": OpenAIProvider,
        }

        logger.info("Using AI provider: %s", AI_PROVIDER)

        provider_class = ProviderFactory._PROVIDERS.get(AI_PROVIDER)

        if provider_class is None:
            raise ValueError(
                f"Unsupported AI provider: {AI_PROVIDER}"
            )
        
        return provider_class()