"""Lightweight article-page verification for briefing candidates.

The verifier intentionally uses deterministic HTTP/HTML checks rather than an LLM.
It enriches a limited set of candidates with article-page evidence before Gemini
selects and synthesises the final Telegram/email outputs.
"""

from __future__ import annotations

import html
import re
from dataclasses import replace
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

from common.logger import logger
from common.models import NewsArticle, NewsList

DEFAULT_VERIFY_TIMEOUT = 10
DEFAULT_MAX_VERIFY_PER_CATEGORY = 4
MAX_CONTENT_EXCERPT_CHARS = 2200

_SPACE_RE = re.compile(r"\s+")
_WORD_RE = re.compile(r"[a-z0-9]{3,}")


class _ArticleHTMLParser(HTMLParser):
    """Extract useful metadata and visible text from an article page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self._skip_depth = 0
        self.meta: dict[str, str] = {}
        self.text_parts: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.casefold(): (value or "") for key, value in attrs}
        lowered = tag.casefold()

        if lowered == "title":
            self._in_title = True
        if lowered in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1

        if lowered == "a":
            href = attributes.get("href", "").strip()
            if href:
                self.links.append(href)

        if lowered == "meta":
            raw_key = (
                attributes.get("property")
                or attributes.get("name")
                or attributes.get("itemprop")
                or ""
            )
            key = raw_key.casefold()
            content = attributes.get("content", "").strip()
            if key and content:
                self.meta[key] = content

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.casefold()
        if lowered == "title":
            self._in_title = False
        if lowered in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        cleaned = _SPACE_RE.sub(" ", html.unescape(data)).strip()
        if not cleaned:
            return
        if self._in_title:
            self.title = f"{self.title} {cleaned}".strip()
        elif not self._skip_depth and len(cleaned) >= 30:
            self.text_parts.append(cleaned)


def _normalise(value: str | None) -> str:
    return _SPACE_RE.sub(" ", html.unescape(value or "")).strip()


def _title_overlap(feed_title: str, page_title: str) -> float:
    feed_words = set(_WORD_RE.findall(feed_title.casefold()))
    page_words = set(_WORD_RE.findall(page_title.casefold()))
    if not feed_words or not page_words:
        return 0.0
    return len(feed_words & page_words) / len(feed_words)


def _page_title(parser: _ArticleHTMLParser) -> str:
    return _normalise(
        parser.meta.get("og:title") or parser.meta.get("twitter:title") or parser.title
    )


def _page_date(parser: _ArticleHTMLParser) -> str:
    for key in (
        "article:published_time",
        "datepublished",
        "date",
        "pubdate",
        "publish-date",
        "parsely-pub-date",
    ):
        value = parser.meta.get(key, "").strip()
        if value:
            return value
    return ""


def _content_excerpt(parser: _ArticleHTMLParser) -> str:
    description = _normalise(
        parser.meta.get("og:description")
        or parser.meta.get("description")
        or parser.meta.get("twitter:description")
    )
    body = _normalise(" ".join(parser.text_parts))
    combined = _normalise(f"{description} {body}")
    return combined[:MAX_CONTENT_EXCERPT_CHARS]


def _is_google_news_url(url: str) -> bool:
    host = urlparse(url).hostname or ""
    host = host.casefold()
    return host == "news.google.com" or host.endswith(".news.google.com")


_GOOGLE_HOST_SUFFIXES = (
    "google.com",
    "googleusercontent.com",
    "gstatic.com",
    "youtube.com",
)


def _is_external_publisher_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    host = (parsed.hostname or "").casefold()
    return bool(host) and not any(
        host == suffix or host.endswith(f".{suffix}")
        for suffix in _GOOGLE_HOST_SUFFIXES
    )


def _google_news_publisher_candidates(html_text: str, base_url: str) -> list[str]:
    """Extract likely publisher links exposed by a Google News landing page."""
    parser = _ArticleHTMLParser()
    parser.feed(html_text)
    candidates: list[str] = []
    seen: set[str] = set()
    for href in parser.links:
        absolute = urljoin(base_url, html.unescape(href))
        if not _is_external_publisher_url(absolute) or absolute in seen:
            continue
        seen.add(absolute)
        candidates.append(absolute)
    return candidates[:8]


def _fetch_response(
    requester: requests.Session,
    url: str,
    *,
    timeout: int,
    headers: dict[str, str],
) -> requests.Response:
    response = requester.get(
        url,
        timeout=timeout,
        headers=headers,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response


def verify_article(
    article: NewsArticle,
    *,
    timeout: int = DEFAULT_VERIFY_TIMEOUT,
    session: requests.Session | None = None,
) -> NewsArticle:
    """Fetch one article page and return an enriched immutable-style copy."""
    requester = session or requests.Session()
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; AI-News-Briefing/1.0; " "+https://github.com/)"
        )
    }

    try:
        response = _fetch_response(
            requester, article.link, timeout=timeout, headers=headers
        )

        final_url = str(response.url)
        content_type = response.headers.get("content-type", "").casefold()
        if "html" not in content_type:
            return replace(
                article,
                verification_status="failed",
                verification_reason="Article URL did not return HTML content.",
                verified_url=final_url,
            )

        if _is_google_news_url(final_url):
            resolved_response: requests.Response | None = None
            for candidate_url in _google_news_publisher_candidates(
                response.text, final_url
            ):
                try:
                    candidate = _fetch_response(
                        requester,
                        candidate_url,
                        timeout=timeout,
                        headers=headers,
                    )
                except requests.RequestException:
                    continue
                if _is_google_news_url(str(candidate.url)):
                    continue
                candidate_type = candidate.headers.get("content-type", "").casefold()
                if "html" not in candidate_type:
                    continue
                candidate_parser = _ArticleHTMLParser()
                candidate_parser.feed(candidate.text)
                candidate_title = _page_title(candidate_parser)
                if _title_overlap(article.title, candidate_title) >= 0.35:
                    resolved_response = candidate
                    break

            if resolved_response is None:
                return replace(
                    article,
                    verification_status="unresolved",
                    verification_reason=(
                        "Google News discovery link did not expose a matching "
                        "publisher page."
                    ),
                    verified_url=final_url,
                )

            response = resolved_response
            final_url = str(response.url)
            logger.info("Resolved Google News article to publisher: %s", final_url)

        parser = _ArticleHTMLParser()
        parser.feed(response.text)
        page_title = _page_title(parser)
        excerpt = _content_excerpt(parser)
        overlap = _title_overlap(article.title, page_title)

        if len(excerpt) < 250:
            return replace(
                article,
                verification_status="failed",
                verification_reason=(
                    "Publisher page contained too little readable content."
                ),
                verified_url=final_url,
                content_excerpt=excerpt,
                content_date=_page_date(parser),
            )

        if page_title and overlap < 0.35:
            return replace(
                article,
                verification_status="partial",
                verification_reason=(
                    "Publisher page title only partially matched feed title."
                ),
                verified_url=final_url,
                content_excerpt=excerpt,
                content_date=_page_date(parser),
            )

        return replace(
            article,
            verification_status="verified",
            verification_reason="Publisher article page fetched and matched.",
            verified_url=final_url,
            content_excerpt=excerpt,
            content_date=_page_date(parser),
        )

    except requests.RequestException as exc:
        return replace(
            article,
            verification_status="failed",
            verification_reason=(
                "Publisher page could not be fetched: " f"{type(exc).__name__}."
            ),
        )
    except Exception as exc:  # defensive guard for malformed publisher HTML
        logger.warning(
            "Article verification failed unexpectedly for %s: %s",
            article.link,
            exc,
        )
        return replace(
            article,
            verification_status="failed",
            verification_reason="Publisher page could not be verified.",
        )


def _verification_priority(article: NewsArticle) -> tuple[int, float, int]:
    quality_rank = {"primary": 0, "established": 1, "discovery": 2}
    return (
        quality_rank.get(article.source_quality, 3),
        -article.editorial_score,
        0 if article.published_at else 1,
    )


def verify_articles(
    articles: NewsList,
    *,
    max_per_category: int = DEFAULT_MAX_VERIFY_PER_CATEGORY,
    timeout: int = DEFAULT_VERIFY_TIMEOUT,
) -> NewsList:
    """Verify a bounded, category-balanced set while preserving original order."""
    if not articles:
        return []

    selected_ids: set[int] = set()
    categories = list(dict.fromkeys(article.category for article in articles))

    for category in categories:
        candidates = [
            (index, article)
            for index, article in enumerate(articles)
            if article.category == category
        ]
        candidates.sort(key=lambda pair: _verification_priority(pair[1]))
        for index, _article in candidates[:max_per_category]:
            selected_ids.add(index)

    logger.info(
        "Verifying %d of %d shortlisted news candidates.",
        len(selected_ids),
        len(articles),
    )

    session = requests.Session()
    results: NewsList = []
    verified = 0
    partial = 0
    unresolved = 0
    failed = 0

    for index, article in enumerate(articles):
        if index not in selected_ids:
            results.append(article)
            continue

        enriched = verify_article(article, timeout=timeout, session=session)
        results.append(enriched)
        if enriched.verification_status == "verified":
            verified += 1
        elif enriched.verification_status == "partial":
            partial += 1
        elif enriched.verification_status == "unresolved":
            unresolved += 1
        else:
            failed += 1

    logger.info(
        "Article verification complete: %d verified, %d partial, "
        "%d unresolved, %d failed.",
        verified,
        partial,
        unresolved,
        failed,
    )
    return results
