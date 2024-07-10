"""
This module contains the QdrantHandler class, which is responsible for interacting with the Qdrant
vector database and Groq client to handle issue embeddings and search similar issues.
"""

import os

import requests
from qdrant_client.models import Distance, PointStruct, VectorParams
from requests.exceptions import RequestException


class QdrantHandler:
    """
    A handler class to manage Qdrant collections and embeddings.

    Attributes:
        client (QdrantClient): An instance of the QdrantClient.
        groq_client (Groq): An instance of the Groq client.
    """

    def __init__(self, client, groq_client):
        """
        Initialize the QdrantHandler with the given clients and ensure the collection exists.

        Args:
            client (QdrantClient): An instance of the QdrantClient.
            groq_client (Groq): An instance of the Groq client.
        """
        self.client = client
        self.groq_client = groq_client
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Ensure the collection exists in Qdrant. If not, create a new one.
        """
        try:
            self.client.get_collection(collection_name="issue_collection")
        except RequestException as e:
            print(f"Collection not found, creating a new one. Details: {e}")
            self.client.create_collection(
                collection_name="issue_collection",
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            print("Collection 'issue_collection' created successfully.")

    def add_issue(self, text, issue_number):
        """
        Add a new issue to the Qdrant collection.

        Args:
            text (str): The text content of the issue.
            issue_number (int): The issue number.
        """
        embedding = self._create_embedding(text)
        point = PointStruct(id=issue_number, vector=embedding, payload={"text": text})
        self.client.upsert("issue_collection", [point])

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
            collection_name="issue_collection", query_vector=embedding
        )
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
            "Authorization": f"Bearer {os.getenv('NOMIC_API_KEY')}",
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
        raise ValueError(f"Failed to create embedding: {response.content}")
