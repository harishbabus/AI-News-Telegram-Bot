from common.logger import logger
from common.models import NewsList
from providers.base_provider import AIProvider


def summarize_news(news: NewsList, provider: AIProvider) -> str:
    """
    Generates an AI summary of the collected news articles.

    Args:
        news: News articles to summarize.
        provider: AI provider used to generate the summary.

    Returns:
        A summarized string containing the key highlights.
    """

    if not news:
        logger.warning("No news articles available for summarization.")
        return "No news articles available."

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
