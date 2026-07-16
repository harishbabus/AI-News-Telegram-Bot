"""
Unit tests for telegram.bot.
"""

from unittest.mock import Mock, patch

import requests

from app.config import CHAT_ID
from telegram.bot import send_message


def test_send_message_success() -> None:
    """
    Returns True when Telegram accepts the message.
    """
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"ok": True}

    with patch(
        "telegram.bot.requests.post",
        return_value=response,
    ) as mock_post:
        result = send_message("Hello")

    assert result is True
    mock_post.assert_called_once()


def test_send_message_api_error() -> None:
    """
    Returns False when Telegram responds with ok=False.
    """
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "ok": False,
        "description": "Bad Request",
    }

    with patch(
        "telegram.bot.requests.post",
        return_value=response,
    ):
        result = send_message("Hello")

    assert result is False


def test_send_message_request_exception() -> None:
    """
    Returns False when the HTTP request fails.
    """
    with patch(
        "telegram.bot.requests.post",
        side_effect=requests.RequestException,
    ):
        result = send_message("Hello")

    assert result is False


def test_send_message_posts_correct_payload() -> None:
    """
    Sends the expected payload to Telegram.
    """
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"ok": True}

    with patch(
        "telegram.bot.requests.post",
        return_value=response,
    ) as mock_post:

        send_message("Test Message")

    _, kwargs = mock_post.call_args

    assert kwargs["data"]["text"] == "Test Message"
    assert kwargs["data"]["chat_id"] == CHAT_ID
