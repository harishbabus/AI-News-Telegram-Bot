import logging

from news import get_latest_news
from utils import remove_duplicates
from formatter import create_digest, split_message
from telegram_bot import send_message
from summarizer import summarize_news

logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Bot execution started")

news = get_latest_news()
news = remove_duplicates(news)

summary = summarize_news(news)
send_message(summary)

message = create_digest(news)

parts = split_message(message)

for part in parts:
    send_message(part)

logging.info("Bot execution completed")