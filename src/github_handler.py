from github import Github


class GithubHandler:
    def __init__(self, config: Config):
        self.github = Github(config.github_token)
        self.repo = self.github.get_repo(config.github_repo)
        self.issue = self.repo.get_issue(config.issue_number)

    def create_labels(self):
        try:
            self.repo.create_label(name="toxic", color="ff0000")
            self.repo.create_label(name="duplicated", color="708090")
        except:
            pass

    def add_label(self, label: str):
        self.issue.add_to_labels(label)

    def close_issue(self):
        self.issue.edit(state="closed")

    def add_comment(self, comment: str):
        self.issue.create_comment(comment)
