"""
Unit tests for app.main.
"""

from unittest.mock import MagicMock, call, patch

from app.main import main
from tests.types import ArticleFactory


def test_main_happy_path(
    article_factory: ArticleFactory,
) -> None:
    """
    Executes the complete workflow successfully.
    """
    article = article_factory()
    mock_provider = MagicMock()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.create_digest", return_value="Digest"),
        patch(
            "app.main.ProviderFactory.get_provider",
            return_value=mock_provider,
        ),
        patch(
            "app.main.summarize_news",
            return_value="Summary",
        ),
        patch(
            "app.main.split_message",
            return_value=[
                "Digest Part 1",
                "Digest Part 2",
            ],
        ),
        patch("app.main.send_message") as mock_send,
        patch("app.main.logger.info"),
    ):
        main()

    mock_send.assert_has_calls(
        [
            call("Summary"),
            call("Digest Part 1"),
            call("Digest Part 2"),
        ]
    )

    assert mock_send.call_count == 3


def test_main_no_news() -> None:
    """
    Stops execution when no news articles are retrieved.
    """
    with (
        patch("app.main.get_latest_news", return_value=[]),
        patch("app.main.logger.warning") as mock_warning,
        patch("app.main.send_message") as mock_send,
    ):
        main()

    mock_warning.assert_called_once_with("No news articles were retrieved.")

    mock_send.assert_not_called()


def test_main_removes_duplicates(
    article_factory: ArticleFactory,
) -> None:
    """
    Removes duplicate news before generating the digest.
    """
    article = article_factory()
    mock_provider = MagicMock()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch(
            "app.main.remove_duplicates",
            return_value=[article],
        ) as mock_remove,
        patch("app.main.create_digest", return_value="Digest"),
        patch(
            "app.main.ProviderFactory.get_provider",
            return_value=mock_provider,
        ),
        patch(
            "app.main.summarize_news",
            return_value="Summary",
        ),
        patch("app.main.split_message", return_value=[]),
        patch("app.main.send_message"),
    ):
        main()

    mock_remove.assert_called_once_with([article])


def test_main_calls_create_digest(
    article_factory: ArticleFactory,
) -> None:
    """
    Creates the Telegram digest.
    """
    article = article_factory()
    mock_provider = MagicMock()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch(
            "app.main.create_digest",
            return_value="Digest",
        ) as mock_digest,
        patch(
            "app.main.ProviderFactory.get_provider",
            return_value=mock_provider,
        ),
        patch(
            "app.main.summarize_news",
            return_value="Summary",
        ),
        patch("app.main.split_message", return_value=[]),
        patch("app.main.send_message"),
    ):
        main()

    mock_digest.assert_called_once_with([article])


def test_main_calls_summarizer(
    article_factory: ArticleFactory,
) -> None:
    """
    Generates the AI summary.
    """
    article = article_factory()
    mock_provider = MagicMock()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.create_digest", return_value="Digest"),
        patch(
            "app.main.ProviderFactory.get_provider",
            return_value=mock_provider,
        ),
        patch(
            "app.main.summarize_news",
            return_value="Summary",
        ) as mock_summary,
        patch("app.main.split_message", return_value=[]),
        patch("app.main.send_message"),
    ):
        main()

    mock_summary.assert_called_once_with(
        [article],
        mock_provider,
    )


def test_main_sends_all_messages(
    article_factory: ArticleFactory,
) -> None:
    """
    Sends the summary followed by all digest parts.
    """
    article = article_factory()
    mock_provider = MagicMock()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.create_digest", return_value="Digest"),
        patch(
            "app.main.ProviderFactory.get_provider",
            return_value=mock_provider,
        ),
        patch(
            "app.main.summarize_news",
            return_value="Summary",
        ),
        patch(
            "app.main.split_message",
            return_value=[
                "Part 1",
                "Part 2",
            ],
        ),
        patch("app.main.send_message") as mock_send,
    ):
        main()

    mock_send.assert_has_calls(
        [
            call("Summary"),
            call("Part 1"),
            call("Part 2"),
        ]
    )


def test_main_handles_unexpected_exception() -> None:
    """
    Logs unexpected exceptions.
    """
    with (
        patch(
            "app.main.get_latest_news",
            side_effect=RuntimeError("Boom"),
        ),
        patch("app.main.logger.exception") as mock_exception,
    ):
        main()

    mock_exception.assert_called_once_with(
        "An unexpected error occurred during bot execution."
    )
