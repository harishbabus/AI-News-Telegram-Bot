from unittest.mock import Mock

from services.briefing_service import FALLBACK_MESSAGE, generate_daily_briefing
from tests.types import ArticleFactory


def test_generate_daily_briefing(article_factory: ArticleFactory) -> None:
    article = article_factory()
    provider = Mock()
    provider.summarize.return_value = "Daily Briefing"

    result = generate_daily_briefing([article], provider)

    assert result == "Daily Briefing"
    provider.summarize.assert_called_once_with([article])


def test_generate_daily_briefing_handles_provider_error(
    article_factory: ArticleFactory,
) -> None:
    provider = Mock()
    provider.summarize.side_effect = RuntimeError("failure")

    result = generate_daily_briefing([article_factory()], provider)

    assert result == FALLBACK_MESSAGE
