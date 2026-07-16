from google import genai

from app.config import GEMINI_API_KEY
from common.constants import GEMINI_MODEL
from common.logger import logger
from common.models import NewsList
from prompts.news_summary_prompt import build_news_prompt
from providers.base_provider import AIProvider


class GeminiProvider(AIProvider):
    """
    AI provider implementation using Google's Gemini models.
    """

    def __init__(self) -> None:
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def summarize(self, news: NewsList) -> str:
        """
        Generates a summary of the supplied news articles using Gemini.

        Args:
            news: List of news article dictionaries.

        Returns:
            A summarized string.
        """
        logger.info("Generating summary using Gemini.")

        prompt = build_news_prompt(news)

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            logger.info("Gemini summary generated successfully.")

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text

        except Exception:
            logger.exception("Gemini summarization failed.")
            raise
