from typing import Any


def remove_duplicates(news: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Removes duplicate news articles based on their normalized title.

    Titles are converted to lowercase and stripped of leading/trailing
    whitespace before comparison.

    Args:
        news: List of news article dictionaries.

    Returns:
        A list containing unique news articles while preserving their
        original order.
    """
    
    seen: set[str] = set()
    unique_articles: list[dict[str, Any]] = []

    for article in news:
        title = article.get("title", "").strip().lower()

        if title not in seen:
            seen.add(title)
            unique_articles.append(article)

    return unique_articles