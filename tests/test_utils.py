"""
Unit tests for common.utils.
"""

from common.utils import remove_duplicates


def test_remove_duplicates_empty_list():
    """
    Returns an empty list when no articles are provided.
    """
    # Arrange
    news = []

    # Act
    result = remove_duplicates(news)

    # Assert
    assert result == []


def test_remove_duplicates_single_article(article_factory):
    """
    Returns the original list when it contains only one article.
    """
    # Arrange
    article = article_factory()

    # Act
    result = remove_duplicates([article])

    # Assert
    assert result == [article]


def test_remove_duplicates_no_duplicates(article_factory):
    """
    Keeps all articles when there are no duplicate titles.
    """
    # Arrange
    article1 = article_factory(
        source="OpenAI",
        title="GPT-5 Released",
    )

    article2 = article_factory(
        source="Google AI",
        title="Gemini 3 Released",
    )

    # Act
    result = remove_duplicates([article1, article2])

    # Assert
    assert result == [article1, article2]


def test_remove_duplicates_duplicate_titles(article_factory):
    """
    Removes duplicate articles that have identical titles.
    """
    # Arrange
    article1 = article_factory(
        source="OpenAI",
        title="GPT-5 Released",
    )

    article2 = article_factory(
        source="Google AI",
        title="GPT-5 Released",
    )

    # Act
    result = remove_duplicates([article1, article2])

    # Assert
    assert result == [article1]


def test_remove_duplicates_case_insensitive(article_factory):
    """
    Treats titles with different letter casing as duplicates.
    """
    # Arrange
    article1 = article_factory(title="GPT-5 Released")

    article2 = article_factory(title="gpt-5 released")

    # Act
    result = remove_duplicates([article1, article2])

    # Assert
    assert result == [article1]


def test_remove_duplicates_ignores_whitespace(article_factory):
    """
    Ignores leading and trailing whitespace when comparing titles.
    """
    # Arrange
    article1 = article_factory(title="GPT-5 Released")

    article2 = article_factory(title="   GPT-5 Released   ")

    # Act
    result = remove_duplicates([article1, article2])

    # Assert
    assert result == [article1]


def test_remove_duplicates_preserves_order(article_factory):
    """
    Preserves the order of the first occurrence of each unique article.
    """
    # Arrange
    article1 = article_factory(title="Article A")

    article2 = article_factory(title="Article B")

    article3 = article_factory(title="Article A")

    # Act
    result = remove_duplicates([article1, article2, article3])

    # Assert
    assert result == [article1, article2]