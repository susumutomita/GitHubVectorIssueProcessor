class IssueProcessor:
    def __init__(
        self, github_handler, content_moderator, vector_handler, openai_client
    ):
        self.github_handler = github_handler
        self.content_moderator = content_moderator
        self.vector_handler = vector_handler
        self.openai_client = openai_client

    def process_issue(self, issue_content: str):
        if self.content_moderator.judge_violation(issue_content):
            self._handle_violation()
            return

        similar_issues = self.vector_handler.search_similar_issues(issue_content)
        if not similar_issues:
            self.vector_handler.add_issue(
                issue_content, self.github_handler.issue.number
            )
            return

        duplicate_id = self._check_duplication(issue_content, similar_issues)
        if duplicate_id:
            self._handle_duplication(duplicate_id)
        else:
            self.vector_handler.add_issue(
                issue_content, self.github_handler.issue.number
            )

    def _handle_violation(self):
        self.github_handler.add_label("toxic")
        self.github_handler.add_comment(
            "不適切な投稿です。アカウントBANの危険性があります。"
        )
        self.github_handler.close_issue()

    def _check_duplication(self, issue_content: str, similar_issues):
        prompt = self._create_duplication_check_prompt(issue_content, similar_issues)
        completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=1024,
            messages=[{"role": "system", "content": prompt}],
        )
        review = completion.choices[0].message.content
        if ":" in review:
            review = review.split(":")[-1]
        return int(review) if review.isdecimal() and review != "0" else 0

    def _handle_duplication(self, duplicate_id: int):
        self.github_handler.add_label("duplicated")
        self.github_handler.add_comment(f"#{duplicate_id} と重複しているかもしれません")

    @staticmethod
    def _create_duplication_check_prompt(issue_content: str, similar_issues):
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
