from telegram_bot import send_message
from news import get_latest_news
from formatter import split_message
from utils import remove_duplicates

# Get the latest news
news = get_latest_news()

# Remove duplicates
news = remove_duplicates(news)

print(f"Found {len(news)} unique articles.")

# Build the Telegram message
message = "🤖 AI Daily Digest\n\n"

for item in news:
    message += (
        f"📰 {item['source']}\n"
        f"{item['title']}\n"
        f"{item['link']}\n\n"
    )

# Split into chunks if needed
parts = split_message(message)

# Send each chunk
for part in parts:
    send_message(part)

print("✅ News sent successfully!")