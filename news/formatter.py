"""Formatting helpers for Telegram delivery."""

from html import escape

from common.constants import MAX_TELEGRAM_MESSAGE_LENGTH
from common.models import NewsList


def split_message(message: str) -> list[str]:
    """Split a Telegram message at paragraph boundaries where possible."""
    if len(message) <= MAX_TELEGRAM_MESSAGE_LENGTH:
        return [message]

    paragraphs = message.split("\n\n")
    parts: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = paragraph if not current else f"{current}\n\n{paragraph}"
        if len(candidate) <= MAX_TELEGRAM_MESSAGE_LENGTH:
            current = candidate
            continue

        if current:
            parts.append(current)
            current = ""

        # A single paragraph should normally be well below Telegram's limit.
        # Fall back to a hard split only for unusually large content.
        while len(paragraph) > MAX_TELEGRAM_MESSAGE_LENGTH:
            parts.append(paragraph[:MAX_TELEGRAM_MESSAGE_LENGTH])
            paragraph = paragraph[MAX_TELEGRAM_MESSAGE_LENGTH:]
        current = paragraph

    if current or not parts:
        parts.append(current)

    return parts


def create_digest(news: NewsList) -> str:
    """Create a compact HTML-formatted AI digest for Telegram."""
    blocks = ["🤖 <b>AI Daily Digest</b>"]

    for article in news:
        source = escape(article.source)
        title = escape(article.title)
        summary = escape(article.summary.strip())
        link = escape(article.link, quote=True)

        block_lines = [
            f"📰 <b>{source}</b>",
            f"<b>{title}</b>",
        ]
        if summary:
            block_lines.append(summary)
        if link:
            block_lines.append(f'<a href="{link}">Read article →</a>')

        blocks.append("\n".join(block_lines))

    return "\n\n".join(blocks)


TELEGRAM_EDITORIAL_HEADINGS = {
    "🔥 TOP STORIES",
    "🛠️ NEW AI TOOLS",
    "🔬 RESEARCH HIGHLIGHTS",
    "🎯 WHY TODAY'S NEWS MATTERS",
}


def _fill_empty_editorial_sections(summary: str) -> str:
    """Guarantee that Gemini never leaves a Telegram editorial section blank."""
    fallbacks = {
        "🔥 TOP STORIES": "No sufficiently verified top story today.",
        "🛠️ NEW AI TOOLS": "No major tool release today.",
        "🔬 RESEARCH HIGHLIGHTS": "No major research highlight today.",
        "🎯 WHY TODAY'S NEWS MATTERS": (
            "No strong cross-cutting signal could be established "
            "from today's verified items."
        ),
    }
    lines = summary.splitlines()
    output: list[str] = []

    for index, raw_line in enumerate(lines):
        line = raw_line.strip()
        output.append(raw_line)
        if line not in TELEGRAM_EDITORIAL_HEADINGS:
            continue

        next_content = ""
        for following in lines[index + 1 :]:
            stripped = following.strip()
            if not stripped:
                continue
            if stripped in TELEGRAM_EDITORIAL_HEADINGS:
                break
            next_content = stripped
            break

        if not next_content:
            output.append(fallbacks[line])

    return "\n".join(output)


def format_telegram_editorial_digest(summary: str) -> str:
    """Safely render the editorial AI summary using Telegram HTML headings."""
    summary = _fill_empty_editorial_sections(summary)
    rendered: list[str] = []
    for raw_line in summary.splitlines():
        line = raw_line.strip()
        if not line:
            rendered.append("")
            continue
        safe_line = escape(line)
        if line in TELEGRAM_EDITORIAL_HEADINGS:
            rendered.append(f"<b>{safe_line}</b>")
        else:
            rendered.append(safe_line)
    return "\n".join(rendered).strip()
