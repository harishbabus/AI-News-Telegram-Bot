from openai import OpenAI

from app.config import OPENAI_API_KEY
from providers.base_provider import AIProvider


class OpenAIProvider(AIProvider):

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def summarize(self, news):

        return "OpenAI Summary (coming next)"