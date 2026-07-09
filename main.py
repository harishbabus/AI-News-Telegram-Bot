from news import get_latest_news
from utils import remove_duplicates
from formatter import create_digest, split_message
from telegram_bot import send_message
from summarizer import summarize_news

news = get_latest_news()
news = remove_duplicates(news)

# Existing digest (keep this for now)
message = create_digest(news)

# New AI summary (currently a placeholder)
summary = summarize_news(news)

# Send AI summary first
send_message(summary)

# Then send the full news digest
parts = split_message(message)

for part in parts:
    send_message(part)