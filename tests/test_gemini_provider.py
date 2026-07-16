"""
Unit tests for providers.gemini_provider.
"""

from unittest.mock import MagicMock, patch

import pytest

from providers.gemini_provider import GeminiProvider
from tests.types import ArticleFactory


def test_gemini_provider_initializes_client() -> None:
    """
    Creates a Gemini client during initialization.
    """
    with patch(
        "providers.gemini_provider.genai.Client",
    ) as mock_client:

        provider = GeminiProvider()

    mock_client.assert_called_once()
    assert provider.client == mock_client.return_value


def test_summarize_returns_summary(
    article_factory: ArticleFactory,
) -> None:
    """
    Returns the generated summary from Gemini.
    """
    article = article_factory()

    response = MagicMock()
    response.text = "AI Daily Brief"

    with (
        patch(
            "providers.gemini_provider.genai.Client",
        ) as mock_client,
        patch(
            "providers.gemini_provider.build_news_prompt",
            return_value="Prompt",
        ) as mock_prompt,
    ):
        mock_client.return_value.models.generate_content.return_value = response

        provider = GeminiProvider()

        summary = provider.summarize([article])

    assert summary == "AI Daily Brief"

    mock_prompt.assert_called_once_with([article])

    mock_client.return_value.models.generate_content.assert_called_once()


def test_summarize_uses_correct_model(
    article_factory: ArticleFactory,
) -> None:
    """
    Uses the configured Gemini model.
    """
    article = article_factory()

    response = MagicMock()
    response.text = "Summary"

    with (
        patch(
            "providers.gemini_provider.genai.Client",
        ) as mock_client,
        patch(
            "providers.gemini_provider.build_news_prompt",
            return_value="Prompt",
        ),
        patch(
            "providers.gemini_provider.GEMINI_MODEL",
            "gemini-test-model",
        ),
    ):
        mock_client.return_value.models.generate_content.return_value = response

        provider = GeminiProvider()

        provider.summarize([article])

    mock_client.return_value.models.generate_content.assert_called_once_with(
        model="gemini-test-model",
        contents="Prompt",
    )


def test_summarize_raises_when_response_is_empty(
    article_factory: ArticleFactory,
) -> None:
    """
    Raises RuntimeError when Gemini returns no text.
    """
    article = article_factory()

    response = MagicMock()
    response.text = ""

    with (
        patch(
            "providers.gemini_provider.genai.Client",
        ) as mock_client,
        patch(
            "providers.gemini_provider.build_news_prompt",
            return_value="Prompt",
        ),
    ):
        mock_client.return_value.models.generate_content.return_value = response

        provider = GeminiProvider()

        with pytest.raises(RuntimeError):
            provider.summarize([article])


def test_summarize_propagates_generate_content_exception(
    article_factory: ArticleFactory,
) -> None:
    """
    Propagates exceptions raised by Gemini.
    """
    article = article_factory()

    with (
        patch(
            "providers.gemini_provider.genai.Client",
        ) as mock_client,
        patch(
            "providers.gemini_provider.build_news_prompt",
            return_value="Prompt",
        ),
    ):
        mock_client.return_value.models.generate_content.side_effect = RuntimeError(
            "API Error",
        )

        provider = GeminiProvider()

        with pytest.raises(RuntimeError):
            provider.summarize([article])


def test_summarize_logs_success(
    article_factory: ArticleFactory,
) -> None:
    """
    Logs successful summarization.
    """
    article = article_factory()

    response = MagicMock()
    response.text = "Summary"

    with (
        patch(
            "providers.gemini_provider.genai.Client",
        ) as mock_client,
        patch(
            "providers.gemini_provider.build_news_prompt",
            return_value="Prompt",
        ),
        patch(
            "providers.gemini_provider.logger.info",
        ) as mock_logger,
    ):
        mock_client.return_value.models.generate_content.return_value = response

        provider = GeminiProvider()

        provider.summarize([article])

    mock_logger.assert_any_call("Generating summary using Gemini.")
    mock_logger.assert_any_call("Gemini summary generated successfully.")


def test_summarize_logs_failure(
    article_factory: ArticleFactory,
) -> None:
    """
    Logs failures before re-raising the exception.
    """
    article = article_factory()

    with (
        patch(
            "providers.gemini_provider.genai.Client",
        ) as mock_client,
        patch(
            "providers.gemini_provider.build_news_prompt",
            return_value="Prompt",
        ),
        patch(
            "providers.gemini_provider.logger.exception",
        ) as mock_logger,
    ):
        mock_client.return_value.models.generate_content.side_effect = RuntimeError(
            "Failure",
        )

        provider = GeminiProvider()

        with pytest.raises(RuntimeError):
            provider.summarize([article])

    mock_logger.assert_called_once_with(
        "Gemini summarization failed.",
    )
