import openai
from azure.ai.openai import OpenAIClient as AzureOpenAIClient
from qdrant_client import QdrantClient

from config import Config
from content_moderator import ContentModerator
from github_handler import GithubHandler
from handlers.embedding_models import AzureOpenAIModel, LocalModel, OpenAIModel
from handlers.pgvector_handler import PgVectorHandler
from handlers.qdrant_handler import QdrantHandler
from issue_processor import IssueProcessor


def setup():
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.create_labels()

    if config.ai_model_type == "openai":
        openai_client = openai.Client(api_key=config.openai_api_key)
        embedding_model = OpenAIModel(openai_client)
    elif config.ai_model_type == "azure":
        azure_client = AzureOpenAIClient(
            api_key=config.azure_api_key
        )  # Azureクライアントの初期化
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