"""
This module contains the Config class, responsible for loading and storing configuration
information from environment variables.
"""

import os

from dotenv import load_dotenv


class Config:
    """
    A class to load and store configuration information from environment variables.
    """

    def __init__(self, env_file=".env", lang="en"):
        """
        Initialize the Config class by loading environment variables from a .env file if provided.

        Args:
            env_file (str): Path to the .env file.
            lang (str): Language for messages ("en" or "jp").
        """
        self.lang = lang
        self.messages = {
            "en": {
                "init_start": "Starting initialization...",
                "github_token_not_found": "GITHUB_TOKEN not found...",
                "github_token_found": "GITHUB_TOKEN successfully retrieved.",
                "qd_api_key_status": "QD_API_KEY status:",
                "qd_url_status": "QD_URL status:",
                "repo_status": "GITHUB_REPOSITORY status:",
                "issue_number": "GITHUB_EVENT_ISSUE_NUMBER:",
                "issue_number_not_found": "GITHUB_EVENT_ISSUE_NUMBER not found",
                "nomic_api_key_not_found": "NOMIC_API_KEY not found...",
                "nomic_api_key_found": "NOMIC_API_KEY successfully retrieved.",
                "init_complete": "Initialization complete.",
                "missing_vars": "Missing required environment variables: {}",
            },
            "jp": {
                "init_start": "設定の初期化を開始します...",
                "github_token_not_found": "GITHUB_TOKENが見つかりません ...",
                "github_token_found": "GITHUB_TOKENからトークンを正常に取得しました。",
                "qd_api_key_status": "QD_API_KEYの状態:",
                "qd_url_status": "QD_URLの状態:",
                "repo_status": "GITHUB_REPOSITORYの状態:",
                "issue_number": "GITHUB_EVENT_ISSUE_NUMBER:",
                "issue_number_not_found": "GITHUB_EVENT_ISSUE_NUMBERが見つかりません",
                "nomic_api_key_not_found": "NOMIC_API_KEYが見つかりません ...",
                "nomic_api_key_found": "NOMIC_API_KEYからトークンを正常に取得しました。",
                "init_complete": "設定の初期化が完了しました。",
                "missing_vars": "必要な環境変数が不足しています: {}",
            },
        }
        print(self.messages[self.lang]["init_start"])
        if os.path.exists(env_file):
            load_dotenv(env_file)
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.qd_api_key = os.getenv("QD_API_KEY")
        self.qd_url = os.getenv("QD_URL")
        self.github_repo = os.getenv("GITHUB_REPOSITORY")
        self.issue_number = os.getenv("GITHUB_EVENT_ISSUE_NUMBER")
        if self.issue_number:
            self.issue_number = int(self.issue_number)
        self.nomic_api_key = os.getenv("NOMIC_API_KEY")
        self.print_config_status()
        self.validate()

    def print_config_status(self):
        """
        Print the status of the loaded configuration.
        """
        if self.github_token is None:
            print(self.messages[self.lang]["github_token_not_found"])
        else:
            print(self.messages[self.lang]["github_token_found"])

        print(
            self.messages[self.lang]["qd_api_key_status"],
            "取得済み" if self.qd_api_key else "見つかりません",
        )
        print(
            self.messages[self.lang]["qd_url_status"],
            "取得済み" if self.qd_url else "見つかりません",
        )
        print(
            self.messages[self.lang]["repo_status"],
            "取得済み" if self.github_repo else "見つかりません",
        )
        if self.issue_number:
            print(f"{self.messages[self.lang]['issue_number']} {self.issue_number}")
        else:
            print(self.messages[self.lang]["issue_number_not_found"])

        if self.nomic_api_key is None:
            print(self.messages[self.lang]["nomic_api_key_not_found"])
        else:
            print(self.messages[self.lang]["nomic_api_key_found"])
        print(self.messages[self.lang]["init_complete"])

    def validate(self):
        """
        Validate the loaded configuration and ensure all required variables are set.
        """
        missing_vars = []
        if not self.github_token:
            missing_vars.append("GITHUB_TOKEN")
        if not self.qd_api_key:
            missing_vars.append("QD_API_KEY")
        if not self.qd_url:
            missing_vars.append("QD_URL")
        if not self.github_repo:
            missing_vars.append("GITHUB_REPOSITORY")
        if not self.issue_number:
            missing_vars.append("GITHUB_EVENT_ISSUE_NUMBER")
        if not self.nomic_api_key:
            missing_vars.append("NOMIC_API_KEY")

        if missing_vars:
            raise ValueError(
                self.messages[self.lang]["missing_vars"].format(", ".join(missing_vars))
            )
