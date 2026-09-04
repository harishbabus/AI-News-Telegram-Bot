"""Shared pytest fixtures."""

from collections.abc import Callable
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from common.models import NewsArticle
from providers.base_provider import AIProvider


@pytest.fixture
def article_factory() -> Callable[..., NewsArticle]:
    def _create(
        source: str = "OpenAI",
        title: str = "Sample Title",
        summary: str = "Sample Summary",
        link: str = "https://example.com",
        category: str = "AI & LLMs",
        published: str = "",
    ) -> NewsArticle:
        return NewsArticle(
            source=source,
            title=title,
            summary=summary,
            link=link,
            category=category,
            published=published,
        )

    return _create


@pytest.fixture
def fake_feed_entry() -> SimpleNamespace:
    return SimpleNamespace(
        title="GPT-5 Released",
        summary="OpenAI announced GPT-5.",
        link="https://example.com",
    )


@pytest.fixture
def fake_feed(fake_feed_entry: SimpleNamespace) -> SimpleNamespace:
    return SimpleNamespace(entries=[fake_feed_entry], bozo=False)


@pytest.fixture
def many_entries_feed() -> SimpleNamespace:
    entries = [
        SimpleNamespace(
            title=f"Article {i}",
            summary=f"Summary {i}",
            link=f"https://example.com/{i}",
        )
        for i in range(10)
    ]
    return SimpleNamespace(entries=entries, bozo=False)


@pytest.fixture
def empty_feed() -> SimpleNamespace:
    return SimpleNamespace(entries=[], bozo=False)


@pytest.fixture
def malformed_feed(fake_feed_entry: SimpleNamespace) -> SimpleNamespace:
    return SimpleNamespace(
        entries=[fake_feed_entry],
        bozo=True,
        bozo_exception=Exception("Malformed XML"),
    )


@pytest.fixture
def provider() -> Mock:
    return Mock(spec=AIProvider)
