"""
This module processes GitHub issues, moderates their content,
and checks for duplicates using Qdrant.
"""

import logging

logger = logging.getLogger(__name__)


class IssueProcessor:
    """
    Class to handle the processing of GitHub issues.

    Attributes:
        github_handler (GithubHandler): An instance of the GithubHandler class.
        content_moderator (ContentModerator): An instance of the ContentModerator class.
        qdrant_handler (QdrantHandler): An instance of the QdrantHandler class.
    """

    def __init__(self, github_handler, content_moderator, qdrant_handler):
        """
        Initialize the IssueProcessor with required handlers.

        Args:
            github_handler (GithubHandler): An instance of the GithubHandler class.
            content_moderator (ContentModerator): An instance of the ContentModerator class.
            qdrant_handler (QdrantHandler): An instance of the QdrantHandler class.
        """
        self.github_handler = github_handler
        self.content_moderator = content_moderator
        self.qdrant_handler = qdrant_handler

    def process_opened_issue(self, issue_content: str):
        """
        Process the given GitHub issue content when the issue is opened.

        Args:
            issue_content (str): The content of the GitHub issue.
        """
        similar_issues = self.qdrant_handler.search_similar_issues(issue_content)
        if not similar_issues:
            self.qdrant_handler.add_issue(
                issue_content, self.github_handler.issue.number
            )
            logger.info("No similar issues found. Issue added to Qdrant.")
            return

        duplicate_id = self._check_duplication(issue_content, similar_issues)
        if duplicate_id:
            self._handle_duplication(duplicate_id)
            logger.info(
                "Issue marked as duplicated and closed. Duplicate ID: %s", duplicate_id
            )
        else:
            self.qdrant_handler.add_issue(
                issue_content, self.github_handler.issue.number
            )
            logger.info("No duplication found. Issue added to Qdrant.")

    def process_new_comment(self, comment_content: str):
        """
        Process the given GitHub issue comment content.

        Args:
            comment_content (str): The content of the GitHub issue comment.
        """
        if self.content_moderator.judge_violation(comment_content):
            self.handle_violation(comment_content)
            logger.info("Comment marked as toxic and rephrased.")

    def handle_violation(self, comment_content: str):
        """Handle comments with content violations."""
        rephrased_content = self.content_moderator.rephrase_inappropriate_comment(
            comment_content
        )
        self.github_handler.add_label("toxic")
        self.github_handler.add_comment(
            f"元のコメントが不適切なため、以下のように修正しました:\n\n{rephrased_content}"
        )
        self.github_handler.issue.edit(body=rephrased_content)

    def _check_duplication(self, issue_content: str, similar_issues):
        """
        Check for duplicate issues using the content and similar issues.

        Args:
            issue_content (str): The content of the GitHub issue.
            similar_issues (list): A list of similar issues.

        Returns:
            int: The ID of the duplicate issue if found, else 0.
        """
        prompt = self._create_duplication_check_prompt(issue_content, similar_issues)
        response = self.qdrant_handler.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            max_tokens=1024,
            messages=[{"role": "system", "content": prompt}],
        )
        review = response.choices[0].message.content
        if ":" in review:
            review = review.split(":")[-1]
        return int(review) if review.isdecimal() and review != "0" else 0

    def _handle_duplication(self, duplicate_id: int):
        """
        Handle duplicate issues by adding a label and a comment.

        Args:
            duplicate_id (int): The ID of the duplicate issue.
        """
        self.github_handler.add_label("duplicated")
        duplicate_issue_url = (
            f"https://github.com/{self.github_handler.repo.full_name}/issues/"
            f"{duplicate_id}"
        )
        self.github_handler.add_comment(
            f"#{duplicate_id} と重複しているかもしれません。"
            f"詳細は次のURLを参照してください: {duplicate_issue_url}"
        )

    @staticmethod
    def _create_duplication_check_prompt(issue_content: str, similar_issues):
        """
        Create a prompt for checking duplicate issues.

        Args:
            issue_content (str): The content of the GitHub issue.
            similar_issues (list): A list of similar issues.

        Returns:
            str: The prompt to be used for checking duplicates.
        """
        similar_issues_text = "\n".join(
            [f'id:{issue.id}\n内容:{issue.payload["text"]}' for issue in similar_issues]
        )
        return f"""
            以下はこのレポジトリに寄せられた改善提案です。
            {issue_content}
            この投稿を読み、以下の過去提案の中に重複する提案があるかを判断してください。
            {similar_issues_text}
            重複する提案があればそのidを出力してください。
            もし存在しない場合は0と出力してください。

            [出力形式]
            id:0
            """
