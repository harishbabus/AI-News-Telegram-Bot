"""
Shared pytest fixtures.
"""

from collections.abc import Callable
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from common.models import NewsArticle
from providers.base_provider import AIProvider


@pytest.fixture
def article_factory() -> Callable[..., NewsArticle]:
    """
    Factory fixture for creating NewsArticle instances.
    """

    def _create(
        source: str = "OpenAI",
        title: str = "Sample Title",
        summary: str = "Sample Summary",
        link: str = "https://example.com",
    ) -> NewsArticle:
        return NewsArticle(
            source=source,
            title=title,
            summary=summary,
            link=link,
        )

    return _create


# ----------------------------------------------------------------------
# RSS Feed Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def fake_feed_entry() -> SimpleNamespace:
    """
    Returns a fake RSS feed entry.
    """
    return SimpleNamespace(
        title="GPT-5 Released",
        summary="OpenAI announced GPT-5.",
        link="https://example.com",
    )


@pytest.fixture
def fake_feed(
    fake_feed_entry: SimpleNamespace,
) -> SimpleNamespace:
    """
    Returns a valid RSS feed containing one article.
    """
    return SimpleNamespace(
        entries=[fake_feed_entry],
        bozo=False,
    )


@pytest.fixture
def many_entries_feed() -> SimpleNamespace:
    """
    Returns a valid RSS feed containing multiple articles.
    """
    entries = [
        SimpleNamespace(
            title=f"Article {i}",
            summary=f"Summary {i}",
            link=f"https://example.com/{i}",
        )
        for i in range(10)
    ]

    return SimpleNamespace(
        entries=entries,
        bozo=False,
    )


@pytest.fixture
def empty_feed() -> SimpleNamespace:
    """
    Returns an empty RSS feed.
    """
    return SimpleNamespace(
        entries=[],
        bozo=False,
    )


@pytest.fixture
def malformed_feed(
    fake_feed_entry: SimpleNamespace,
) -> SimpleNamespace:
    """
    Returns a malformed RSS feed.
    """
    return SimpleNamespace(
        entries=[fake_feed_entry],
        bozo=True,
        bozo_exception=Exception("Malformed XML"),
    )


@pytest.fixture
def provider() -> Mock:
    """
    Returns a mocked AI provider.
    """
    return Mock(spec=AIProvider)
