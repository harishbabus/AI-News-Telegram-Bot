"""
Defines the abstract interface for AI providers.

Concrete providers such as GeminiProvider and OpenAIProvider inherit
from AIProvider and implement the summarize() method.
"""

from abc import ABC, abstractmethod

from common.models import NewsList


class AIProvider(ABC):
    """
    Abstract interface for AI providers.
    """

    @abstractmethod
    def summarize(
        self,
        news: NewsList,
    ) -> str:
        """
        Generates a summary of the supplied news articles.

        Args:
            news: List of news article dictionaries.

        Returns:
            A summarized string of the news articles.
        """
        raise NotImplementedError
