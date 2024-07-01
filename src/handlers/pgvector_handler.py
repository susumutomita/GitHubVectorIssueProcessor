import psycopg2
import psycopg2.extras


class PgVectorHandler:
    def __init__(self, db_connection_str: str, embedding_model):
        self.conn = psycopg2.connect(db_connection_str)
        self.embedding_model = embedding_model

    def add_issue(self, text: str, issue_number: int):
        embedding = self.embedding_model.create_embedding(text)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO issue_vectors (issue_number, embedding, text) VALUES (%s, %s, %s)",
                (issue_number, embedding, text),
            )
        self.conn.commit()

    def search_similar_issues(self, text: str):
        embedding = self.embedding_model.create_embedding(text)
        query = """
        SELECT id, issue_number, text, 1 - (embedding <=> %s) AS similarity
        FROM issue_vectors
        ORDER BY embedding <=> %s
        LIMIT 3;
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, (embedding, embedding))
            results = cur.fetchall()
        return [
            {
                "id": row["id"],
                "issue_number": row["issue_number"],
                "text": row["text"],
                "similarity": row["similarity"],
            }
            for row in results
        ]
