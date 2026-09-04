from common.models import NewsList


def build_telegram_summary_prompt(news: NewsList) -> str:
    """Build the editorial AI-only digest prompt used for Telegram."""
    articles: list[str] = []
    for index, article in enumerate(news, start=1):
        articles.append(
            "\n".join(
                [
                    f"Article {index}",
                    f"Feed source: {article.source}",
                    f"Publisher: {article.publisher or article.source}",
                    f"Source quality: {article.source_quality}",
                    f"Verification: {article.verification_status}",
                    f"Verification note: {article.verification_reason or 'Not checked'}",
                    f"Published: {article.published or 'Not supplied'}",
                    f"Page date: {article.content_date or 'Not found'}",
                    f"Title: {article.title}",
                    f"Summary: {article.summary}",
                    f"Verified page excerpt: {article.content_excerpt or 'Not available'}",
                    f"Link: {article.verified_url or article.link}",
                ]
            )
        )

    formatted_articles = "\n\n".join(articles)
    return f"""
You are editing a concise AI news digest for Telegram.

Select and synthesise the supplied AI news. Do not produce a raw article list.
Focus on what is genuinely important, useful, or new. Merge duplicate stories.
Prefer source_quality=primary items with Verification=verified and avoid hype.
Verification=verified means the publisher page was fetched and matched; partial is useful
supporting evidence. A failed, unresolved, or not_checked verification result does NOT by
itself mean that an ordinary story is false; such an item may still be used when its source
and claim are routine and credible. Treat discovery-source items as leads rather than proof.
Use only facts supported by the supplied articles. For extraordinary, security-sensitive,
major model-launch, acquisition, or large financial claims, require a verified primary article
or corroborating established evidence. If a discovery item is unresolved, failed, or not
checked and is the only evidence for a sensational claim, omit it.

Never leave a section blank. TOP STORIES must contain 2-4 bullets whenever at least two
credible supplied articles are available. If fewer than two are usable, include the usable
ones and then write "No additional major story verified today." NEW AI TOOLS and RESEARCH
HIGHLIGHTS must use their explicit fallback sentence when no material item qualifies.

Return exactly these sections and headings:

🔥 TOP STORIES
• 2-4 concise bullets covering the most important developments.

🛠️ NEW AI TOOLS
• 0-3 concise bullets about noteworthy models, products, APIs, developer tools,
  or practical capabilities. If there is nothing material, write:
  No major tool release today.

🔬 RESEARCH HIGHLIGHTS
• 0-3 concise bullets about meaningful research, benchmarks, methods, or papers.
  If there is nothing material, write:
  No major research highlight today.

🎯 WHY TODAY'S NEWS MATTERS
Write one compact paragraph (3-5 sentences) connecting the strongest signals and
explaining what they mean for engineers, product leaders, and AI practitioners.

Style rules:
- Mobile-friendly and editorial, not a catalogue.
- Keep the whole digest under about 750 words.
- No Markdown tables.
- No raw URLs and no "Source:" lines.
- No introductory or closing chatter.
- Do not repeat the same story across sections.

Articles:

{formatted_articles}
""".strip()
