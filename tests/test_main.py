"""
Unit tests for app.main.
"""

from unittest.mock import patch

from app.main import main
from tests.types import ArticleFactory


def test_main_success(article_factory: ArticleFactory) -> None:
    """
    Executes the complete workflow successfully.
    """
    article = article_factory()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.create_digest", return_value="Digest"),
        patch("app.main.summarize_news", return_value="Summary"),
        patch(
            "app.main.split_message", return_value=["Digest Part 1", "Digest Part 2"]
        ),
        patch("app.main.send_message") as mock_send,
        patch("app.main.logger.info"),
    ):
        main()

    assert mock_send.call_count == 3

    mock_send.assert_any_call("Summary")
    mock_send.assert_any_call("Digest Part 1")
    mock_send.assert_any_call("Digest Part 2")


def test_main_no_news() -> None:
    """
    Stops execution when no news articles are retrieved.
    """
    with (
        patch("app.main.get_latest_news", return_value=[]),
        patch("app.main.remove_duplicates", return_value=[]),
        patch("app.main.logger.warning") as mock_warning,
        patch("app.main.summarize_news") as mock_summary,
        patch("app.main.send_message") as mock_send,
    ):
        main()

    mock_warning.assert_called_once_with(
        "No news articles were retrieved.",
    )

    mock_summary.assert_not_called()
    mock_send.assert_not_called()


def test_main_calls_remove_duplicates(
    article_factory: ArticleFactory,
) -> None:
    """
    Removes duplicate articles before summarization.
    """
    article = article_factory()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]) as mock_remove,
        patch("app.main.create_digest", return_value="Digest"),
        patch("app.main.summarize_news", return_value="Summary"),
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

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.create_digest", return_value="Digest") as mock_digest,
        patch("app.main.summarize_news", return_value="Summary"),
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

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.create_digest", return_value="Digest"),
        patch("app.main.summarize_news", return_value="Summary") as mock_summary,
        patch("app.main.split_message", return_value=[]),
        patch("app.main.send_message"),
    ):
        main()

    mock_summary.assert_called_once_with([article])


def test_main_calls_split_message(
    article_factory: ArticleFactory,
) -> None:
    """
    Splits the digest before sending.
    """
    article = article_factory()

    with (
        patch("app.main.get_latest_news", return_value=[article]),
        patch("app.main.remove_duplicates", return_value=[article]),
        patch("app.main.create_digest", return_value="Digest"),
        patch("app.main.summarize_news", return_value="Summary"),
        patch(
            "app.main.split_message",
            return_value=["Digest"],
        ) as mock_split,
        patch("app.main.send_message"),
    ):
        main()

    mock_split.assert_called_once_with("Digest")


def test_main_logs_unexpected_exception() -> None:
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
        "An unexpected error occurred during bot execution.",
    )
