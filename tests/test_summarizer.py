"""Unit tests for services.summarizer."""

from unittest.mock import MagicMock, patch

from providers.base_provider import AIProvider
from services.summarizer import summarize_news
from tests.types import ArticleFactory


def test_summarize_news_returns_summary(article_factory: ArticleFactory) -> None:
    article = article_factory()
    provider: MagicMock = MagicMock(spec=AIProvider)
    provider.summarize.return_value = "AI Summary"

    with patch(
        "services.summarizer.build_telegram_summary_prompt",
        return_value="Telegram Prompt",
    ):
        result = summarize_news([article], provider)

    assert result == "AI Summary"
    provider.summarize.assert_called_once_with([article], prompt="Telegram Prompt")


def test_summarize_news_empty_news() -> None:
    provider: MagicMock = MagicMock(spec=AIProvider)
    result = summarize_news([], provider)
    assert result == "No news articles available."
    provider.summarize.assert_not_called()


def test_summarize_news_calls_provider_once(article_factory: ArticleFactory) -> None:
    article = article_factory()
    provider: MagicMock = MagicMock(spec=AIProvider)
    provider.summarize.return_value = "Summary"

    with patch(
        "services.summarizer.build_telegram_summary_prompt",
        return_value="Telegram Prompt",
    ):
        summarize_news([article], provider)

    provider.summarize.assert_called_once_with([article], prompt="Telegram Prompt")


def test_summarize_news_handles_provider_exception(
    article_factory: ArticleFactory,
) -> None:
    article = article_factory()
    provider: MagicMock = MagicMock(spec=AIProvider)
    provider.summarize.side_effect = RuntimeError("API failed")

    result = summarize_news([article], provider)
    assert "🔥 TOP STORIES" in result
    assert article.title in result
    assert "Gemini was temporarily unavailable" in result


def test_summarize_news_logs_info(article_factory: ArticleFactory) -> None:
    article = article_factory()
    provider: MagicMock = MagicMock(spec=AIProvider)
    provider.summarize.return_value = "Summary"

    with (
        patch("services.summarizer.logger.info") as mock_info,
        patch(
            "services.summarizer.build_telegram_summary_prompt",
            return_value="Prompt",
        ),
    ):
        summarize_news([article], provider)

    mock_info.assert_any_call(
        "Summarizing %d articles for Telegram using %s.",
        1,
        provider.__class__.__name__,
    )
    mock_info.assert_any_call("Telegram AI digest summarization completed.")


def test_summarize_news_logs_warning_for_empty_news() -> None:
    provider: MagicMock = MagicMock(spec=AIProvider)
    with patch("services.summarizer.logger.warning") as mock_warning:
        summarize_news([], provider)
    mock_warning.assert_called_once_with(
        "No news articles available for summarization."
    )
