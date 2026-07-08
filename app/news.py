import feedparser
from sources import RSS_SOURCES

def get_latest_news(limit_per_source=3):

    news = []

    for source_name, rss_url in RSS_SOURCES.items():

        feed = feedparser.parse(rss_url)

        for entry in feed.entries[:limit_per_source]:

            news.append({
                "source": source_name,
                "title": entry.title,
                "link": entry.link
            })

    return news