from news import get_latest_news
from utils import remove_duplicates
from formatter import create_digest, split_message
from telegram_bot import send_message

news = get_latest_news()
news = remove_duplicates(news)

message = create_digest(news)

parts = split_message(message)

for part in parts:
    send_message(part)