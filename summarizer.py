from config import AI_PROVIDER

from providers.openai_provider import OpenAIProvider
from providers.gemini_provider import GeminiProvider


def summarize_news(news):

    providers = {
        "openai": OpenAIProvider(),
        "gemini": GeminiProvider(),
    }

    provider = providers.get(AI_PROVIDER)

    if provider is None:
        raise ValueError(f"Unsupported AI provider: {AI_PROVIDER}")

    return provider.summarize(news)