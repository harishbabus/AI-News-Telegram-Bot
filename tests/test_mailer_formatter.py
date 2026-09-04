"""Tests for HTML Daily Briefing rendering."""

from mailer.formatter import format_daily_briefing_html


def test_daily_briefing_html_formats_executive_story_and_source() -> None:
    briefing = """📰 Daily Briefing

Today’s signal
AI investment remains the main theme today.

🤖 AI & LLMs

1. Major model release
A new model was announced.
Why it matters: Developers gain new capabilities.
Source name: OpenAI
Source: https://example.com/story

🎯 What matters most today
• Watch adoption by developers.
"""

    result = format_daily_briefing_html(briefing, "04 September 2026")

    assert "Daily Briefing" in result
    assert "04 September 2026" in result
    assert "🤖 AI &amp; LLMs" in result
    assert "WHY IT MATTERS" in result
    assert "OpenAI" in result
    assert '<a href="https://example.com/story">Read article →</a>' in result
    assert "Source: https://example.com/story" not in result
    assert 'class="story"' in result


def test_daily_briefing_html_removes_separator_artifacts() -> None:
    result = format_daily_briefing_html(
        "📰 Daily Briefing\n\nToday’s signal\nSignal.\n\n---\n\n🤖 AI & LLMs\nNo major headline today.",
        "04 September 2026",
    )
    assert ">---</" not in result
    assert "No major headline today." in result


def test_daily_briefing_html_escapes_untrusted_text() -> None:
    result = format_daily_briefing_html(
        "📰 Daily Briefing\n\nToday’s signal\n<script>alert(1)</script>",
        "04 September 2026",
    )
    assert "<script>" not in result
    assert "&lt;script&gt;" in result
