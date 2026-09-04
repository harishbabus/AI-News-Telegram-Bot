from openai import OpenAI

from app.config import OPENAI_API_KEY
from common.constants import OPENAI_MODEL
from common.logger import logger
from common.models import NewsList
from prompts.news_summary_prompt import build_news_prompt
from providers.base_provider import AIProvider


class OpenAIProvider(AIProvider):
    """AI provider implementation using OpenAI models."""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def summarize(self, news: NewsList, prompt: str | None = None) -> str:
        """Generate the briefing from the supplied news articles."""
        logger.info("Generating briefing using OpenAI.")
        prompt = prompt or build_news_prompt(news)

        try:
            response = self.client.responses.create(
                model=OPENAI_MODEL,
                input=prompt,
            )

            text = response.output_text
            if not text:
                raise RuntimeError("OpenAI returned an empty response.")

            logger.info("OpenAI briefing generated successfully.")
            return text
        except Exception:
            logger.exception("OpenAI briefing generation failed.")
            raise
