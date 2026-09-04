"""Unit tests for app.main."""

from dataclasses import replace
from unittest.mock import MagicMock, call, patch

from app.main import main
from app.settings import settings
from tests.types import ArticleFactory


def _settings_with_email_disabled():
    return replace(settings, email_enabled=False)


def _settings_with_email_enabled():
    return replace(
        settings,
        email_enabled=True,
        email_from="from@example.com",
        email_to="to@example.com",
        email_app_password="secret",
    )


def test_main_single_fetch_reuses_ai_for_telegram_and_email(
    article_factory: ArticleFactory,
) -> None:
    ai_article = article_factory(title="AI Telegram Story")
    market_article = article_factory(
        source="Business & Markets News",
        title="Market Story",
        category="Business & Markets",
    )
    all_news = [ai_article, market_article]

    with (
        patch("app.main.settings", _settings_with_email_enabled()),
        patch("app.main.get_latest_news", return_value=all_news) as mock_all_fetch,
        patch("app.main.get_latest_ai_news") as mock_ai_fetch,
        patch("app.main.remove_duplicates", return_value=all_news),
        patch("app.main.verify_articles", return_value=all_news) as mock_verify,
        patch("app.main.ProviderFactory.get_provider", return_value=MagicMock()),
        patch(
            "app.main.summarize_news", return_value="Editorial AI Digest"
        ) as mock_summary,
        patch(
            "app.main.format_telegram_editorial_digest",
            return_value="Formatted AI Digest",
        ),
        patch("app.main.split_message", return_value=["Formatted AI Digest"]),
        patch(
            "app.main.generate_daily_briefing", return_value="New Daily Briefing"
        ) as mock_brief,
        patch(
            "app.main.format_daily_briefing_html", return_value="<html>Briefing</html>"
        ),
        patch("app.main.send_message") as mock_send,
        patch("app.main.send_email", return_value=True) as mock_email,
    ):
        main()

    mock_all_fetch.assert_called_once_with()
    mock_ai_fetch.assert_not_called()
    mock_verify.assert_called_once_with(all_news)
    mock_summary.assert_called_once()
    assert mock_summary.call_args.args[0] == [ai_article]
    mock_brief.assert_called_once_with(all_news, mock_brief.call_args.args[1])
    mock_send.assert_called_once_with("Formatted AI Digest")
    mock_email.assert_called_once()


def test_main_email_disabled_fetches_ai_only(article_factory: ArticleFactory) -> None:
    article = article_factory()

    with (
        patch("app.main.settings", _settings_with_email_disabled()),
        patch("app.main.get_latest_ai_news", return_value=[article]) as mock_ai_fetch,
        patch("app.main.get_latest_news") as mock_all_fetch,
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.verify_articles", return_value=[article]),
        patch("app.main.ProviderFactory.get_provider", return_value=MagicMock()),
        patch("app.main.summarize_news", return_value="Digest"),
        patch("app.main.format_telegram_editorial_digest", return_value="Digest"),
        patch("app.main.split_message", return_value=["Digest"]),
        patch("app.main.send_message") as mock_send,
        patch("app.main.send_email") as mock_email,
    ):
        main()

    mock_ai_fetch.assert_called_once_with()
    mock_all_fetch.assert_not_called()
    mock_send.assert_called_once_with("Digest")
    mock_email.assert_not_called()


def test_main_no_ai_news_still_sends_email_briefing(
    article_factory: ArticleFactory,
) -> None:
    market = article_factory(category="Business & Markets")

    with (
        patch("app.main.settings", _settings_with_email_enabled()),
        patch("app.main.get_latest_news", return_value=[market]),
        patch("app.main.remove_duplicates", return_value=[market]),
        patch("app.main.verify_articles", return_value=[market]),
        patch("app.main.ProviderFactory.get_provider", return_value=MagicMock()),
        patch("app.main.generate_daily_briefing", return_value="Briefing"),
        patch(
            "app.main.format_daily_briefing_html", return_value="<html>Briefing</html>"
        ),
        patch("app.main.send_message") as mock_send,
        patch("app.main.send_email", return_value=True) as mock_email,
    ):
        main()

    mock_send.assert_not_called()
    mock_email.assert_called_once()


def test_main_no_news_does_not_send_anything() -> None:
    with (
        patch("app.main.settings", _settings_with_email_enabled()),
        patch("app.main.get_latest_news", return_value=[]),
        patch("app.main.remove_duplicates", return_value=[]),
        patch("app.main.verify_articles", return_value=[]),
        patch("app.main.ProviderFactory.get_provider", return_value=MagicMock()),
        patch("app.main.send_message") as mock_send,
        patch("app.main.send_email") as mock_email,
    ):
        main()

    mock_send.assert_not_called()
    mock_email.assert_not_called()


def test_main_splits_multiple_telegram_messages(
    article_factory: ArticleFactory,
) -> None:
    article = article_factory()

    with (
        patch("app.main.settings", _settings_with_email_disabled()),
        patch("app.main.get_latest_ai_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.verify_articles", return_value=[article]),
        patch("app.main.ProviderFactory.get_provider", return_value=MagicMock()),
        patch("app.main.summarize_news", return_value="Digest"),
        patch("app.main.format_telegram_editorial_digest", return_value="Digest"),
        patch("app.main.split_message", return_value=["Part 1", "Part 2"]),
        patch("app.main.send_message") as mock_send,
    ):
        main()

    mock_send.assert_has_calls([call("Part 1"), call("Part 2")])


def test_main_handles_unexpected_exception() -> None:
    with (
        patch(
            "app.main.ProviderFactory.get_provider", side_effect=RuntimeError("Boom")
        ),
        patch("app.main.logger.exception") as mock_exception,
    ):
        main()

    mock_exception.assert_called_once_with(
        "An unexpected error occurred during bot execution."
    )
