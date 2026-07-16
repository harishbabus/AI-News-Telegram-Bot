# Third-party imports
import requests

# Local application imports
from app.config import BOT_TOKEN, CHAT_ID
from common.constants import TELEGRAM_REQUEST_TIMEOUT
from common.logger import logger

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_message(message: str) -> bool:
    """
    Sends a message to the configured Telegram chat.

    Args:
        message: The message text to send.

    Returns:
        True if the message was sent successfully, False otherwise.
    """

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }

    try:
        logger.info("Sending message to Telegram.")

        response = requests.post(
            TELEGRAM_API_URL,
            data=payload,
            timeout=TELEGRAM_REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        result = response.json()

        if result.get("ok"):
            logger.info(
                "Telegram message sent successfully to chat %s.",
                CHAT_ID,
            )
            return True

        logger.error(
            "Telegram API returned an error: %s",
            result.get("description", "Unknown error"),
        )

        return False

    except requests.RequestException:
        logger.exception("Failed to send Telegram message.")
        return False
