"""Regression tests for v8.2 classification, resolution and email cleanup."""

from unittest.mock import Mock

from common.models import NewsArticle
from news.sources import CATEGORY_AI, CATEGORY_TELECOM
from services.article_verifier import verify_article
from services.briefing_service import generate_daily_briefing
from services.editorial_scoring import (
    is_category_relevant,
    select_editorial_candidates,
)


def _article(**overrides: object) -> NewsArticle:
    values: dict[str, object] = {
        "source": "AI Discovery",
        "title": "OpenAI launches enterprise AI agent platform",
        "summary": "A major AI platform release for developers.",
        "link": "https://example.com/story",
        "category": CATEGORY_AI,
        "publisher": "Reuters",
        "source_quality": "established",
    }
    values.update(overrides)
    return NewsArticle(**values)  # type: ignore[arg-type]


def test_category_gate_does_not_use_feed_name_as_evidence() -> None:
    aircraft = _article(
        source="Telecom Reuters",
        title="Pilots considered aborting landing in Miami cargo plane crash",
        summary="Investigators reviewed the flight crew's landing decision.",
        category=CATEGORY_TELECOM,
    )

    assert not is_category_relevant(aircraft)


def test_uncorroborated_major_discovery_claim_is_filtered() -> None:
    claim = _article(
        title="Google launches Gemini 9 Flash for coding agents",
        publisher="Unknown Discovery Site",
        source_quality="discovery",
    )

    assert select_editorial_candidates([claim], max_per_category=8) == []


def test_google_news_page_can_resolve_to_matching_publisher() -> None:
    google = Mock()
    google.url = "https://news.google.com/rss/articles/abc"
    google.headers = {"content-type": "text/html"}
    google.text = '<a href="https://publisher.example/story">Publisher story</a>'
    google.raise_for_status.return_value = None

    publisher = Mock()
    publisher.url = "https://publisher.example/story"
    publisher.headers = {"content-type": "text/html"}
    publisher.text = """
    <meta property="og:title"
          content="OpenAI launches enterprise AI agent platform">
    <meta property="og:description"
          content="A detailed enterprise AI platform announcement.">
    <article><p>This publisher article contains substantial readable information
    about the enterprise AI agent platform, developer APIs, security, deployment,
    performance, operational guidance, customer adoption and software teams.</p>
    <p>Additional reporting explains the launch, capabilities, availability,
    developer workflows, enterprise usage and practical implications.</p></article>
    """
    publisher.raise_for_status.return_value = None

    session = Mock()
    session.get.side_effect = [google, publisher]
    result = verify_article(
        _article(link="https://news.google.com/rss/articles/abc"),
        session=session,
    )

    assert result.verification_status == "verified"
    assert result.verified_url == "https://publisher.example/story"


def test_email_briefing_removes_markdown_bold_markers() -> None:
    provider = Mock()
    provider.summarize.return_value = (
        "📰 Daily Briefing\n\n🤖 AI & LLMs\n\n"
        "1. **Major AI release**\nA material development."
    )

    result = generate_daily_briefing([_article()], provider)

    assert "**" not in result
    assert "Major AI release" in result
