"""Abstract interface for AI providers."""

from abc import ABC, abstractmethod

from common.models import NewsList


class AIProvider(ABC):
    """Abstract interface implemented by each LLM provider."""

    @abstractmethod
    def summarize(self, news: NewsList, prompt: str | None = None) -> str:
        """Generate text from the supplied news and an optional prepared prompt."""
        raise NotImplementedError
