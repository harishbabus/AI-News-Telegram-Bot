from dataclasses import dataclass


@dataclass
class NewsArticle:
    """
    Represents a single AI news article.
    """

    source: str
    title: str
    summary: str
    link: str


NewsList = list[NewsArticle]
