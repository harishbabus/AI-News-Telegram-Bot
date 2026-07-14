from typing import Any

import feedparser

from common.logger import logger
from news.sources import RSS_SOURCES


DEFAULT_LIMIT_PER_SOURCE = 3


def get_latest_news(
    limit_per_source: int = DEFAULT_LIMIT_PER_SOURCE,
) -> list[dict[str, Any]]:
    """
    Fetches the latest news articles from all configured RSS feeds.

    Args:
        limit_per_source: Maximum number of articles to fetch from
            each RSS source.

    Returns:
        A list of news article dictionaries.
    """
    news: list[dict[str, Any]] = []

    for source_name, feed_url in RSS_SOURCES.items():
        try:
            logger.info("Fetching %s", source_name)

            feed = feedparser.parse(feed_url)

            if feed.bozo:
                logger.warning(
                    "Problem parsing %s",
                    source_name,
                )

            for entry in feed.entries[:limit_per_source]:
                article = {
                    "source": source_name,
                    "title": getattr(entry, "title", ""),
                    "summary": getattr(entry, "summary", ""),
                    "link": getattr(entry, "link", ""),
                }

                news.append(article)

        except Exception:
            logger.exception(
                "Failed to fetch RSS feed: %s",
                source_name,
            )

    return news