"""
This module processes GitHub issues, moderates their content,
and checks for duplicates using Qdrant.
"""


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

    def process_issue(self, issue_content: str):
        """
        Process the given GitHub issue content.

        Args:
            issue_content (str): The content of the GitHub issue.
        """
        if self.content_moderator.judge_violation(issue_content):
            self.handle_violation()
            return

        similar_issues = self.qdrant_handler.search_similar_issues(issue_content)
        if not similar_issues:
            self.qdrant_handler.add_issue(
                issue_content, self.github_handler.issue.number
            )
            return

        duplicate_id = self._check_duplication(issue_content, similar_issues)
        if duplicate_id:
            self._handle_duplication(duplicate_id)
        else:
            self.qdrant_handler.add_issue(
                issue_content, self.github_handler.issue.number
            )

    def handle_violation(self):
        """Handle issues with content violations."""
        self.github_handler.add_label("toxic")
        self.github_handler.add_comment(
            "不適切な投稿です。アカウントBANの危険性があります。"
        )
        self.github_handler.close_issue()

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
        self.github_handler.add_comment(f"#{duplicate_id} と重複しているかもしれません")

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
