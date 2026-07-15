from common.models import NewsList

# Telegram message limit (slightly below the official limit)
MAX_MESSAGE_LENGTH = 4000


def split_message(message: str) -> list[str]:
    """
    Splits a message into chunks that do not exceed the maximum
    Telegram message length.

    Args:
        message: The message to split.

    Returns:
        A list of message parts.
    """
    parts: list[str] = []

    while len(message) > MAX_MESSAGE_LENGTH:
        parts.append(message[:MAX_MESSAGE_LENGTH])
        message = message[MAX_MESSAGE_LENGTH:]

    parts.append(message)

    return parts


def create_digest(news: NewsList) -> str:
    """
    Creates a formatted AI news digest.

    Args:
        news: List of NewsArticle instances.

    Returns:
        A formatted message ready to be sent to Telegram.
    """
    lines = [
        "🤖 AI Daily Digest",
        "=" * 25,
        "",
    ]
    
    for article in news:
        lines.extend(
            [
                f"📰 {article.source}",
                f"**{article.title}**",
                article.summary,
                article.link,
                "-" * 40,
            ]
        )

    return "\n".join(lines)