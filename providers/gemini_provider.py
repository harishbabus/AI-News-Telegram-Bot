from google import genai

from config import GEMINI_API_KEY
from providers.base_provider import AIProvider
from prompts.news_summary_prompt import build_news_prompt


class GeminiProvider(AIProvider):

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def summarize(self, news):

        prompt = build_news_prompt(news)

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text