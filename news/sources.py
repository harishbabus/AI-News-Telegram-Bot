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
    "associated press",
    "financial times",
    "bloomberg",
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


# Telegram remains AI-only. The larger set improves discovery before editorial
# scoring narrows the pool again.
AI_RSS_SOURCES: dict[str, str] = {
    "Anthropic": _google_news_rss("site:anthropic.com/news Anthropic when:7d"),
    "Google AI": "https://blog.google/technology/ai/rss/",
    "OpenAI": "https://openai.com/news/rss.xml",
    "AI Reuters": _google_news_rss(
        '(AI OR "artificial intelligence" OR LLM OR OpenAI OR Anthropic '
        "OR Gemini OR Mistral) Reuters when:2d"
    ),
    "AI Technology News": _google_news_rss(
        '(AI OR "large language model" OR "AI agent" OR "coding agent") '
        '(TechCrunch OR "MIT Technology Review" OR Ars) when:2d'
    ),
    "AI Infrastructure News": _google_news_rss(
        '(AI chip OR GPU OR "AI data center" OR "AI datacenter" OR inference) '
        "(Reuters OR TechCrunch OR CNBC) when:3d"
    ),
}


# Email discovery is intentionally broad. Relevance/scoring and Gemini make the
# final editorial cut; discovery feeds should not be mistaken for evidence.
BRIEFING_RSS_SOURCES: dict[str, str] = {
    # AI & LLMs
    **AI_RSS_SOURCES,
    # Python & software development
    "Python Insider": "https://blog.python.org/rss.xml",
    "GitHub Blog": "https://github.blog/feed/",
    "Python Ecosystem News": _google_news_rss(
        "(Python OR CPython OR PyPI OR Django OR FastAPI) "
        '(InfoQ OR "The New Stack" OR Ars OR TechCrunch) when:4d'
    ),
    "Developer Tools & Security": _google_news_rss(
        '(GitHub OR "developer tools" OR "software supply chain" '
        'OR "software vulnerability" OR "coding agent") '
        '(Reuters OR InfoQ OR "The New Stack" OR Ars OR TechCrunch) when:3d'
    ),
    # Telecom / BSS
    "TM Forum News": _google_news_rss(
        'site:tmforum.org (AI OR "autonomous networks" OR BSS OR OSS '
        'OR "Open API" OR ODA OR charging OR monetization) when:7d'
    ),
    "Telecom Reuters": _google_news_rss(
        '(telecom OR telco OR 5G OR 6G OR "network slicing") Reuters when:3d'
    ),
    "Telecom Specialist News": _google_news_rss(
        '(telecom OR telco OR 5G OR 6G OR "network slicing" OR satellite) '
        '("Light Reading" OR "Mobile World Live" OR "RCR Wireless") when:4d'
    ),
    "BSS OSS News": _google_news_rss(
        '(BSS OR OSS OR charging OR billing OR "customer management" '
        'OR "service orchestration" OR "autonomous network") '
        '("TM Forum" OR "Light Reading" OR "Mobile World Live") when:5d'
    ),
    # Business & markets
    "Global Markets Reuters": _google_news_rss(
        "(markets OR economy OR inflation OR rates OR oil OR Fed "
        "OR earnings OR IPO OR acquisition) Reuters when:2d"
    ),
    "India Markets Reuters": _google_news_rss(
        '(India OR RBI OR rupee OR Nifty OR Sensex OR "Indian markets" '
        'OR "India economy") Reuters when:2d'
    ),
    "Technology Business Reuters": _google_news_rss(
        "(technology OR software OR AI OR semiconductor OR cloud) "
        "(deal OR acquisition OR IPO OR investment OR earnings) Reuters when:2d"
    ),
    "Business & Markets News": _google_news_rss(
        "(business OR markets OR economy OR earnings OR RBI OR Sensex OR Nifty "
        "OR rupee OR rates OR oil) (CNBC OR Moneycontrol) when:2d"
    ),
}

RSS_SOURCES = BRIEFING_RSS_SOURCES

SOURCE_CATEGORIES: dict[str, str] = {
    "Anthropic": CATEGORY_AI,
    "Google AI": CATEGORY_AI,
    "OpenAI": CATEGORY_AI,
    "AI Reuters": CATEGORY_AI,
    "AI Technology News": CATEGORY_AI,
    "AI Infrastructure News": CATEGORY_AI,
    "Python Insider": CATEGORY_PYTHON,
    "GitHub Blog": CATEGORY_PYTHON,
    "Python Ecosystem News": CATEGORY_PYTHON,
    "Developer Tools & Security": CATEGORY_PYTHON,
    "TM Forum News": CATEGORY_TELECOM,
    "Telecom Reuters": CATEGORY_TELECOM,
    "Telecom Specialist News": CATEGORY_TELECOM,
    "BSS OSS News": CATEGORY_TELECOM,
    "Global Markets Reuters": CATEGORY_BUSINESS,
    "India Markets Reuters": CATEGORY_BUSINESS,
    "Technology Business Reuters": CATEGORY_BUSINESS,
    "Business & Markets News": CATEGORY_BUSINESS,
}

SOURCE_QUALITY: dict[str, str] = {
    "Anthropic": QUALITY_PRIMARY,
    "Google AI": QUALITY_PRIMARY,
    "OpenAI": QUALITY_PRIMARY,
    "Python Insider": QUALITY_PRIMARY,
    "GitHub Blog": QUALITY_PRIMARY,
    "AI Reuters": QUALITY_DISCOVERY,
    "AI Technology News": QUALITY_DISCOVERY,
    "AI Infrastructure News": QUALITY_DISCOVERY,
    "Python Ecosystem News": QUALITY_DISCOVERY,
    "Developer Tools & Security": QUALITY_DISCOVERY,
    "TM Forum News": QUALITY_DISCOVERY,
    "Telecom Reuters": QUALITY_DISCOVERY,
    "Telecom Specialist News": QUALITY_DISCOVERY,
    "BSS OSS News": QUALITY_DISCOVERY,
    "Global Markets Reuters": QUALITY_DISCOVERY,
    "India Markets Reuters": QUALITY_DISCOVERY,
    "Technology Business Reuters": QUALITY_DISCOVERY,
    "Business & Markets News": QUALITY_DISCOVERY,
}

CATEGORY_MAX_AGE_HOURS: dict[str, int] = {
    CATEGORY_AI: 72,
    CATEGORY_PYTHON: 96,
    CATEGORY_TELECOM: 120,
    CATEGORY_BUSINESS: 48,
}
