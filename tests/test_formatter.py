"""
Unit tests for news.formatter.
"""

from common.constants import MAX_TELEGRAM_MESSAGE_LENGTH
from news.formatter import create_digest, split_message


# ============================================================================
# split_message()
# ============================================================================

def test_split_message_empty_string():
    """
    Returns a single empty message when the input is empty.
    """
    # Arrange
    message = ""

    # Act
    result = split_message(message)

    # Assert
    assert result == [""]


def test_split_message_short_message():
    """
    Does not split messages shorter than the Telegram limit.
    """
    # Arrange
    message = "Hello World"

    # Act
    result = split_message(message)

    # Assert
    assert result == [message]


def test_split_message_exact_limit():
    """
    Does not split a message that is exactly the Telegram limit.
    """
    # Arrange
    message = "A" * MAX_TELEGRAM_MESSAGE_LENGTH

    # Act
    result = split_message(message)

    # Assert
    assert result == [message]


def test_split_message_exceeds_limit():
    """
    Splits a message into multiple parts when it exceeds the limit.
    """
    # Arrange
    message = "A" * (MAX_TELEGRAM_MESSAGE_LENGTH + 100)

    # Act
    result = split_message(message)

    # Assert
    assert len(result) == 2
    assert len(result[0]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[1]) == 100


def test_split_message_large_message():
    """
    Splits a very large message into multiple parts.
    """
    # Arrange
    message = "A" * (MAX_TELEGRAM_MESSAGE_LENGTH * 3 + 250)

    # Act
    result = split_message(message)

    # Assert
    assert len(result) == 4

    assert len(result[0]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[1]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[2]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[3]) == 250


# ============================================================================
# create_digest()
# ============================================================================

def test_create_digest_empty_news():
    """
    Creates a valid digest even when no news articles are supplied.
    """
    # Arrange
    news = []

    # Act
    digest = create_digest(news)

    # Assert
    assert "🤖 AI Daily Digest" in digest
    assert "=" * 25 in digest


def test_create_digest_single_article(article_factory):
    """
    Includes the article title, summary and link.
    """
    # Arrange
    article = article_factory(
        title="GPT-5 Released",
        summary="A new model was announced.",
        link="https://example.com",
    )

    # Act
    digest = create_digest([article])

    # Assert
    assert "GPT-5 Released" in digest
    assert "A new model was announced." in digest
    assert "https://example.com" in digest


def test_create_digest_multiple_articles(article_factory):
    """
    Includes every supplied article.
    """
    # Arrange
    article1 = article_factory(
        title="GPT-5 Released",
    )

    article2 = article_factory(
        title="Gemini 3 Released",
    )

    # Act
    digest = create_digest([article1, article2])

    # Assert
    assert "GPT-5 Released" in digest
    assert "Gemini 3 Released" in digest


def test_create_digest_contains_header(article_factory):
    """
    Always starts with the AI Daily Digest header.
    """
    # Arrange
    article = article_factory()

    # Act
    digest = create_digest([article])

    # Assert
    assert digest.startswith("🤖 AI Daily Digest")


def test_create_digest_contains_separator(article_factory):
    """
    Includes the separator line below the header.
    """
    # Arrange
    article = article_factory()

    # Act
    digest = create_digest([article])

    # Assert
    assert "=" * 25 in digest