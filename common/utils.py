import re
from difflib import SequenceMatcher

from common.models import NewsList

_NON_ALNUM_RE = re.compile(r"[^a-z0-9 ]+")
_MULTI_SPACE_RE = re.compile(r"\s+")


def _normalise_title(title: str) -> str:
    value = title.casefold().strip()
    value = value.replace("–", "-").replace("—", "-")
    # Publisher suffixes are common in syndicated/Google News titles.
    value = re.sub(r"\s+-\s+[^-]{2,40}$", "", value)
    value = _NON_ALNUM_RE.sub(" ", value)
    return _MULTI_SPACE_RE.sub(" ", value).strip()


def _titles_are_near_duplicates(left: str, right: str) -> bool:
    if left == right:
        return True
    if min(len(left), len(right)) < 20:
        return False
    return SequenceMatcher(None, left, right).ratio() >= 0.88


def remove_duplicates(news: NewsList) -> NewsList:
    """Remove exact and obvious syndicated-title duplicates, preserving order."""
    unique_articles: NewsList = []
    normalised_titles: list[str] = []

    for article in news:
        normalised = _normalise_title(article.title)
        if not normalised:
            continue

        if any(
            _titles_are_near_duplicates(normalised, existing)
            for existing in normalised_titles
        ):
            continue

        normalised_titles.append(normalised)
        unique_articles.append(article)

    return unique_articles
