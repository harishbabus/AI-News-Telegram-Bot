from common.models import NewsList


def remove_duplicates(news: NewsList) -> NewsList:
    """
    Removes duplicate NewsArticle instances based on their normalized title.

    Titles are compared case-insensitively after trimming
    leading and trailing whitespace.

    Args:
        news: List of NewsArticle instances.

    Returns:
        A list containing unique news articles while preserving their
        original order.
    """
    
    seen_titles: set[str] = set()
    unique_articles: NewsList  = []

    for article in news:
        normalized_title = article.title.strip().lower()

        if normalized_title not in seen_titles:
            seen_titles.add(normalized_title)
            unique_articles.append(article)

    return unique_articles