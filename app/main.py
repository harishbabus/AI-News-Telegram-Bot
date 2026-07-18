"""
Entry point for the AI News Telegram Bot.

Workflow:
1. Fetch latest AI news.
2. Remove duplicate articles.
3. Build the Telegram digest.
4. Generate an AI summary using the configured provider.
5. Send the summary and digest to Telegram.
"""

from common.logger import logger
from common.utils import remove_duplicates
from news.fetcher import get_latest_news
from news.formatter import create_digest, split_message
from providers.provider_factory import ProviderFactory
from services.summarizer import summarize_news
from telegram.bot import send_message


def main() -> None:
    """
    Executes the AI News Telegram Bot workflow.
    """

    try:

        logger.info("Starting AI News Telegram Bot.")

        provider = ProviderFactory.get_provider()

        news = get_latest_news()
        news = remove_duplicates(news)

        logger.info("%d unique articles collected.", len(news))

        if not news:
            logger.warning("No news articles were retrieved.")
            return

        digest = create_digest(news)

        summary = summarize_news(
            news,
            provider,
        )

        messages = [
            summary,
            *split_message(digest),
        ]

        logger.info(
            "Sending %d Telegram messages.",
            len(messages),
        )

        for message in messages:
            send_message(message)

        logger.info("AI News Telegram Bot execution completed.")

    except Exception:
        logger.exception("An unexpected error occurred during bot execution.")


if __name__ == "__main__":
    main()
