"""Tests for deterministic delivery fallbacks."""

from services.fallback_renderer import (
    build_daily_briefing_fallback,
    build_telegram_fallback,
)
from tests.types import ArticleFactory


def test_telegram_fallback_keeps_editorial_sections(
    article_factory: ArticleFactory,
) -> None:
    news = [
        article_factory(title="New AI agent tool released"),
        article_factory(title="Research benchmark improves model evaluation"),
    ]
    result = build_telegram_fallback(news)

    assert "🔥 TOP STORIES" in result
    assert "🛠️ NEW AI TOOLS" in result
    assert "🔬 RESEARCH HIGHLIGHTS" in result
    assert "🎯 WHY TODAY'S NEWS MATTERS" in result


def test_email_fallback_keeps_briefing_contract(
    article_factory: ArticleFactory,
) -> None:
    news = [
        article_factory(
            title="AI Story",
            category="AI & LLMs",
            link="https://example.com/ai",
        ),
        article_factory(
            title="Market Story",
            category="Business & Markets",
            link="https://example.com/market",
        ),
    ]
    result = build_daily_briefing_fallback(news)

    assert "📰 Daily Briefing" in result
    assert "Today’s signal" in result
    assert "🤖 AI & LLMs" in result
    assert "💹 Business & Markets" in result
    assert "🎯 What matters most today" in result
    assert "Source: https://example.com/ai" in result
