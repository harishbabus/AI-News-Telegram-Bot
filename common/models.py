from dataclasses import dataclass


@dataclass
class NewsArticle:
    """Represents a single news article used by the daily briefing."""

    source: str
    title: str
    summary: str
    link: str
    category: str = "AI & LLMs"
    published: str = ""
    publisher: str = ""
    source_quality: str = "discovery"
    published_at: str = ""
    verification_status: str = "not_checked"
    verification_reason: str = ""
    verified_url: str = ""
    content_excerpt: str = ""
    content_date: str = ""
    editorial_score: float = 0.0


NewsList = list[NewsArticle]
