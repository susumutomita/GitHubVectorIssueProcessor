"""
This module contains the GithubHandler class, responsible for interacting with the GitHub API
to manage issues and labels.
"""

from github import Github
from github.GithubException import GithubException, UnknownObjectException


class GithubHandler:
    """
    A handler class to manage GitHub issues and labels.

    Attributes:
        github (Github): An instance of the Github client.
        repo (Repository): The repository to interact with.
        issue (Issue): The issue to manage.
    """

    def __init__(self, config):
        """
        Initialize the GithubHandler with the given configuration.

        Args:
            config (Config): An instance of the Config class containing the GitHub token,
                             repository name, and issue number.
        """
        self.github = Github(config.github_token)
        self.repo = self.github.get_repo(config.github_repo)
        self.issue = self.repo.get_issue(config.issue_number)

    def create_labels(self):
        """
        Create labels for issues if they don't already exist.
        """
        try:
            self.repo.create_label(name="toxic", color="ff0000")
            self.repo.create_label(name="duplicated", color="708090")
        except UnknownObjectException:
            pass
        except GithubException as e:
            if "already_exists" in str(e):
                pass
            else:
                raise RuntimeError(f"Failed to create label: {e}") from e

    def add_label(self, label):
        """
        Add a label to the issue.

        Args:
            label (str): The label to add to the issue.
        """
        self.issue.add_to_labels(label)

    def close_issue(self):
        """
        Close the issue.
        """
        self.issue.edit(state="closed")

    def add_comment(self, comment):
        """
        Add a comment to the issue.

        Args:
            comment (str): The comment to add to the issue.
        """
        self.issue.create_comment(comment)