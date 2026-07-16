from common.models import NewsList


def build_news_prompt(news: NewsList) -> str:
    """
    Builds the prompt used by the LLM to generate the AI Daily Brief.

    Args:
        news: List of NewsArticle instances. Each article should contain:
            - source
            - title
            - summary
            - link

    Returns:
        A formatted prompt string ready to be sent to the LLM.
    """

    article_sections: list[str] = []

    for index, article in enumerate(news, start=1):
        article_sections.append(
            "\n".join(
                [
                    "==============================",
                    f"Article {index}",
                    "",
                    "Source:",
                    article.source,
                    "",
                    "Title:",
                    article.title,
                    "",
                    "Summary:",
                    article.summary,
                    "",
                    "Link:",
                    article.link,
                ]
            )
        )

    formatted_articles = "\n\n".join(article_sections)

    PROMPT_TEMPLATE = """
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
    11. Always include the names of important companies, 
    models, or research papers exactly as written in
    the source articles.
    12. Do not repeat the same news in multiple sections.

    ## Writing Style

    - Be objective.
    - Avoid sensational language.
    - Mention product and model names exactly as given.
    - Do not repeat information across sections.

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

    {formatted_articles}
    """.strip()

    return PROMPT_TEMPLATE.format(formatted_articles=formatted_articles)