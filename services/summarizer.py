from common.logger import logger
from common.models import NewsList
from prompts.telegram_summary_prompt import build_telegram_summary_prompt
from providers.base_provider import AIProvider
from services.fallback_renderer import build_telegram_fallback


def summarize_news(news: NewsList, provider: AIProvider) -> str:
    """Generate the editorial AI-only Telegram digest."""
    if not news:
        logger.warning("No news articles available for summarization.")
        return "No news articles available."

    logger.info(
        "Summarizing %d articles for Telegram using %s.",
        len(news),
        provider.__class__.__name__,
    )

    try:
        prompt = build_telegram_summary_prompt(news)
        summary = provider.summarize(news, prompt=prompt).strip()
        if not summary:
            raise RuntimeError("AI provider returned an empty Telegram digest.")
        logger.info("Telegram AI digest summarization completed.")
        return summary
    except Exception:
        logger.exception(
            "News summarization failed; using deterministic Telegram fallback."
        )
        return build_telegram_fallback(news)
