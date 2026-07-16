"""
Unit tests for ProviderFactory.
"""

from unittest.mock import patch

import pytest

from providers.base_provider import AIProvider
from providers.gemini_provider import GeminiProvider
from providers.openai_provider import OpenAIProvider
from providers.provider_factory import ProviderFactory


def test_returns_gemini_provider() -> None:
    """
    Returns a GeminiProvider when AI_PROVIDER is 'gemini'.
    """
    with patch(
        "providers.provider_factory.AI_PROVIDER",
        "gemini",
    ):
        provider = ProviderFactory.get_provider()

    assert isinstance(provider, GeminiProvider)
    assert isinstance(provider, AIProvider)


def test_returns_openai_provider() -> None:
    """
    Returns an OpenAIProvider when AI_PROVIDER is 'openai'.
    """
    with patch(
        "providers.provider_factory.AI_PROVIDER",
        "openai",
    ):
        provider = ProviderFactory.get_provider()

    assert isinstance(provider, OpenAIProvider)
    assert isinstance(provider, AIProvider)


def test_raises_error_for_unknown_provider() -> None:
    """
    Raises ValueError for an unsupported provider.
    """
    with patch(
        "providers.provider_factory.AI_PROVIDER",
        "unknown",
    ):
        with pytest.raises(
            ValueError,
            match="Unsupported AI provider: unknown",
        ):
            ProviderFactory.get_provider()


def test_logs_selected_provider() -> None:
    """
    Logs the configured AI provider.
    """
    with (
        patch(
            "providers.provider_factory.AI_PROVIDER",
            "gemini",
        ),
        patch(
            "providers.provider_factory.logger.info",
        ) as mock_logger,
    ):
        ProviderFactory.get_provider()

    mock_logger.assert_called_once_with(
        "Using AI provider: %s",
        "gemini",
    )
