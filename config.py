import os
from dotenv import load_dotenv

# Load .env only if it exists (for local development)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError(
        "BOT_TOKEN and CHAT_ID must be set either in .env or as environment variables."
    )