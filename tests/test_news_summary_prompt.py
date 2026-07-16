"""
Unit tests for prompts.news_summary_prompt.
"""

from prompts.news_summary_prompt import build_news_prompt


# ============================================================================
# build_news_prompt()
# ============================================================================

def test_build_news_prompt_empty_news():
    """
    Builds a valid prompt even when no news articles are supplied.
    """
    # Arrange
    news = []

    # Act
    prompt = build_news_prompt(news)

    # Assert
    assert "You are an experienced AI News Editor" in prompt
    assert "## Articles" in prompt


def test_build_news_prompt_single_article(article_factory):
    """
    Includes all fields of a single news article.
    """
    # Arrange
    article = article_factory(
        source="OpenAI",
        title="GPT-5 Released",
        summary="OpenAI announced GPT-5.",
        link="https://example.com",
    )

    # Act
    prompt = build_news_prompt([article])

    # Assert
    assert "Article 1" in prompt
    assert "OpenAI" in prompt
    assert "GPT-5 Released" in prompt
    assert "OpenAI announced GPT-5." in prompt
    assert "https://example.com" in prompt


def test_build_news_prompt_multiple_articles(article_factory):
    """
    Includes all supplied articles.
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
    prompt = build_news_prompt([article1, article2])

    # Assert
    assert "Article 1" in prompt
    assert "Article 2" in prompt

    assert "GPT-5 Released" in prompt
    assert "Gemini 3 Released" in prompt


def test_build_news_prompt_contains_editor_instructions(article_factory):
    """
    Includes the LLM instructions.
    """
    # Arrange
    article = article_factory()

    # Act
    prompt = build_news_prompt([article])

    # Assert
    assert "Read every article carefully." in prompt
    assert "Remove duplicate stories." in prompt
    assert "Merge articles covering the same event." in prompt
    assert "Do not invent or assume facts." in prompt


def test_build_news_prompt_contains_required_output_format(article_factory):
    """
    Includes the required output sections.
    """
    # Arrange
    article = article_factory()

    # Act
    prompt = build_news_prompt([article])

    # Assert
    assert "🧠 AI Daily Brief" in prompt
    assert "🔥 Top Story" in prompt
    assert "🛠 New AI Tools" in prompt
    assert "📄 Research Highlights" in prompt
    assert "💡 Why Today's News Matters" in prompt


def test_build_news_prompt_contains_article_separator(article_factory):
    """
    Separates articles using the expected divider.
    """
    # Arrange
    article = article_factory()

    # Act
    prompt = build_news_prompt([article])

    # Assert
    assert "==============================" in prompt


def test_build_news_prompt_preserves_article_order(article_factory):
    """
    Preserves the order of supplied articles.
    """
    # Arrange
    article1 = article_factory(title="Article One")

    article2 = article_factory(title="Article Two")

    # Act
    prompt = build_news_prompt([article1, article2])

    # Assert
    assert prompt.index("Article One") < prompt.index("Article Two")


def test_build_news_prompt_includes_article_links(article_factory):
    """
    Includes article links in the generated prompt.
    """
    # Arrange
    article = article_factory(
        link="https://openai.com/news",
    )

    # Act
    prompt = build_news_prompt([article])

    # Assert
    assert "https://openai.com/news" in prompt