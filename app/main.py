"""
This module sets up the necessary components and processes GitHub issues using the Groq client,
Qdrant vector database, and other handlers.
"""

from app.config import load_env
from app.content_moderator import ContentModerator
from app.github_handler import GithubHandler
from app.groq_handler import GroqHandler
from app.issue_processor import IssueProcessor
from app.qdrant_handler import QdrantHandler


def setup():
    """
    Set up the necessary components for processing GitHub issues.

    Returns:
        tuple: A tuple containing the GitHub handler, content moderator, and Qdrant handler.
    """
    load_env()
    github_handler = GithubHandler()
    github_handler.create_labels()

    groq_handler = GroqHandler()
    groq_client = groq_handler.get_client()
    content_moderator = ContentModerator(groq_client)

    qdrant_handler = QdrantHandler(groq_client)

    return github_handler, content_moderator, qdrant_handler


def main():
    """
    Main function to process GitHub issues.
    """
    github_handler, content_moderator, qdrant_handler = setup()
    issue_processor = IssueProcessor(github_handler, content_moderator, qdrant_handler)
    issue_content = f"{github_handler.issue.title}\n{github_handler.issue.body}"
    issue_processor.process_opened_issue(issue_content)


def process_new_comment():
    """
    Function to process new comments on GitHub issues.
    """
    github_handler, content_moderator, qdrant_handler = setup()
    issue_processor = IssueProcessor(github_handler, content_moderator, qdrant_handler)
    comment_content = github_handler.issue.get_comments()[-1].body
    issue_processor.process_new_comment(comment_content)


if __name__ == "__main__":
    main()
