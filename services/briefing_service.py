from common.logger import logger
from common.models import NewsList
from providers.base_provider import AIProvider


FALLBACK_MESSAGE = "Unable to generate the daily briefing."


def generate_daily_briefing(news: NewsList, provider: AIProvider) -> str:
    """Generate the final curated four-topic briefing."""
    if not news:
        logger.warning("No news articles available for the daily briefing.")
        return "No major news articles were retrieved today."

    logger.info(
        "Generating daily briefing from %d articles using %s.",
        len(news),
        provider.__class__.__name__,
    )

    try:
        briefing = provider.summarize(news).strip()
        if not briefing:
            raise RuntimeError("AI provider returned an empty briefing.")

        logger.info("Daily briefing generated successfully.")
        return briefing
    except Exception:
        logger.exception("Daily briefing generation failed.")
        return FALLBACK_MESSAGE
