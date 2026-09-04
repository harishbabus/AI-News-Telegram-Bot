"""
Unit tests for news.fetcher.
"""

from types import SimpleNamespace
from unittest.mock import patch

from common.models import NewsArticle, NewsList
from news.fetcher import get_latest_news
from news.sources import RSS_SOURCES


def test_get_latest_news_returns_articles(
    fake_feed: SimpleNamespace,
) -> None:
    """
    Returns NewsArticle instances when RSS feeds contain entries.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=fake_feed,
    ):
        news: NewsList = get_latest_news(limit_per_source=1)

    assert len(news) == len(RSS_SOURCES)

    article = news[0]

    assert isinstance(article, NewsArticle)
    assert article.title == "GPT-5 Released"
    assert article.summary == "OpenAI announced GPT-5."
    assert article.link == "https://example.com"


def test_get_latest_news_respects_limit(
    many_entries_feed: SimpleNamespace,
) -> None:
    """
    Fetches no more than the configured number of articles
    from each RSS feed.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=many_entries_feed,
    ):
        news: NewsList = get_latest_news(limit_per_source=2)

    assert len(news) == len(RSS_SOURCES) * 2


def test_get_latest_news_returns_empty_list(
    empty_feed: SimpleNamespace,
) -> None:
    """
    Returns an empty list when every RSS feed has no entries.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=empty_feed,
    ):
        news: NewsList = get_latest_news()

    assert len(news) == 0


def test_get_latest_news_handles_feedparser_exception() -> None:
    """
    Returns an empty list when feedparser raises an exception.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        side_effect=Exception("RSS unavailable"),
    ):
        news: NewsList = get_latest_news()

    assert len(news) == 0


def test_get_latest_news_keeps_entries_when_feed_has_parser_warning(
    malformed_feed: SimpleNamespace,
) -> None:
    """A MIME/parser warning must not discard successfully parsed entries."""
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=malformed_feed,
    ):
        news: NewsList = get_latest_news(limit_per_source=1)

    assert len(news) == len(RSS_SOURCES)


def test_get_latest_news_logs_warning_for_malformed_feed(
    malformed_feed: SimpleNamespace,
) -> None:
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
        "RSS feed '%s' reported a parser warning but returned %d "
        "entries; continuing: %s",
        "Anthropic",
        1,
        malformed_feed.bozo_exception,
    )


def test_get_latest_news_returns_news_article_instances(
    fake_feed: SimpleNamespace,
) -> None:
    """
    Returns NewsArticle objects.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=fake_feed,
    ):
        news: NewsList = get_latest_news(limit_per_source=1)

    assert all(isinstance(article, NewsArticle) for article in news)


def test_get_latest_news_calls_feedparser_for_each_source(
    fake_feed: SimpleNamespace,
) -> None:
    """
    Calls feedparser once for every configured RSS source.
    """
    with patch(
        "news.fetcher.feedparser.parse",
        return_value=fake_feed,
    ) as mock_parse:
        get_latest_news()

    assert mock_parse.call_count == len(RSS_SOURCES)


def test_get_latest_ai_news_uses_only_ai_sources(
    fake_feed: SimpleNamespace,
) -> None:
    """Telegram fetcher uses only the original AI source set."""
    from news.fetcher import get_latest_ai_news
    from news.sources import AI_RSS_SOURCES

    with patch(
        "news.fetcher.feedparser.parse",
        return_value=fake_feed,
    ) as mock_parse:
        news: NewsList = get_latest_ai_news(limit_per_source=1)

    assert len(news) == len(AI_RSS_SOURCES)
    assert mock_parse.call_count == len(AI_RSS_SOURCES)
    assert all(article.category == "AI & LLMs" for article in news)


def test_fetcher_filters_stale_dated_articles() -> None:
    from datetime import UTC, datetime, timedelta
    from time import gmtime

    from news.fetcher import _fetch_news

    now = datetime(2026, 9, 4, 12, 0, tzinfo=UTC)
    stale = now - timedelta(days=10)
    entry = SimpleNamespace(
        title="Old AI story",
        summary="Old summary",
        link="https://example.com/old",
        published_parsed=gmtime(stale.timestamp()),
        published="25 Aug 2026 12:00:00 +0000",
    )
    feed = SimpleNamespace(entries=[entry], bozo=False)

    with patch("news.fetcher.feedparser.parse", return_value=feed):
        result = _fetch_news({"OpenAI": "https://example.com/rss"}, 4, now=now)

    assert result == []


def test_fetcher_keeps_recent_article_and_captures_publisher() -> None:
    from datetime import UTC, datetime, timedelta
    from time import gmtime

    from news.fetcher import _fetch_news

    now = datetime(2026, 9, 4, 12, 0, tzinfo=UTC)
    recent = now - timedelta(hours=2)
    entry = SimpleNamespace(
        title="Important AI story",
        summary="Summary",
        link="https://example.com/story",
        published_parsed=gmtime(recent.timestamp()),
        published="04 Sep 2026 10:00:00 +0000",
        source=SimpleNamespace(title="Reuters"),
    )
    feed = SimpleNamespace(entries=[entry], bozo=False)

    with patch("news.fetcher.feedparser.parse", return_value=feed):
        result = _fetch_news(
            {"AI Industry News": "https://example.com/rss"}, 4, now=now
        )

    assert len(result) == 1
    assert result[0].publisher == "Reuters"
    assert result[0].source_quality == "established"
    assert result[0].published_at.startswith("2026-09-04T10:00:00")


def test_fetcher_rejects_implausibly_future_dated_article() -> None:
    from datetime import UTC, datetime, timedelta
    from time import gmtime

    from news.fetcher import _fetch_news

    now = datetime(2026, 9, 4, 12, 0, tzinfo=UTC)
    future = now + timedelta(days=2)
    entry = SimpleNamespace(
        title="Future story",
        summary="Summary",
        link="https://example.com/future",
        published_parsed=gmtime(future.timestamp()),
    )
    feed = SimpleNamespace(entries=[entry], bozo=False)

    with patch("news.fetcher.feedparser.parse", return_value=feed):
        result = _fetch_news({"OpenAI": "https://example.com/rss"}, 4, now=now)

    assert result == []
