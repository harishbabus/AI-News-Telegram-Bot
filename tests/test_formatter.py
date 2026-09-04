"""Unit tests for news.formatter."""

from common.constants import MAX_TELEGRAM_MESSAGE_LENGTH
from common.models import NewsList
from news.formatter import create_digest, split_message
from tests.types import ArticleFactory


def test_split_message_empty_string() -> None:
    assert split_message("") == [""]


def test_split_message_short_message() -> None:
    message = "Hello World"
    assert split_message(message) == [message]


def test_split_message_exact_limit() -> None:
    message = "A" * MAX_TELEGRAM_MESSAGE_LENGTH
    assert split_message(message) == [message]


def test_split_message_exceeds_limit() -> None:
    message = "A" * (MAX_TELEGRAM_MESSAGE_LENGTH + 100)
    result = split_message(message)
    assert len(result) == 2
    assert len(result[0]) == MAX_TELEGRAM_MESSAGE_LENGTH
    assert len(result[1]) == 100


def test_split_message_prefers_paragraph_boundary() -> None:
    first = "A" * (MAX_TELEGRAM_MESSAGE_LENGTH - 20)
    second = "B" * 30
    result = split_message(f"{first}\n\n{second}")
    assert result == [first, second]


def test_create_digest_empty_news() -> None:
    news: NewsList = []
    digest = create_digest(news)
    assert digest == "🤖 <b>AI Daily Digest</b>"


def test_create_digest_single_article(article_factory: ArticleFactory) -> None:
    article = article_factory(
        title="GPT-5 Released",
        summary="A new model was announced.",
        link="https://example.com",
    )
    digest = create_digest([article])
    assert "<b>GPT-5 Released</b>" in digest
    assert "A new model was announced." in digest
    assert '<a href="https://example.com">Read article →</a>' in digest


def test_create_digest_multiple_articles(article_factory: ArticleFactory) -> None:
    article1 = article_factory(title="GPT-5 Released")
    article2 = article_factory(title="Gemini 3 Released")
    digest = create_digest([article1, article2])
    assert "GPT-5 Released" in digest
    assert "Gemini 3 Released" in digest


def test_create_digest_escapes_html(article_factory: ArticleFactory) -> None:
    article = article_factory(title="Model <Alpha>", summary="A & B")
    digest = create_digest([article])
    assert "Model &lt;Alpha&gt;" in digest
    assert "A &amp; B" in digest


def test_format_telegram_editorial_digest_bolds_only_section_headings() -> None:
    from news.formatter import format_telegram_editorial_digest

    summary = """🔥 TOP STORIES
• OpenAI & Google announced updates.

🎯 WHY TODAY'S NEWS MATTERS
Engineers should watch <agent> adoption."""
    result = format_telegram_editorial_digest(summary)

    assert "<b>🔥 TOP STORIES</b>" in result
    assert "OpenAI &amp; Google" in result
    assert "&lt;agent&gt;" in result
    assert "<b>🎯 WHY TODAY&#x27;S NEWS MATTERS</b>" in result


def test_format_telegram_editorial_digest_fills_empty_sections() -> None:
    from news.formatter import format_telegram_editorial_digest

    summary = """🔥 TOP STORIES

🛠️ NEW AI TOOLS

🔬 RESEARCH HIGHLIGHTS

🎯 WHY TODAY'S NEWS MATTERS
A useful closing synthesis."""

    result = format_telegram_editorial_digest(summary)
    assert "No sufficiently verified top story today." in result
    assert "No major tool release today." in result
    assert "No major research highlight today." in result
    assert "A useful closing synthesis." in result
