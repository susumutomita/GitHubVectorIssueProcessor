from config import Config
from github_handler import GithubHandler
from content_moderator import ContentModerator
from qdrant_handler import QdrantHandler
from issue_processor import IssueProcessor
from groq import Groq
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os


def setup():
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.create_labels()

    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    content_moderator = ContentModerator(groq_client)

    qdrant_client = QdrantClient(url=config.qd_url, api_key=config.qd_api_key)
    try:
        qdrant_client.get_collection(collection_name="issue_collection")
    except Exception as e:
        print(f"Collection not found, creating a new one. Details: {e}")
        qdrant_client.create_collection(
            collection_name="issue_collection",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print("Collection 'issue_collection' created successfully.")

    qdrant_handler = QdrantHandler(qdrant_client, groq_client)

    return github_handler, content_moderator, qdrant_handler


def main():
    github_handler, content_moderator, qdrant_handler = setup()
    issue_processor = IssueProcessor(github_handler, content_moderator, qdrant_handler)
    issue_content = f"{github_handler.issue.title}\n{github_handler.issue.body}"
    issue_processor.process_issue(issue_content)


if __name__ == "__main__":
    main()
