import os
from config import Config
from github_handler import GithubHandler
from content_moderator import ContentModerator
from handlers.qdrant_handler import QdrantHandler
from handlers.pgvector_handler import PgVectorHandler
from handlers.embedding_models import OpenAIModel, AzureOpenAIModel, LocalModel
from openai import OpenAI
from issue_processor import IssueProcessor
from qdrant_client import QdrantClient


def setup():
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.create_labels()

    if config.ai_model_type == "openai":
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        embedding_model = OpenAIModel(openai_client)
    elif config.ai_model_type == "azure":
        azure_client = AzureOpenAIClient(
            api_key=os.getenv("AZURE_API_KEY"),
            api_version="2023-05-15",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
        embedding_model = AzureOpenAIModel(azure_client)
    elif config.ai_model_type == "local":
        embedding_model = LocalModel(config.local_model_path)
    else:
        raise ValueError("Unsupported AI model type")

    if config.qd_url:
        qdrant_client = QdrantClient(url=config.qd_url, api_key=config.qd_api_key)
        vector_handler = QdrantHandler(qdrant_client, embedding_model)
    else:
        vector_handler = PgVectorHandler(config.db_connection_str, embedding_model)

    return (
        github_handler,
        ContentModerator(openai_client),
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
