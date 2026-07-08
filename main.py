from telegram_bot import send_message
from news import get_latest_news

news = get_latest_news()

message = "🤖 AI Daily Digest\n\n"

for item in news:
    message += (
        f"📰 {item['source']}\n"
        f"{item['title']}\n"
        f"{item['link']}\n\n"
    )

send_message(message)