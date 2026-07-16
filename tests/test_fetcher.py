"""
Unit tests for news.fetcher.
"""

from unittest.mock import patch

from common.models import NewsArticle
from news.fetcher import get_latest_news
from news.sources import RSS_SOURCES


def test_get_latest_news_returns_articles(fake_feed):
    """
    Returns NewsArticle instances when RSS feeds contain entries.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=fake_feed,
    ):
        news = get_latest_news(limit_per_source=1)

    assert len(news) == len(RSS_SOURCES)

    article = news[0]

    assert isinstance(article, NewsArticle)
    assert article.title == "GPT-5 Released"
    assert article.summary == "OpenAI announced GPT-5."
    assert article.link == "https://example.com"


def test_get_latest_news_respects_limit(many_entries_feed):
    """
    Fetches no more than the configured number of articles
    from each RSS feed.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=many_entries_feed,
    ):
        news = get_latest_news(limit_per_source=2)

    assert len(news) == len(RSS_SOURCES) * 2


def test_get_latest_news_returns_empty_list(empty_feed):
    """
    Returns an empty list when every RSS feed has no entries.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=empty_feed,
    ):
        news = get_latest_news()

    assert len(news) == 0


def test_get_latest_news_handles_feedparser_exception():
    """
    Returns an empty list when feedparser raises an exception.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        side_effect=Exception("RSS unavailable"),
    ):
        news = get_latest_news()

    assert len(news) == 0


def test_get_latest_news_skips_malformed_feed(malformed_feed):
    """
    Skips malformed RSS feeds.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=malformed_feed,
    ):
        news = get_latest_news(limit_per_source=1)

    assert len(news) == 0


def test_get_latest_news_logs_warning_for_malformed_feed(
    malformed_feed,
):
    """
    Logs a warning when a malformed RSS feed is encountered.
    """
    with (
        patch(
            "news.fetcher.feedparser.parse",
            return_value=malformed_feed,
        ),
        patch("news.fetcher.logger.warning") as mock_warning,
    ):
        get_latest_news()

    assert mock_warning.call_count == len(RSS_SOURCES)

    mock_warning.assert_any_call(
        "Skipping invalid RSS feed '%s': %s",
        "Anthropic",
        malformed_feed.bozo_exception,
    )


def test_get_latest_news_returns_news_article_instances(fake_feed):
    """
    Returns NewsArticle objects.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=fake_feed,
    ):
        news = get_latest_news(limit_per_source=1)

    assert all(
        isinstance(article, NewsArticle)
        for article in news
    )


def test_get_latest_news_calls_feedparser_for_each_source(
    fake_feed,
):
    """
    Calls feedparser once for every configured RSS source.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=fake_feed,
    ) as mock_parse:
        get_latest_news()

    assert mock_parse.call_count == len(RSS_SOURCES)