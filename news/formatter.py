MAX_MESSAGE_LENGTH = 4000

def split_message(message):

    parts = []

    while len(message) > MAX_MESSAGE_LENGTH:
        parts.append(message[:MAX_MESSAGE_LENGTH])
        message = message[MAX_MESSAGE_LENGTH:]

    parts.append(message)

    return parts

def create_digest(news):

    message = "🤖 AI Daily Digest\n"
    message += "=" * 25 + "\n\n"

    for article in news:

        message += f"📰 {article['source']}\n"
        message += f"{article['title']}\n"
        message += f"{article['link']}\n\n"

    return message