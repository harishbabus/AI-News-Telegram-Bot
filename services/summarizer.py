from common.logger import logger
from common.models import NewsList
from providers.provider_factory import ProviderFactory


def summarize_news(news: NewsList) -> str:
    """
    Generates an AI summary of the collected news articles.

    The configured AI provider is selected using the ProviderFactory.

    Args:
        news: News articles to summarize.

    Returns:
        A summarized string containing the key highlights.
    """

    if not news:
        logger.warning("No news articles available for summarization.")
        return "No news articles available."

    provider = ProviderFactory.get_provider()

    logger.info(
        "Summarizing %d articles using %s.",
        len(news),
        provider.__class__.__name__,
    )

    try:
        summary = provider.summarize(news)

        logger.info("News summarization completed.")

        return summary

    except Exception:
        logger.exception("News summarization failed.")
        return "Unable to generate AI summary."
