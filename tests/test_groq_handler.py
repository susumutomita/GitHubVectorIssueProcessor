from unittest.mock import patch

from app.groq_handler import GroqHandler


@patch("app.groq_handler.Groq")
def test_groq_handler_initialization(mock_groq):
    GroqHandler()
    mock_groq.assert_called_once_with(api_key="dummy_groq_api_key")


def test_groq_handler_get_client():
    handler = GroqHandler()
    client = handler.get_client()
    assert client is handler.groq_client
