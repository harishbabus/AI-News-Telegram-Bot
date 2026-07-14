from typing import Any

from common.logger import logger
from providers.provider_factory import ProviderFactory

def summarize_news(news: list[dict[str, Any]]) -> str:
    """
    Generates an AI summary of the collected news articles.

    The configured AI provider is selected using the ProviderFactory.

    Args:
        news: List of news article dictionaries.

    Returns:
        A summarized string containing the key highlights.
    """

    logger.info("Summarizing %d news articles.", len(news))
    
    provider = ProviderFactory.get_provider()
    summary = provider.summarize(news)
    
    logger.info("News summarization completed.")
    
    return summary