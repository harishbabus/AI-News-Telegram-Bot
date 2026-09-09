import calendar
import html
import re
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from time import struct_time

import feedparser

from common.logger import logger
from common.models import NewsArticle, NewsList
from news.sources import (
    AI_RSS_SOURCES,
    CATEGORY_MAX_AGE_HOURS,
    RSS_SOURCES,
    SOURCE_CATEGORIES,
    SOURCE_QUALITY,
    TRUSTED_PUBLISHER_HINTS,
)

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def _clean_text(value: str) -> str:
    """Convert RSS HTML/snippets into clean plain text."""
    if not value:
        return ""

    text = html.unescape(value)
    text = _TAG_RE.sub(" ", text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def _entry_published(entry: object) -> str:
    for field in ("published", "updated"):
        value = getattr(entry, field, "")
        if value:
            return _clean_text(str(value))
    return ""


def _entry_datetime(entry: object) -> datetime | None:
    """Return a UTC publication timestamp when the feed provides one."""
    for field in ("published_parsed", "updated_parsed"):
        value = getattr(entry, field, None)
        if isinstance(value, struct_time):
            return datetime.fromtimestamp(calendar.timegm(value), tz=UTC)

    # A few feeds expose the textual RFC date but omit feedparser's parsed field.
    for field in ("published", "updated"):
        value = getattr(entry, field, "")
        if not value:
            continue
        try:
            parsed = parsedate_to_datetime(str(value))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=UTC)
            return parsed.astimezone(UTC)
        except (TypeError, ValueError, OverflowError):
            continue

    return None


def _entry_publisher(entry: object, fallback: str) -> str:
    """Extract the original publisher from aggregator feeds when available."""
    source = getattr(entry, "source", None)
    title = getattr(source, "title", "") if source is not None else ""
    cleaned = _clean_text(str(title)) if title else ""
    return cleaned or fallback


def _is_fresh(
    published_at: datetime | None,
    category: str,
    now: datetime,
) -> bool:
    """Reject stale or implausibly future-dated stories."""
    if published_at is None:
        # Some official feeds omit a structured timestamp. Keep these candidates,
        # but the prompt is told that their date was not verified.
        return True

    if published_at > now + timedelta(hours=6):
        return False

    max_age = timedelta(hours=CATEGORY_MAX_AGE_HOURS.get(category, 72))
    return now - published_at <= max_age


def _quality_for_entry(source_name: str, publisher: str) -> str:
    """Upgrade trusted publishers found through an aggregator to established."""
    configured = SOURCE_QUALITY.get(source_name, "discovery")
    if configured != "discovery":
        return configured

    publisher_key = publisher.casefold()
    if any(hint in publisher_key for hint in TRUSTED_PUBLISHER_HINTS):
        return "established"
    return configured


def _fetch_news(
    sources: dict[str, str],
    limit_per_source: int,
    *,
    now: datetime | None = None,
) -> NewsList:
    """Fetch fresh articles from a supplied source mapping."""
    news: NewsList = []
    current_time = now or datetime.now(UTC)

    for source_name, feed_url in sources.items():
        try:
            logger.info("Fetching RSS feed: %s", source_name)
            feed = feedparser.parse(feed_url)
            entries = list(feed.entries)

            if feed.bozo:
                if not entries:
                    logger.warning(
                        "Skipping invalid RSS feed '%s': %s",
                        source_name,
                        feed.bozo_exception,
                    )
                    continue

                logger.warning(
                    "RSS feed '%s' reported a parser warning but returned %d "
                    "entries; continuing: %s",
                    source_name,
                    len(entries),
                    feed.bozo_exception,
                )

            logger.info("Found %d articles from %s", len(entries), source_name)
            if not entries:
                continue

            category = SOURCE_CATEGORIES.get(source_name, "Other")

            # Prefer newest dated entries before applying the per-source cap.
            entries.sort(
                key=lambda item: _entry_datetime(item)
                or datetime.min.replace(tzinfo=UTC),
                reverse=True,
            )

            accepted = 0
            stale = 0
            for entry in entries:
                published_at = _entry_datetime(entry)
                if not _is_fresh(published_at, category, current_time):
                    stale += 1
                    continue

                title = _clean_text(str(getattr(entry, "title", "")))
                summary = _clean_text(str(getattr(entry, "summary", "")))
                link = str(getattr(entry, "link", "")).strip()

                if not title or not link:
                    continue

                publisher = _entry_publisher(entry, source_name)
                quality = _quality_for_entry(source_name, publisher)

                news.append(
                    NewsArticle(
                        source=source_name,
                        title=title,
                        summary=summary,
                        link=link,
                        category=category,
                        published=_entry_published(entry),
                        publisher=publisher,
                        source_quality=quality,
                        published_at=(published_at.isoformat() if published_at else ""),
                    )
                )
                accepted += 1
                if accepted >= limit_per_source:
                    break

            if stale:
                logger.info(
                    "Filtered %d stale articles from %s.",
                    stale,
                    source_name,
                )

        except Exception:
            logger.exception("Failed to fetch RSS feed: %s", source_name)

    return news


def get_latest_ai_news(
    limit_per_source: int = 6,
) -> NewsList:
    """Fetch the curated AI-only candidates used for Telegram."""
    return _fetch_news(AI_RSS_SOURCES, limit_per_source)


def get_latest_news(
    limit_per_source: int = 8,
) -> NewsList:
    """Fetch the curated broader candidates used for the email briefing."""
    return _fetch_news(RSS_SOURCES, limit_per_source)
