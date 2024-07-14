from unittest.mock import MagicMock, patch

from app.groq_handler import GroqHandler
from app.qdrant_handler import QdrantHandler


@patch("app.qdrant_handler.QdrantClient")
@patch("app.groq_handler.Groq")
def test_add_issue(mock_groq_client, mock_qdrant_client):
    mock_qdrant_instance = mock_qdrant_client.return_value

    # Create QdrantHandler instance
    groq_handler = GroqHandler()
    handler = QdrantHandler(groq_handler.groq_client)

    # Mock _create_embedding method
    handler._create_embedding = MagicMock(return_value=[0.1, 0.2, 0.3])

    # Call add_issue and verify the expected interactions
    handler.add_issue("Test issue", 1)
    mock_qdrant_instance.upsert.assert_called_once()


@patch("app.qdrant_handler.QdrantClient")
@patch("app.groq_handler.Groq")
def test_search_similar_issues(mock_groq_client, mock_qdrant_client):
    mock_qdrant_instance = mock_qdrant_client.return_value

    # Create QdrantHandler instance
    groq_handler = GroqHandler()
    handler = QdrantHandler(groq_handler.groq_client)

    # Mock _create_embedding method
    handler._create_embedding = MagicMock(return_value=[0.1, 0.2, 0.3])

    # Call search_similar_issues and verify the expected interactions
    handler.search_similar_issues("Test issue")
    mock_qdrant_instance.search.assert_called_once()
