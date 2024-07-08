from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams


class QdrantHandler:
    def __init__(self, client: QdrantClient, embedding_model):
        self.client = client
        self.embedding_model = embedding_model
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            self.client.get_collection(collection_name="issue_collection")
        except Exception as e:
            print(f"Collection not found, creating a new one. Details: {e}")
            self.client.create_collection(
                collection_name="issue_collection",
                vectors_config=VectorParams(size=512, distance="Cosine"),
            )

    def add_issue(self, text: str, issue_number: int):
        embedding = self.embedding_model.create_embedding(text)
        point = PointStruct(id=issue_number, vector=embedding, payload={"text": text})
        self.client.upsert(collection_name="issue_collection", points=[point])

    def search_similar_issues(self, text: str):
        embedding = self.embedding_model.create_embedding(text)
        results = self.client.search(
            collection_name="issue_collection", query_vector=embedding, limit=3
        )
        return results
