from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


class QdrantHandler:
    def __init__(self, client: QdrantClient, embedding_model):
        self.client = client
        self.embedding_model = embedding_model

    def add_issue(self, text: str, issue_number: int):
        embedding = self.embedding_model.create_embedding(text)
        point = PointStruct(id=issue_number, vector=embedding, payload={"text": text})
        self.client.upsert("issue_collection", [point])

    def search_similar_issues(self, text: str):
        embedding = self.embedding_model.create_embedding(text)
        results = self.client.search(
            collection_name="issue_collection", query_vector=embedding
        )
        return results[:3]
