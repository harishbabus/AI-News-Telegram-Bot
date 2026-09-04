"""Unit tests for prompts.news_summary_prompt."""

from common.models import NewsList
from prompts.news_summary_prompt import build_news_prompt
from tests.types import ArticleFactory


def test_build_news_prompt_empty_news() -> None:
    news: NewsList = []
    prompt = build_news_prompt(news)
    assert "concise executive daily briefing" in prompt
    assert "## Articles" in prompt


def test_build_news_prompt_single_article(article_factory: ArticleFactory) -> None:
    article = article_factory(
        source="OpenAI",
        title="Model Released",
        summary="A new model was announced.",
        link="https://example.com",
    )
    prompt = build_news_prompt([article])
    assert "Article 1" in prompt
    assert "OpenAI" in prompt
    assert "Model Released" in prompt
    assert "https://example.com" in prompt


def test_build_news_prompt_contains_required_sections(
    article_factory: ArticleFactory,
) -> None:
    prompt = build_news_prompt([article_factory()])
    assert "🤖 AI & LLMs" in prompt
    assert "🐍 Python & Software Development" in prompt
    assert "📡 Telecom / BSS" in prompt
    assert "💹 Business & Markets" in prompt
    assert "🎯 What matters most today" in prompt
    assert "Exclude sports and entertainment completely." in prompt
    assert "Never pad a section." in prompt
