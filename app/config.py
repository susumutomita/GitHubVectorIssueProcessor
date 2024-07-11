"""
This module contains the Config class, responsible for loading and storing configuration
information from environment variables.
"""

import os

from dotenv import load_dotenv


class Config:
    """
    A class to load and store configuration information from environment variables.

    Attributes:
        github_token (str): GitHub API token.
        qd_api_key (str): Qdrant API key.
        qd_url (str): Qdrant URL.
        github_repo (str): GitHub repository name.
        issue_number (int): GitHub issue number.
        nomic_api_key (str): Nomic API key.
    """

    def __init__(self):
        """
        Initialize the Config class by loading environment variables.
        """
        print("設定の初期化を開始します...")
        self.load_env_variables()
        self.print_config_status()

    def load_env_variables(self):
        """
        Load environment variables from a .env file if not running in GitHub Actions.
        """
        if not os.getenv("GITHUB_ACTIONS"):
            load_dotenv()

        self.github_token = os.getenv("GITHUB_TOKEN")
        self.qd_api_key = os.getenv("QD_API_KEY")
        self.qd_url = os.getenv("QD_URL")
        self.github_repo = os.getenv("GITHUB_REPOSITORY")
        self.issue_number = os.getenv("GITHUB_EVENT_ISSUE_NUMBER")
        if self.issue_number:
            self.issue_number = int(self.issue_number)
        self.nomic_api_key = os.getenv("NOMIC_API_KEY")

    def print_config_status(self):
        """
        Print the status of the loaded configuration.
        """
        if self.github_token is None:
            print("GITHUB_TOKENが見つかりません ...")
        else:
            print("GITHUB_TOKENからトークンを正常に取得しました。")

        print("QD_API_KEYの状態:", "取得済み" if self.qd_api_key else "見つかりません")
        print("QD_URLの状態:", "取得済み" if self.qd_url else "見つかりません")
        print(
            "GITHUB_REPOSITORYの状態:",
            "取得済み" if self.github_repo else "見つかりません",
        )
        if self.issue_number:
            print(f"GITHUB_EVENT_ISSUE_NUMBER: {self.issue_number}")
        else:
            print("GITHUB_EVENT_ISSUE_NUMBERが見つかりません")

        if self.nomic_api_key is None:
            print("NOMIC_API_KEYが見つかりません ...")
        else:
            print("NOMIC_API_KEYからトークンを正常に取得しました。")
        print("設定の初期化が完了しました。")
