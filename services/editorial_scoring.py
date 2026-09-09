"""Deterministic editorial ranking for daily briefing candidates.

The scoring layer narrows a broad discovery pool before Gemini is asked to edit the
briefing. It deliberately rewards trustworthy, fresh, high-signal stories that match
this briefing's AI/software/telecom/markets focus and penalises generic content.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import replace
from datetime import UTC, datetime

from common.logger import logger
from common.models import NewsArticle, NewsList
from news.sources import (
    CATEGORY_AI,
    CATEGORY_BUSINESS,
    CATEGORY_PYTHON,
    CATEGORY_TELECOM,
)

_WORD_RE = re.compile(r"[a-z0-9][a-z0-9+./-]*")

_CATEGORY_TERMS: dict[str, tuple[str, ...]] = {
    CATEGORY_AI: (
        "ai",
        "artificial intelligence",
        "llm",
        "large language model",
        "openai",
        "anthropic",
        "claude",
        "gemini",
        "deepmind",
        "mistral",
        "agent",
        "agents",
        "model",
        "inference",
        "training",
        "chip",
        "gpu",
        "data center",
        "datacenter",
    ),
    CATEGORY_PYTHON: (
        "python",
        "cpython",
        "pypi",
        "github",
        "developer",
        "software",
        "programming",
        "framework",
        "library",
        "package",
        "security",
        "vulnerability",
        "supply chain",
        "ide",
        "coding agent",
    ),
    CATEGORY_TELECOM: (
        "telecom",
        "telco",
        "tm forum",
        "bss",
        "oss",
        "charging",
        "billing",
        "crm",
        "customer management",
        "open api",
        "oda",
        "autonomous network",
        "5g",
        "6g",
        "network slicing",
        "spectrum",
        "wireless",
        "satellite",
        "broadband",
        "operator",
        "monetization",
        "monetisation",
    ),
    CATEGORY_BUSINESS: (
        "market",
        "markets",
        "economy",
        "economic",
        "inflation",
        "rates",
        "interest rate",
        "federal reserve",
        "fed",
        "rbi",
        "rupee",
        "nifty",
        "sensex",
        "india",
        "oil",
        "brent",
        "earnings",
        "ipo",
        "acquisition",
        "merger",
    ),
}

_HIGH_SIGNAL_TERMS: tuple[str, ...] = (
    "launch",
    "released",
    "release",
    "acquire",
    "acquisition",
    "merger",
    "ipo",
    "billion",
    "trillion",
    "record",
    "regulator",
    "regulation",
    "ban",
    "lawsuit",
    "security",
    "breach",
    "vulnerability",
    "outage",
    "interest rate",
    "rate cut",
    "rate hike",
    "inflation",
    "jobs",
    "oil",
    "brent",
    "funding",
    "investment",
    "partnership",
    "deal",
    "chip",
    "data center",
    "datacenter",
)

_USER_RELEVANCE_TERMS: tuple[str, ...] = (
    "agent",
    "coding",
    "developer",
    "python",
    "enterprise ai",
    "tm forum",
    "bss",
    "oss",
    "crm",
    "charging",
    "monetization",
    "monetisation",
    "open api",
    "oda",
    "autonomous network",
    "india",
    "rbi",
    "rupee",
    "nifty",
    "sensex",
    "oil",
    "brent",
)

_SPAM_TERMS: tuple[str, ...] = (
    "livestream",
    "live stream",
    "free tv",
    "watch live",
    "tv channel",
    "live updates",
)

_GENERIC_TERMS: tuple[str, ...] = (
    "opinion",
    "podcast",
    "sponsored",
    "weekly roundup",
    "weekly round-up",
    "what you need to know",
    "how to",
    "explainer",
)

_PUBLISHER_BONUSES: tuple[tuple[str, float], ...] = (
    ("reuters", 12.0),
    ("tm forum", 10.0),
    ("python", 9.0),
    ("github", 8.0),
    ("openai", 8.0),
    ("anthropic", 8.0),
    ("google", 7.0),
    ("mit technology review", 7.0),
    ("techcrunch", 6.0),
    ("ars technica", 6.0),
    ("light reading", 6.0),
    ("mobile world live", 6.0),
    ("rcr wireless", 5.0),
    ("cnbc", 5.0),
    ("moneycontrol", 5.0),
)

_QUALITY_SCORES = {
    "primary": 30.0,
    "established": 25.0,
    "discovery": 12.0,
}

# Verification measures confidence, not editorial importance. Keep this deliberately
# small so a verified routine post cannot outrank a major unresolved Reuters story.
_VERIFICATION_SCORES = {
    "verified": 3.0,
    "partial": 1.0,
    "not_checked": 0.0,
    "unresolved": 0.0,
    "failed": -8.0,
}

_CATEGORY_ORDER = (
    CATEGORY_AI,
    CATEGORY_PYTHON,
    CATEGORY_TELECOM,
    CATEGORY_BUSINESS,
)


def _text(article: NewsArticle) -> str:
    return " ".join(
        part
        for part in (
            article.title,
            article.summary,
            article.publisher,
            article.source,
            article.content_excerpt,
        )
        if part
    ).casefold()


def _term_hits(text: str, terms: tuple[str, ...]) -> int:
    return sum(1 for term in terms if term in text)


def _freshness_score(article: NewsArticle, now: datetime) -> float:
    if not article.published_at:
        return 5.0

    try:
        published = datetime.fromisoformat(article.published_at.replace("Z", "+00:00"))
        if published.tzinfo is None:
            published = published.replace(tzinfo=UTC)
        age_hours = max(0.0, (now - published.astimezone(UTC)).total_seconds() / 3600)
    except ValueError:
        return 5.0

    if age_hours <= 18:
        return 30.0
    if age_hours <= 36:
        return 25.0
    if age_hours <= 60:
        return 20.0
    if age_hours <= 96:
        return 14.0
    if age_hours <= 120:
        return 8.0
    return 2.0


def _publisher_bonus(article: NewsArticle) -> float:
    publisher = (article.publisher or article.source).casefold()
    for hint, bonus in _PUBLISHER_BONUSES:
        if hint in publisher:
            return bonus
    return 0.0


def is_category_relevant(article: NewsArticle) -> bool:
    """Return whether an article has enough evidence to belong to its category."""
    text = _text(article)
    if any(term in text for term in _SPAM_TERMS):
        return False

    terms = _CATEGORY_TERMS.get(article.category)
    if not terms:
        return True
    return _term_hits(text, terms) > 0


def score_article(article: NewsArticle, *, now: datetime | None = None) -> float:
    """Return a deterministic editorial significance score for one article."""
    current = now or datetime.now(UTC)
    text = _text(article)

    if not is_category_relevant(article):
        return 0.0

    score = _QUALITY_SCORES.get(article.source_quality, 8.0)
    score += _freshness_score(article, current)
    score += _publisher_bonus(article)

    category_terms = _CATEGORY_TERMS.get(article.category, ())
    score += min(20.0, _term_hits(text, category_terms) * 2.5)
    # Magnitude is driven primarily by the headline. This rewards actual events
    # (launches, deals, regulation, market moves) over broad thought leadership.
    title_text = article.title.casefold()
    score += min(20.0, _term_hits(title_text, _HIGH_SIGNAL_TERMS) * 4.0)
    score += min(12.0, _term_hits(text, _USER_RELEVANCE_TERMS) * 1.5)
    score += _VERIFICATION_SCORES.get(article.verification_status, 0.0)

    if any(term in text for term in _GENERIC_TERMS):
        score -= 12.0

    # A title that says little beyond the source/category is usually weak editorially.
    if len(_WORD_RE.findall(article.title.casefold())) < 5:
        score -= 4.0

    return round(score, 2)


def _publisher_key(article: NewsArticle) -> str:
    return (article.publisher or article.source or "unknown").casefold().strip()


def select_editorial_candidates(
    articles: NewsList,
    *,
    max_per_category: int,
    max_per_publisher: int = 3,
    now: datetime | None = None,
) -> NewsList:
    """Score, diversify and cap candidates per category for the editorial pipeline."""
    if not articles:
        return []

    current = now or datetime.now(UTC)
    relevant = [article for article in articles if is_category_relevant(article)]
    rejected = len(articles) - len(relevant)
    if rejected:
        logger.info(
            "Editorial relevance gate rejected %d of %d candidates.",
            rejected,
            len(articles),
        )

    scored = [
        replace(
            article,
            editorial_score=score_article(article, now=current),
        )
        for article in relevant
    ]

    selected: NewsList = []
    category_counts: dict[str, int] = defaultdict(int)
    publisher_counts: dict[tuple[str, str], int] = defaultdict(int)

    ordered_categories = list(_CATEGORY_ORDER)
    ordered_categories.extend(
        category
        for category in dict.fromkeys(article.category for article in scored)
        if category not in _CATEGORY_ORDER
    )

    for category in ordered_categories:
        candidates = [article for article in scored if article.category == category]
        candidates.sort(key=lambda article: article.editorial_score, reverse=True)

        for article in candidates:
            if category_counts[category] >= max_per_category:
                break
            publisher_key = (category, _publisher_key(article))
            if publisher_counts[publisher_key] >= max_per_publisher:
                continue

            selected.append(article)
            category_counts[category] += 1
            publisher_counts[publisher_key] += 1

    logger.info(
        "Editorial selection kept %d of %d candidates (max %d per category).",
        len(selected),
        len(articles),
        max_per_category,
    )
    for category in ordered_categories:
        category_items = [
            article for article in selected if article.category == category
        ]
        if not category_items:
            continue
        summary = " | ".join(
            f"{article.editorial_score:.1f} "
            f"{article.publisher or article.source}: {article.title[:90]}"
            for article in category_items
        )
        logger.info("Editorial shortlist [%s]: %s", category, summary)

    return selected
