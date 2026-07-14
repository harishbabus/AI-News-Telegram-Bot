from typing import Any


def build_news_prompt(news: list[dict[str, Any]]) -> str:
    """
    Builds the prompt used by the LLM to generate the AI Daily Brief.

    Args:
        news: List of news article dictionaries. Each article should contain:
            - source
            - title
            - summary
            - link

    Returns:
        A formatted prompt string ready to be sent to the LLM.
    """

    article_sections = []

    for index, article in enumerate(news, start=1):
        article_sections.append(
            f"""
==============================
Article {index}

Source:
{article.get("source", "Unknown")}

Title:
{article.get("title", "Untitled")}

Summary:
{article.get("summary", "No summary available.")}

Link:
{article.get("link", "N/A")}
""".strip()
        )

    articles = "\n\n".join(article_sections)

    return f"""
You are an experienced AI News Editor responsible for creating a concise, accurate, and engaging daily AI news briefing for technology professionals.

## Objective

Analyze the provided news articles and produce a high-quality daily AI news summary.

## Instructions

1. Read every article carefully.
2. Remove duplicate stories.
3. Merge articles covering the same event.
4. Identify the single most important AI story of the day.
5. Highlight newly released AI tools, products, or features.
6. Highlight significant AI research papers or breakthroughs.
7. Explain why today's news matters.
8. Use only information contained in the supplied articles.
9. Do not invent or assume facts.
10. If a section has no relevant information, write "None today."

## Output Format

🧠 AI Daily Brief

🔥 Top Story
<summary>

🛠 New AI Tools
• item
• item

📄 Research Highlights
• item
• item

💡 Why Today's News Matters
<summary>

## Rules

- Maximum 300 words.
- Use clear, professional language.
- Keep the summary concise.
- Prioritize factual accuracy over completeness.
- Do not include introductory or closing remarks.

## Articles

{articles}
""".strip()