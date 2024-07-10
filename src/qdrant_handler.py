import os

import requests
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class QdrantHandler:
    def __init__(self, client, groq_client):
        self.client = client
        self.groq_client = groq_client
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            self.client.get_collection(collection_name="issue_collection")
        except Exception as e:
            print(f"Collection not found, creating a new one. Details: {e}")
            self.client.create_collection(
                collection_name="issue_collection",
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            print("Collection 'issue_collection' created successfully.")

    def add_issue(self, text, issue_number):
        embedding = self._create_embedding(text)
        point = PointStruct(id=issue_number, vector=embedding, payload={"text": text})
        self.client.upsert("issue_collection", [point])

    def search_similar_issues(self, text):
        embedding = self._create_embedding(text)
        results = self.client.search(
            collection_name="issue_collection", query_vector=embedding
        )
        return results[:3]

    def _create_embedding(self, text):
        url = "https://api-atlas.nomic.ai/v1/embedding/text"
        headers = {
            "Authorization": f"Bearer {os.getenv('NOMIC_API_KEY')}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "nomic-embed-text-v1",
            "texts": [text],
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            embedding = response.json()["embeddings"][0]
            return embedding
        else:
            raise ValueError(f"Failed to create embedding: {response.content}")
