import feedparser
from sources import RSS_SOURCES
from logger import logger


def get_latest_news(limit_per_source=3):

    news = []

    for source_name, rss_url in RSS_SOURCES.items():

        try:

            logger.info(f"Fetching {source_name}")

            feed = feedparser.parse(rss_url)

            if feed.bozo:
                logger.warning(f"Problem parsing {source_name}")

            for entry in feed.entries[:limit_per_source]:

                news.append({
                    "source": source_name,
                    "title": entry.title,
                    "summary": getattr(entry, "summary", ""),
                    "link": entry.link
                })

        except Exception as e:

            logger.error(f"{source_name} failed: {e}")

    return news