"""RSS sources and editorial metadata for the news bot."""

from urllib.parse import quote_plus

CATEGORY_AI = "AI & LLMs"
CATEGORY_PYTHON = "Python & Software Development"
CATEGORY_TELECOM = "Telecom / BSS"
CATEGORY_BUSINESS = "Business & Markets"

QUALITY_PRIMARY = "primary"
QUALITY_ESTABLISHED = "established"
QUALITY_DISCOVERY = "discovery"

TRUSTED_PUBLISHER_HINTS: tuple[str, ...] = (
    "reuters",
    "techcrunch",
    "mit technology review",
    "ars technica",
    "infoq",
    "the new stack",
    "tm forum",
    "light reading",
    "mobile world live",
    "rcr wireless",
    "cnbc",
    "moneycontrol",
)


def _google_news_rss(query: str) -> str:
    encoded = quote_plus(query)
    return (
        "https://news.google.com/rss/search?" f"q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"
    )


# Telegram: keep the channel AI-only, but use primary sources wherever possible.
# Anthropic does not currently expose a working RSS endpoint at /news/rss.xml,
# so Google News is used only as a transport for pages from anthropic.com/news.
AI_RSS_SOURCES: dict[str, str] = {
    "Anthropic": _google_news_rss("site:anthropic.com/news Anthropic when:7d"),
    "Google AI": "https://blog.google/technology/ai/rss/",
    "OpenAI": "https://openai.com/news/rss.xml",
    "AI Industry News": _google_news_rss(
        '(AI OR "large language model" OR LLM) '
        '(Reuters OR TechCrunch OR "MIT Technology Review" OR Ars) when:2d'
    ),
}


# Email: broader executive briefing. Google News queries are deliberately narrow
# and supplement, rather than replace, primary/official sources.
BRIEFING_RSS_SOURCES: dict[str, str] = {
    # AI & LLMs
    "Anthropic": _google_news_rss("site:anthropic.com/news Anthropic when:7d"),
    "Google AI": "https://blog.google/technology/ai/rss/",
    "OpenAI": "https://openai.com/news/rss.xml",
    "AI Industry News": _google_news_rss(
        '(AI OR "large language model" OR LLM) '
        '(Reuters OR TechCrunch OR "MIT Technology Review" OR Ars) when:2d'
    ),
    # Python & software development
    "Python Insider": "https://blog.python.org/rss.xml",
    "GitHub Blog": "https://github.blog/feed/",
    "Software Development News": _google_news_rss(
        '(Python OR GitHub OR "software development" OR "developer tools") '
        '(InfoQ OR "The New Stack" OR Ars OR TechCrunch) when:3d'
    ),
    # Telecom / BSS
    "Telecom & BSS News": _google_news_rss(
        '(telecom OR telco OR "TM Forum" OR BSS OR OSS OR charging OR billing '
        'OR "customer management") '
        '("TM Forum" OR "Light Reading" OR "Mobile World Live" OR Reuters '
        'OR "RCR Wireless") when:4d'
    ),
    # Business & markets
    "Business & Markets News": _google_news_rss(
        "(business OR markets OR economy OR earnings OR RBI OR Sensex OR Nifty "
        "OR rupee OR rates) (Reuters OR CNBC OR Moneycontrol) when:2d"
    ),
}


RSS_SOURCES = BRIEFING_RSS_SOURCES


SOURCE_CATEGORIES: dict[str, str] = {
    "Anthropic": CATEGORY_AI,
    "Google AI": CATEGORY_AI,
    "OpenAI": CATEGORY_AI,
    "AI Industry News": CATEGORY_AI,
    "Python Insider": CATEGORY_PYTHON,
    "GitHub Blog": CATEGORY_PYTHON,
    "Software Development News": CATEGORY_PYTHON,
    "Telecom & BSS News": CATEGORY_TELECOM,
    "Business & Markets News": CATEGORY_BUSINESS,
}

SOURCE_QUALITY: dict[str, str] = {
    "Anthropic": QUALITY_PRIMARY,
    "Google AI": QUALITY_PRIMARY,
    "OpenAI": QUALITY_PRIMARY,
    "Python Insider": QUALITY_PRIMARY,
    "GitHub Blog": QUALITY_PRIMARY,
    "AI Industry News": QUALITY_DISCOVERY,
    "Software Development News": QUALITY_DISCOVERY,
    "Telecom & BSS News": QUALITY_DISCOVERY,
    "Business & Markets News": QUALITY_DISCOVERY,
}

# Freshness is intentionally category-specific. Niche telecom/software stories can
# remain useful for longer than fast-moving markets news.
CATEGORY_MAX_AGE_HOURS: dict[str, int] = {
    CATEGORY_AI: 72,
    CATEGORY_PYTHON: 96,
    CATEGORY_TELECOM: 120,
    CATEGORY_BUSINESS: 48,
}
