"""HTML rendering for the Daily Briefing email."""

import re
from html import escape

SECTION_HEADINGS = {
    "🤖 AI & LLMs",
    "🐍 Python & Software Development",
    "📡 Telecom / BSS",
    "💹 Business & Markets",
    "🎯 What matters most today",
}

_URL_RE = re.compile(r"^Source:\s*(https?://\S+)\s*$")
_SOURCE_NAME_RE = re.compile(r"^Source name:\s*(.+)$", re.IGNORECASE)
_STORY_RE = re.compile(r"^(\d+)\.\s+(.+)$")
_SEPARATOR_RE = re.compile(r"^[-_=]{3,}$")


def format_daily_briefing_html(briefing: str, date_label: str) -> str:
    """Convert the briefing's stable text format into an executive newsletter."""
    body: list[str] = []
    in_signal = False
    in_story = False
    source_name = ""

    def close_signal() -> None:
        nonlocal in_signal
        if in_signal:
            body.append("</div>")
            in_signal = False

    def close_story() -> None:
        nonlocal in_story, source_name
        if in_story:
            body.append("</div>")
            in_story = False
        source_name = ""

    for raw_line in briefing.splitlines():
        line = raw_line.strip()
        if not line or _SEPARATOR_RE.match(line):
            continue

        if line == "📰 Daily Briefing":
            continue

        if line in {"Today’s signal", "Today's signal"}:
            close_story()
            close_signal()
            in_signal = True
            body.append(
                '<div class="signal"><div class="eyebrow">TODAY’S SIGNAL</div>'
            )
            continue

        if line in SECTION_HEADINGS:
            close_signal()
            close_story()
            css_class = "takeaways-heading" if line.startswith("🎯") else ""
            body.append(f'<h2 class="{css_class}">{escape(line)}</h2>')
            continue

        story_match = _STORY_RE.match(line)
        if story_match:
            close_signal()
            close_story()
            number, title = story_match.groups()
            in_story = True
            body.append('<div class="story">')
            body.append(
                '<div class="story-heading">'
                f'<span class="story-number">{escape(number.zfill(2))}</span>'
                f'<h3>{escape(title)}</h3></div>'
            )
            continue

        source_name_match = _SOURCE_NAME_RE.match(line)
        if source_name_match:
            source_name = source_name_match.group(1).strip()
            continue

        source_match = _URL_RE.match(line)
        if source_match:
            url = escape(source_match.group(1), quote=True)
            label = escape(source_name) if source_name else "Source"
            body.append(
                '<div class="story-meta">'
                f'<span class="source-name">{label}</span>'
                '<span class="dot">•</span>'
                f'<a href="{url}">Read article →</a></div>'
            )
            source_name = ""
            continue

        if line.startswith("Why it matters:"):
            text = line.removeprefix("Why it matters:").strip()
            body.append(
                '<div class="why"><div class="why-label">WHY IT MATTERS</div>'
                f'<div>{escape(text)}</div></div>'
            )
            continue

        if line.startswith(("• ", "- ")):
            text = line[2:].strip()
            body.append(
                '<div class="takeaway"><span>→</span><div>'
                f"{escape(text)}</div></div>"
            )
            continue

        if line == "No major headline today.":
            body.append('<div class="empty">No major headline today.</div>')
            continue

        cls = "signal-text" if in_signal else "copy"
        body.append(f'<p class="{cls}">{escape(line)}</p>')

    close_signal()
    close_story()

    content = "\n".join(body)
    safe_date = escape(date_label)

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{ margin:0; padding:0; background:#eef2f6; font-family:Arial,Helvetica,sans-serif; color:#1d2939; }}
.wrapper {{ width:100%; padding:28px 12px; box-sizing:border-box; }}
.card {{ max-width:720px; margin:0 auto; background:#ffffff; border-radius:12px; overflow:hidden; border:1px solid #e4e7ec; }}
.header {{ padding:26px 32px 22px; background:#ffffff; border-bottom:1px solid #e4e7ec; }}
.header-top {{ display:flex; justify-content:space-between; gap:16px; align-items:center; }}
.kicker {{ font-size:11px; letter-spacing:1.5px; font-weight:700; color:#667085; }}
.date {{ font-size:12px; color:#667085; white-space:nowrap; }}
.header h1 {{ margin:9px 0 4px; font-size:29px; line-height:1.15; color:#101828; }}
.subtitle {{ margin:0; font-size:13px; color:#667085; }}
.content {{ padding:26px 32px 34px; }}
.signal {{ margin:0 0 30px; padding:18px 20px; background:#f8fafc; border:1px solid #e4e7ec; border-radius:10px; }}
.eyebrow {{ font-size:10px; letter-spacing:1.4px; font-weight:700; color:#667085; margin-bottom:8px; }}
.signal-text {{ margin:0; font-size:16px; line-height:1.55; color:#344054; }}
h2 {{ margin:32px 0 14px; padding-bottom:10px; border-bottom:2px solid #eaecf0; font-size:20px; line-height:1.3; color:#101828; }}
.story {{ padding:18px 0 20px; border-bottom:1px solid #eaecf0; }}
.story:last-child {{ border-bottom:0; }}
.story-heading {{ display:flex; gap:12px; align-items:flex-start; }}
.story-number {{ flex:0 0 auto; margin-top:2px; font-size:11px; line-height:22px; width:24px; height:22px; text-align:center; border-radius:5px; background:#f2f4f7; color:#667085; font-weight:700; }}
h3 {{ margin:0 0 8px; font-size:17px; line-height:1.38; color:#101828; }}
.copy {{ margin:7px 0 9px; font-size:14.5px; line-height:1.6; color:#344054; }}
.why {{ margin:12px 0; padding:11px 13px; background:#f9fafb; border-left:3px solid #98a2b3; border-radius:4px; font-size:13.5px; line-height:1.5; color:#344054; }}
.why-label {{ margin-bottom:4px; font-size:9px; letter-spacing:1.1px; font-weight:700; color:#667085; }}
.story-meta {{ margin-top:11px; font-size:12.5px; color:#667085; }}
.source-name {{ font-weight:700; color:#475467; }}
.dot {{ margin:0 7px; }}
a {{ color:#175cd3; font-weight:700; text-decoration:none; }}
.takeaways-heading {{ margin-top:34px; }}
.takeaway {{ display:flex; gap:9px; margin:8px 0; padding:10px 12px; background:#f8fafc; border-radius:7px; font-size:14px; line-height:1.5; color:#344054; }}
.takeaway span {{ color:#667085; font-weight:700; }}
.empty {{ margin:10px 0 22px; padding:12px 14px; background:#f8fafc; color:#667085; border-radius:7px; font-size:14px; }}
.footer {{ padding:16px 32px; background:#f9fafb; color:#98a2b3; font-size:11px; border-top:1px solid #e4e7ec; text-align:center; }}
@media (max-width:600px) {{ .wrapper {{ padding:0; }} .card {{ border-radius:0; border-left:0; border-right:0; }} .header,.content,.footer {{ padding-left:20px; padding-right:20px; }} .header-top {{ display:block; }} .date {{ margin-top:5px; }} .header h1 {{ font-size:26px; }} }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="card">
    <div class="header">
      <div class="header-top">
        <div class="kicker">PERSONALISED NEWS BRIEFING</div>
        <div class="date">{safe_date}</div>
      </div>
      <h1>Daily Briefing</h1>
      <p class="subtitle">AI · Software · Telecom / BSS · Markets</p>
    </div>
    <div class="content">{content}</div>
    <div class="footer">A concise briefing of the developments worth your attention today.</div>
  </div>
</div>
</body>
</html>"""
