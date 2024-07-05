import os
from config import Config
from github_handler import GithubHandler
from content_moderator import ContentModerator
from handlers.qdrant_handler import QdrantHandler
from handlers.pgvector_handler import PgVectorHandler
from handlers.embedding_models import GroqModel
from issue_processor import IssueProcessor
from qdrant_client import QdrantClient
from groq import Groq


def setup():
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.create_labels()

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    embedding_model = GroqModel(client)

    if config.qd_url:
        qdrant_client = QdrantClient(url=config.qd_url, api_key=config.qd_api_key)
        vector_handler = QdrantHandler(qdrant_client, embedding_model)
    else:
        vector_handler = PgVectorHandler(config.db_connection_str, embedding_model)

    return (
        github_handler,
        ContentModerator(client),
        vector_handler,
        embedding_model,
    )


def main():
    github_handler, content_moderator, vector_handler, embedding_model = setup()
    issue_processor = IssueProcessor(
        github_handler, content_moderator, vector_handler, embedding_model
    )
    issue_content = f"{github_handler.issue.title}\n{github_handler.issue.body}"
    issue_processor.process_issue(issue_content)


if __name__ == "__main__":
    main()
