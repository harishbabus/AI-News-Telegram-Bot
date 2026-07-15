from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class NewsArticle:
    """
    Represents a single AI news article.
    """
    source: str
    title: str
    summary: str
    link: str

NewsList: TypeAlias = list[NewsArticle]