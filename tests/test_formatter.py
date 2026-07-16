"""
Unit tests for news.formatter.
"""

from common.constants import MAX_TELEGRAM_MESSAGE_LENGTH
from common.models import NewsList
from news.formatter import create_digest, split_message
from tests.types import ArticleFactory

# ============================================================================
# split_message()
# ============================================================================


def test_split_message_empty_string() -> None:
    """
    Returns a single empty message when the input is empty.
    """
    message = ""

    result = split_message(message)

    assert result == [""]


def test_split_message_short_message() -> None:
    """
    Does not split messages shorter than the Telegram limit.
    """
    message = "Hello World"

    result = split_message(message)

    assert result == [message]


def test_split_message_exact_limit() -> None:
    """
    Does not split a message that is exactly the Telegram limit.
    """
    message = "A" * MAX_TELEGRAM_MESSAGE_LENGTH

    result = split_message(message)

    assert result == [message]


def test_split_message_exceeds_limit() -> None:
    """
    Splits a message into multiple parts when it exceeds the limit.
    """
    message = "A" * (MAX_TELEGRAM_MESSAGE_LENGTH + 100)

    result = split_message(message)

    assert len(result) == 2
    assert len(result[0]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[1]) == 100


def test_split_message_large_message() -> None:
    """
    Splits a very large message into multiple parts.
    """
    message = "A" * (MAX_TELEGRAM_MESSAGE_LENGTH * 3 + 250)

    result = split_message(message)

    assert len(result) == 4

    assert len(result[0]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[1]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[2]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[3]) == 250


# ============================================================================
# create_digest()
# ============================================================================


def test_create_digest_empty_news() -> None:
    """
    Creates a valid digest even when no news articles are supplied.
    """
    news: NewsList = []

    digest = create_digest(news)

    assert "🤖 AI Daily Digest" in digest
    assert "=" * 25 in digest


def test_create_digest_single_article(
    article_factory: ArticleFactory,
) -> None:
    """
    Includes the article title, summary and link.
    """
    article = article_factory(
        title="GPT-5 Released",
        summary="A new model was announced.",
        link="https://example.com",
    )

    digest = create_digest([article])

    assert "GPT-5 Released" in digest
    assert "A new model was announced." in digest
    assert "https://example.com" in digest


def test_create_digest_multiple_articles(
    article_factory: ArticleFactory,
) -> None:
    """
    Includes every supplied article.
    """
    article1 = article_factory(
        title="GPT-5 Released",
    )

    article2 = article_factory(
        title="Gemini 3 Released",
    )

    digest = create_digest([article1, article2])

    assert "GPT-5 Released" in digest
    assert "Gemini 3 Released" in digest


def test_create_digest_contains_header(
    article_factory: ArticleFactory,
) -> None:
    """
    Always starts with the AI Daily Digest header.
    """
    article = article_factory()

    digest = create_digest([article])

    assert digest.startswith("🤖 AI Daily Digest")


def test_create_digest_contains_separator(
    article_factory: ArticleFactory,
) -> None:
    """
    Includes the separator line below the header.
    """
    article = article_factory()

    digest = create_digest([article])

    assert "=" * 25 in digest
