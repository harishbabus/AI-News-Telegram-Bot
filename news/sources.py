"""
RSS feed sources used by the AI News Telegram Bot.

The keys represent the display names of the news sources, and the
values are the corresponding RSS feed URLs.
"""

RSS_SOURCES: dict[str, str] = {
    "Anthropic": "https://www.anthropic.com/news/rss.xml",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "MarkTechPost": "https://www.marktechpost.com/feed/",  # AI news blog
    "OpenAI": "https://openai.com/news/rss.xml",
}
