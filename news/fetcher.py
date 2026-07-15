import feedparser

from common.logger import logger
from common.models import NewsArticle, NewsList
from news.sources import RSS_SOURCES


DEFAULT_LIMIT_PER_SOURCE = 3


def get_latest_news(
    limit_per_source: int = DEFAULT_LIMIT_PER_SOURCE,
) -> NewsList:
    """
    Fetches the latest news articles from all configured RSS feeds.

    Args:
        limit_per_source: Maximum number of articles to fetch from
            each RSS source.

    Returns:
        A list of NewsArticle instances.
    """

    news: NewsList = []

    for source_name, feed_url in RSS_SOURCES.items():
        try:

            logger.info("Fetching RSS feed: %s", source_name)

            feed = feedparser.parse(feed_url)
            available_articles = len(feed.entries)

            if feed.bozo:
                logger.warning(
                    "Skipping invalid RSS feed '%s': %s",
                    source_name,
                    feed.bozo_exception,
                )
                continue

            logger.info(
                "Fetched %d articles from %s",
                available_articles,
                source_name,
            )

            if available_articles == 0:
                continue

            for entry in feed.entries[:limit_per_source]:
                article = NewsArticle(
                    source=source_name,
                    title=getattr(entry, "title", ""),
                    summary=getattr(entry, "summary", ""),
                    link=getattr(entry, "link", ""),
                )

                news.append(article)

        except Exception:
            logger.exception(
                "Failed to fetch RSS feed: %s",
                source_name,
            )

    return news