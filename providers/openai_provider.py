from typing import Any

from openai import OpenAI

from app.config import OPENAI_API_KEY
from providers.base_provider import AIProvider


class OpenAIProvider(AIProvider):
    """
    AI provider implementation using OpenAI models.
    """

    def __init__(self)-> None:
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def summarize(self, news: list[dict[str, Any]]) -> str:
        """
        Generates a summary of the supplied news articles using the Gemini API.
        
        Args:
            news: List of news article dictionaries.
        
        Returns:
            A summarized string of the news articles.
        """

        return "OpenAI Summary (coming next)"