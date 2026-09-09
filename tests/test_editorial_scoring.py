from datetime import UTC, datetime

from common.models import NewsArticle
from news.sources import CATEGORY_AI, CATEGORY_TELECOM
from services.editorial_scoring import (
    is_category_relevant,
    score_article,
    select_editorial_candidates,
)

NOW = datetime(2026, 9, 9, 6, 0, tzinfo=UTC)


def _article(
    *,
    title: str,
    category: str = CATEGORY_AI,
    publisher: str = "Reuters",
    quality: str = "established",
    published_at: str = "2026-09-09T03:00:00+00:00",
    verification_status: str = "not_checked",
) -> NewsArticle:
    return NewsArticle(
        source="Discovery",
        title=title,
        summary="Relevant executive news development.",
        link="https://example.com/story",
        category=category,
        publisher=publisher,
        source_quality=quality,
        published_at=published_at,
        verification_status=verification_status,
    )


def test_score_rewards_fresh_authoritative_relevant_story() -> None:
    strong = _article(
        title="Reuters: OpenAI signs billion-dollar enterprise AI chip deal",
    )
    weak = _article(
        title="Weekly roundup: how to think about technology",
        publisher="Unknown Blog",
        quality="discovery",
        published_at="2026-09-07T03:00:00+00:00",
    )

    assert score_article(strong, now=NOW) > score_article(weak, now=NOW)


def test_category_gate_rejects_cross_category_and_spam() -> None:
    aircraft = _article(
        title="Pilots considered aborting landing in Miami cargo plane crash",
        category=CATEGORY_TELECOM,
    )
    spam = _article(
        title="LIVESTREAM TV ARS vs CHE live free TV channel",
        category=CATEGORY_TELECOM,
    )
    spectrum = _article(
        title="FCC proposes more spectrum for space-based wireless service",
        category=CATEGORY_TELECOM,
    )

    assert not is_category_relevant(aircraft)
    assert not is_category_relevant(spam)
    assert is_category_relevant(spectrum)


def test_verification_is_confidence_not_large_importance_bonus() -> None:
    unchecked = _article(title="OpenAI launches enterprise AI agent platform")
    verified = _article(
        title="OpenAI launches enterprise AI agent platform",
        verification_status="verified",
    )

    delta = score_article(verified, now=NOW) - score_article(unchecked, now=NOW)
    assert delta == 3.0


def test_major_reuters_development_can_outrank_verified_routine_primary_post() -> None:
    major = _article(
        title="OpenAI signs major partnership for next-generation AI chips",
        publisher="Reuters",
        quality="established",
        verification_status="unresolved",
    )
    routine = _article(
        title="OpenAI explains the work now within reach with AI",
        publisher="OpenAI",
        quality="primary",
        verification_status="verified",
    )

    assert score_article(major, now=NOW) > score_article(routine, now=NOW)


def test_score_rewards_verified_story() -> None:
    unchecked = _article(title="OpenAI launches enterprise AI agent platform")
    verified = _article(
        title="OpenAI launches enterprise AI agent platform",
        verification_status="verified",
    )

    assert score_article(verified, now=NOW) > score_article(unchecked, now=NOW)


def test_selection_caps_category_and_diversifies_publishers() -> None:
    articles = [_article(title=f"Reuters AI deal {index}") for index in range(5)] + [
        _article(
            title="TM Forum launches autonomous network architecture",
            category=CATEGORY_TELECOM,
            publisher="TM Forum",
            quality="primary",
        ),
        _article(
            title="Operator launches major BSS transformation",
            category=CATEGORY_TELECOM,
            publisher="Light Reading",
        ),
    ]

    selected = select_editorial_candidates(
        articles,
        max_per_category=2,
        max_per_publisher=1,
        now=NOW,
    )

    ai = [article for article in selected if article.category == CATEGORY_AI]
    telecom = [article for article in selected if article.category == CATEGORY_TELECOM]

    assert len(ai) == 1
    assert len(telecom) == 2
    assert all(article.editorial_score > 0 for article in selected)
