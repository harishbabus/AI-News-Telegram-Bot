from unittest.mock import Mock

from common.models import NewsArticle
from services.article_verifier import verify_article, verify_articles


def _article(**overrides) -> NewsArticle:
    values = {
        "source": "OpenAI",
        "title": "OpenAI launches a new model for developers",
        "summary": "A new model was announced.",
        "link": "https://example.com/article",
        "category": "AI & LLMs",
        "publisher": "OpenAI",
        "source_quality": "primary",
        "published_at": "2026-09-04T08:00:00+00:00",
    }
    values.update(overrides)
    return NewsArticle(**values)


def test_verify_article_marks_matching_html_verified() -> None:
    response = Mock()
    response.url = "https://openai.com/article"
    response.headers = {"content-type": "text/html; charset=utf-8"}
    response.text = """
    <html><head>
      <meta property="og:title" content="OpenAI launches a new model for developers">
      <meta property="og:description" content="OpenAI announced a new model for developers and enterprise workloads.">
      <meta property="article:published_time" content="2026-09-04T08:00:00Z">
    </head><body>
      <article><p>This article contains substantial readable content about the new model,
      its developer capabilities, deployment considerations, safety controls, enterprise use,
      API availability, performance, and operational guidance for teams adopting the release.</p>
      <p>Additional details explain the product announcement and its practical implications for
      software engineers and technology leaders evaluating the new system.</p></article>
    </body></html>
    """
    response.raise_for_status.return_value = None
    session = Mock()
    session.get.return_value = response

    verified = verify_article(_article(), session=session)

    assert verified.verification_status == "verified"
    assert verified.verified_url == "https://openai.com/article"
    assert verified.content_date == "2026-09-04T08:00:00Z"
    assert "substantial readable content" in verified.content_excerpt


def test_verify_article_rejects_unresolved_google_news_page() -> None:
    response = Mock()
    response.url = "https://news.google.com/rss/articles/abc"
    response.headers = {"content-type": "text/html"}
    response.text = "<html><body>Google News</body></html>"
    response.raise_for_status.return_value = None
    session = Mock()
    session.get.return_value = response

    verified = verify_article(
        _article(link="https://news.google.com/x"), session=session
    )

    assert verified.verification_status == "unresolved"


def test_verify_articles_balances_categories(monkeypatch) -> None:
    articles = [_article(title=f"AI story {i}") for i in range(5)] + [
        _article(
            title=f"Market story {i}",
            category="Business & Markets",
            source="Reuters",
            publisher="Reuters",
            source_quality="established",
        )
        for i in range(5)
    ]

    called: list[str] = []

    def fake_verify(article, **_kwargs):
        called.append(article.title)
        article.verification_status = "verified"
        return article

    monkeypatch.setattr("services.article_verifier.verify_article", fake_verify)

    result = verify_articles(articles, max_per_category=2)

    assert len(called) == 4
    assert len(result) == 10
