def build_news_prompt(news):

    articles = ""

    for index, article in enumerate(news, start=1):

        articles += f"""
==============================
Article {index}

Source:
{article['source']}

Title:
{article['title']}

Summary:
{article.get('summary', 'No summary available')}

Link:
{article['link']}
"""

    prompt = f"""
You are an expert AI News Editor.

You will receive AI news articles collected from multiple trusted sources.

Each article contains:
- Source
- Title
- Summary
- Link

Your responsibilities:

1. Read every article carefully.
2. Ignore duplicate stories.
3. Merge related news together.
4. Identify the biggest news of the day.
5. Mention important AI tools released.
6. Mention significant research papers.
7. Explain why today's news matters.

Return the answer using EXACTLY this format:

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

Maximum 300 words.

Articles:

{articles}
"""

    return prompt