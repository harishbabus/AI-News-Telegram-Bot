import os
from dotenv import load_dotenv

# Load .env only if it exists (for local development)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY=  os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError(
        "BOT_TOKEN and CHAT_ID must be set either in .env or as environment variables."
    )