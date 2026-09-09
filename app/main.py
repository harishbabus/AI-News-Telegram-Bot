"""Entry point for Telegram AI Digest and email Daily Briefing delivery."""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.settings import settings
from common.logger import logger
from common.models import NewsList
from common.utils import remove_duplicates
from mailer.formatter import format_daily_briefing_html
from mailer.sender import send_email
from news.fetcher import get_latest_ai_news, get_latest_news
from news.formatter import format_telegram_editorial_digest, split_message
from news.sources import CATEGORY_AI
from providers.base_provider import AIProvider
from providers.provider_factory import ProviderFactory
from services.article_verifier import verify_articles
from services.briefing_service import generate_daily_briefing
from services.editorial_scoring import select_editorial_candidates
from services.summarizer import summarize_news
from telegram.bot import send_message

IST = ZoneInfo("Asia/Kolkata")


def _send_telegram_ai_digest(provider: AIProvider, ai_news: NewsList) -> None:
    """Generate and send the editorial AI-only digest to Telegram."""
    logger.info("%d unique AI articles collected for Telegram.", len(ai_news))

    if not ai_news:
        logger.warning("No AI news articles were retrieved for Telegram.")
        return

    digest = summarize_news(ai_news, provider)
    telegram_digest = format_telegram_editorial_digest(digest)
    messages = split_message(telegram_digest)

    logger.info("Sending %d Telegram AI Digest messages.", len(messages))
    for message in messages:
        send_message(message)


def _send_email_daily_briefing(provider: AIProvider, briefing_news: NewsList) -> None:
    """Generate and send the broader four-section briefing by email only."""
    if not settings.email_enabled:
        logger.info("Email delivery is disabled; skipping Daily Briefing email.")
        return

    logger.info(
        "%d unique articles collected for the email Daily Briefing.",
        len(briefing_news),
    )

    if not briefing_news:
        logger.warning("No news articles were retrieved for the email Daily Briefing.")
        return

    briefing = generate_daily_briefing(briefing_news, provider)
    today = datetime.now(IST).strftime("%d %B %Y")
    html_briefing = format_daily_briefing_html(briefing, today)

    sent = send_email(
        sender=settings.email_from,
        recipient=settings.email_to,
        app_password=settings.email_app_password,
        smtp_host=settings.email_smtp_host,
        smtp_port=settings.email_smtp_port,
        subject=f"Daily Briefing — {today}",
        body=briefing,
        html_body=html_briefing,
    )

    if not sent:
        logger.warning("Daily briefing email could not be sent.")


def _collect_and_verify_news() -> tuple[NewsList, NewsList]:
    """Fetch once when email is enabled and reuse AI items for Telegram."""
    if settings.email_enabled:
        all_news = remove_duplicates(get_latest_news())
        logger.info(
            "%d unique briefing candidates after freshness filtering.",
            len(all_news),
        )
        preselected = select_editorial_candidates(
            all_news,
            max_per_category=8,
            max_per_publisher=3,
        )
        verified_news = verify_articles(preselected)
        briefing_news = select_editorial_candidates(
            verified_news,
            max_per_category=6,
            max_per_publisher=2,
        )
        ai_news = [
            article for article in briefing_news if article.category == CATEGORY_AI
        ]
        return ai_news, briefing_news

    ai_news = remove_duplicates(get_latest_ai_news())
    logger.info("%d unique AI candidates after freshness filtering.", len(ai_news))
    preselected_ai = select_editorial_candidates(
        ai_news,
        max_per_category=10,
        max_per_publisher=4,
    )
    verified_ai_news = verify_articles(preselected_ai)
    selected_ai_news = select_editorial_candidates(
        verified_ai_news,
        max_per_category=8,
        max_per_publisher=3,
    )
    return selected_ai_news, []


def main() -> None:
    """Fetch/verify once, then deliver Telegram digest and email briefing."""
    try:
        logger.info("Starting AI News + Daily Briefing bot.")
        provider = ProviderFactory.get_provider()
        ai_news, briefing_news = _collect_and_verify_news()

        _send_telegram_ai_digest(provider, ai_news)
        _send_email_daily_briefing(provider, briefing_news)

        logger.info("AI News + Daily Briefing bot execution completed.")

    except Exception:
        logger.exception("An unexpected error occurred during bot execution.")


if __name__ == "__main__":
    main()
