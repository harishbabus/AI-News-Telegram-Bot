"""Gemini provider with lightweight application-level resilience."""

import time
from collections.abc import Sequence

from google import genai

from app.config import GEMINI_API_KEY
from common.constants import GEMINI_MODEL
from common.logger import logger
from common.models import NewsList
from prompts.news_summary_prompt import build_news_prompt
from providers.base_provider import AIProvider

# The Google SDK already performs some retries. These short application-level
# retries protect scheduled runs from a transient 429/5xx that survives the SDK.
_RETRY_DELAYS_SECONDS: Sequence[float] = (2.0, 5.0)
_TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


def _status_code(exc: Exception) -> int | None:
    """Best-effort extraction of an HTTP-like status code from SDK errors."""
    value = getattr(exc, "status_code", None)
    if isinstance(value, int):
        return value

    response = getattr(exc, "response", None)
    value = getattr(response, "status_code", None)
    if isinstance(value, int):
        return value

    # Keep this deliberately narrow: only known transient markers are matched.
    text = str(exc).upper()
    for code in _TRANSIENT_STATUS_CODES:
        if str(code) in text:
            return code
    if "UNAVAILABLE" in text or "HIGH DEMAND" in text:
        return 503
    if "RESOURCE_EXHAUSTED" in text or "TOO MANY REQUESTS" in text:
        return 429
    return None


def _is_transient(exc: Exception) -> bool:
    return _status_code(exc) in _TRANSIENT_STATUS_CODES


class GeminiProvider(AIProvider):
    """AI provider implementation using Google's Gemini models."""

    def __init__(self) -> None:
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def summarize(self, news: NewsList, prompt: str | None = None) -> str:
        """Generate a summary, retrying only transient Gemini failures."""
        logger.info("Generating summary using Gemini.")
        prompt = prompt or build_news_prompt(news)
        total_attempts = len(_RETRY_DELAYS_SECONDS) + 1

        for attempt in range(1, total_attempts + 1):
            try:
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                )

                if not response.text:
                    raise RuntimeError("Gemini returned an empty response.")

                if attempt > 1:
                    logger.info(
                        "Gemini summary generated successfully on attempt %d.", attempt
                    )
                else:
                    logger.info("Gemini summary generated successfully.")
                return response.text

            except Exception as exc:
                if not _is_transient(exc) or attempt == total_attempts:
                    logger.exception(
                        "Gemini summarization failed after %d attempt(s).",
                        attempt,
                    )
                    raise

                delay = _RETRY_DELAYS_SECONDS[attempt - 1]
                logger.warning(
                    "Transient Gemini error (status=%s) on attempt %d/%d; "
                    "retrying in %.1fs.",
                    _status_code(exc),
                    attempt,
                    total_attempts,
                    delay,
                )
                time.sleep(delay)

        raise RuntimeError("Gemini retry loop exited unexpectedly.")
