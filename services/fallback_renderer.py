"""Deterministic non-LLM fallbacks for scheduled delivery continuity."""

from collections import defaultdict

from common.models import NewsArticle, NewsList

_TOOL_TERMS = (
    "tool",
    "app",
    "agent",
    "copilot",
    "workspace",
    "api",
    "sdk",
    "platform",
    "launch",
    "release",
)
_RESEARCH_TERMS = (
    "research",
    "paper",
    "study",
    "benchmark",
    "model",
    "deepmind",
    "lab",
    "forecast",
)


def _clean(text: str, limit: int = 360) -> str:
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


def _quality_rank(article: NewsArticle) -> tuple[float, int, int]:
    verification = {
        "verified": 4,
        "partial": 3,
        "not_checked": 2,
        "unresolved": 1,
        "failed": 0,
    }.get(article.verification_status, 1)
    source = {"primary": 3, "established": 2, "discovery": 1}.get(
        article.source_quality, 1
    )
    return article.editorial_score, verification, source


def _ranked(news: NewsList) -> NewsList:
    return sorted(news, key=_quality_rank, reverse=True)


def _bullet(article: NewsArticle) -> str:
    summary = _clean(article.content_excerpt or article.summary, 260)
    if summary:
        return f"• {article.title} — {summary}"
    return f"• {article.title}"


def build_telegram_fallback(news: NewsList) -> str:
    """Build a useful editorial-shaped Telegram digest without an LLM."""
    ranked = _ranked(news)
    top = ranked[:3]

    tools = [
        article
        for article in ranked
        if any(term in article.title.casefold() for term in _TOOL_TERMS)
        and article not in top
    ][:2]
    research = [
        article
        for article in ranked
        if any(term in article.title.casefold() for term in _RESEARCH_TERMS)
        and article not in top
        and article not in tools
    ][:2]

    lines = ["🔥 TOP STORIES"]
    lines.extend(_bullet(article) for article in top)
    if not top:
        lines.append("No sufficiently verified top story today.")

    lines.extend(["", "🛠️ NEW AI TOOLS"])
    lines.extend(_bullet(article) for article in tools)
    if not tools:
        lines.append("No major tool release today.")

    lines.extend(["", "🔬 RESEARCH HIGHLIGHTS"])
    lines.extend(_bullet(article) for article in research)
    if not research:
        lines.append("No major research highlight today.")

    lines.extend(
        [
            "",
            "🎯 WHY TODAY'S NEWS MATTERS",
            (
                "Gemini was temporarily unavailable, so this edition uses the "
                "highest-quality collected stories without AI-generated synthesis."
            ),
        ]
    )
    return "\n".join(lines)


def build_daily_briefing_fallback(news: NewsList) -> str:
    """Build the established email text contract without an LLM."""
    grouped: dict[str, list[NewsArticle]] = defaultdict(list)
    for article in _ranked(news):
        grouped[article.category].append(article)

    sections = (
        ("🤖 AI & LLMs", "AI & LLMs"),
        ("🐍 Python & Software Development", "Python & Software Development"),
        ("📡 Telecom / BSS", "Telecom / BSS"),
        ("💹 Business & Markets", "Business & Markets"),
    )

    lines = [
        "📰 Daily Briefing",
        "",
        "Today’s signal",
        (
            "Gemini is temporarily unavailable. This fallback edition presents the "
            "highest-quality fresh stories collected today without "
            "AI-generated synthesis."
        ),
    ]

    takeaways: list[str] = []
    for heading, category in sections:
        lines.extend(["", heading, ""])
        stories = grouped.get(category, [])[:2]
        if not stories:
            lines.append("No major headline today.")
            continue

        for index, article in enumerate(stories, start=1):
            description = _clean(article.content_excerpt or article.summary, 420)
            source_name = article.publisher or article.source or "Source"
            link = article.verified_url or article.link
            lines.append(f"{index}. {article.title}")
            if description:
                lines.append(description)
            lines.append(
                "Why it matters: Selected from today's fresh feed based on source and "
                "verification quality; AI interpretation is unavailable for this run."
            )
            lines.append(f"Source name: {source_name}")
            if link:
                lines.append(f"Source: {link}")
            lines.append("")
            if len(takeaways) < 3:
                takeaways.append(article.title)

    lines.extend(["🎯 What matters most today", ""])
    if takeaways:
        lines.extend(f"• {title}" for title in takeaways[:3])
    else:
        lines.append(
            "• No sufficiently strong signal was available from today's feeds."
        )

    return "\n".join(lines).strip()
