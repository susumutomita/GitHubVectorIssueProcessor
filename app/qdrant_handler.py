"""
This module contains the QdrantHandler class, which is responsible for interacting with the Qdrant
vector database and Groq client to handle issue embeddings and search similar issues.
"""

import logging

import requests
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse  # ここを追加
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import get_env_var

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QdrantHandler:
    """
    A handler class to manage Qdrant collections and embeddings.

    Attributes:
        client (QdrantClient): An instance of the QdrantClient.
        groq_client (Groq): An instance of the Groq client.
    """

    def __init__(self, groq_client):
        """
        Initialize the QdrantHandler with the Qdrant client and ensure the collection exists.

        Args:
            groq_client (Groq): An instance of the Groq client.
        """
        url = get_env_var("QD_URL")
        api_key = get_env_var("QD_API_KEY")
        self.collection_name = get_env_var("GITHUB_REPOSITORY").replace("/", "-")
        self.client = QdrantClient(url=url, api_key=api_key)
        self.groq_client = groq_client
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Ensure the collection exists in Qdrant. If not, create a new one.
        """
        try:
            self.client.get_collection(collection_name=self.collection_name)
            logger.info("Collection %s exists.", self.collection_name)
        except UnexpectedResponse as e:
            if e.status_code == 404:
                logger.warning(
                    "Collection not found, creating a new one. Details: %s", e
                )
                try:
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                    )
                    logger.info(
                        "Collection %s created successfully.", self.collection_name
                    )
                except UnexpectedResponse as create_e:
                    logger.error("Failed to create collection: %s", create_e)
                    raise
            else:
                logger.error("Error checking collection existence: %s", e)
                raise

    def add_issue(self, text, issue_number):
        """
        Add a new issue to the Qdrant collection.

        Args:
            text (str): The text content of the issue.
            issue_number (int): The issue number.
        """
        embedding = self._create_embedding(text)
        point = PointStruct(id=issue_number, vector=embedding, payload={"text": text})
        self.client.upsert(self.collection_name, [point])
        logger.info("Issue #%d added to the %s.", issue_number, self.collection_name)

    def search_similar_issues(self, text):
        """
        Search for similar issues in the Qdrant collection.

        Args:
            text (str): The text content of the issue to search for.

        Returns:
            list: A list of similar issues.
        """
        embedding = self._create_embedding(text)
        results = self.client.search(
            collection_name=self.collection_name, query_vector=embedding
        )
        logger.info("Found %d similar issues.", len(results))
        return results[:3]

    def _create_embedding(self, text):
        """
        Create an embedding for the given text using the Nomic API.

        Args:
            text (str): The text content to create an embedding for.

        Returns:
            list: The embedding vector for the given text.

        Raises:
            ValueError: If the embedding creation fails.
        """
        url = "https://api-atlas.nomic.ai/v1/embedding/text"
        headers = {
            "Authorization": f"Bearer {get_env_var('NOMIC_API_KEY')}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "nomic-embed-text-v1",
            "texts": [text],
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            embedding = response.json()["embeddings"][0]
            return embedding

        logger.error("Failed to create embedding: %s", response.content)
        raise ValueError(f"Failed to create embedding: {response.content}")
