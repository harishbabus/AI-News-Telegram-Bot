from common.models import NewsList


def build_news_prompt(news: NewsList) -> str:
    """Build the prompt used to produce the four-topic daily briefing."""

    article_sections: list[str] = []

    for index, article in enumerate(news, start=1):
        article_sections.append(
            "\n".join(
                [
                    "==============================",
                    f"Article {index}",
                    f"Category: {article.category}",
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

    formatted_articles = "\n\n".join(article_sections)

    prompt_template = """
You are the editor of a concise executive daily briefing for a technology and
telecom engineering leader in India.

Your job is to select, verify within the supplied material, and synthesise only
the most important developments. Do not reproduce the feed as a list.

## Coverage

Create exactly these sections:
1. 🤖 AI & LLMs
2. 🐍 Python & Software Development
3. 📡 Telecom / BSS
4. 💹 Business & Markets
5. 🎯 What matters most today

## Editorial rules

1. Read all supplied articles, merge duplicates, and strongly prefer primary/official sources.
   Treat source_quality=primary plus Verification=verified as the strongest evidence.
   Verification=verified means the publisher page was fetched and matched. Verification=partial
   is supporting evidence only. Discovery sources are leads, not proof.
2. Include only material or genuinely useful developments. Never pad a section.
3. Exclude sports and entertainment completely.
4. Use only facts supported by the supplied articles. Do not invent details.
5. Rewrite promotional or sensational wording neutrally. For extraordinary, security-sensitive,
   model-launch, financial, acquisition, or market-moving claims, require either a verified
   primary article or corroborating established evidence in the supplied material. A discovery
   item with Verification=unresolved/failed/not_checked must never be the sole basis for such a
   claim. When evidence is insufficient, omit the claim rather than hedge or speculate.
6. Prefer recently published stories. If Published is missing, use the item only when its
   relevance is clear and avoid describing it as breaking or newly announced.
7. Do not expose RSS markup, HTML, escaped entities, feed boilerplate, or separators.
8. Do not repeat the same story in multiple sections.
9. For every selected story, include one source name and one source URL. Prefer Publisher
   over Feed source when Publisher identifies the original outlet.
10. Business & Markets should prioritise developments material to technology,
   global markets, India, rates, currencies, major companies, or the economy.
11. Telecom/BSS should prioritise operators, OSS/BSS, customer lifecycle,
    charging/monetisation, APIs, TM Forum, cloud-native architecture, and AI in telecom.
12. If a section has no sufficiently important story, write exactly:
    No major headline today.

## Required format

📰 Daily Briefing

Today’s signal
<2 concise sentences synthesising the most important cross-topic developments.>

🤖 AI & LLMs

1. <Headline>
<2 concise sentences explaining what happened.>
Why it matters: <1 concise sentence focused on practical impact.>
Source name: <source>
Source: <URL>

🐍 Python & Software Development

<same format, or "No major headline today.">

📡 Telecom / BSS

<same format, or "No major headline today.">

💹 Business & Markets

<same format, or "No major headline today.">

🎯 What matters most today
• <short actionable takeaway 1>
• <short actionable takeaway 2>
• <short actionable takeaway 3>

## Length and style

- Target 450-650 words maximum.
- Maximum 2 stories per section; one is enough when only one is truly material.
- Keep paragraphs short and skimmable.
- Use crisp professional English suitable for an executive email.
- No Markdown emphasis, no horizontal rules, no introductory or closing chatter.
- Do not say that you are an AI.

## Articles

{formatted_articles}
""".strip()

    return prompt_template.format(formatted_articles=formatted_articles)
