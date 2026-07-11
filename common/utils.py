def remove_duplicates(news):

    seen = set()
    unique = []

    for article in news:

        title = article["title"].strip().lower()

        if title not in seen:
            seen.add(title)
            unique.append(article)

    return unique