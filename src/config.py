import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        print("設定の初期化を開始します...")
        if not os.getenv("GITHUB_ACTIONS"):
            load_dotenv()

        self.github_token = os.getenv("GITHUB_TOKEN")
        if self.github_token is None:
            print("GITHUB_TOKENが見つかりません ...")
        else:
            print("GITHUB_TOKENからトークンを正常に取得しました。")

        self.qd_api_key = os.getenv("QD_API_KEY")
        print("QD_API_KEYの状態:", "取得済み" if self.qd_api_key else "見つかりません")

        self.qd_url = os.getenv("QD_URL")
        print("QD_URLの状態:", "取得済み" if self.qd_url else "見つかりません")

        self.github_repo = os.getenv("GITHUB_REPOSITORY")
        print(
            "GITHUB_REPOSITORYの状態:",
            "取得済み" if self.github_repo else "見つかりません",
        )

        self.issue_number = os.getenv("GITHUB_EVENT_ISSUE_NUMBER")
        if self.issue_number:
            self.issue_number = int(self.issue_number)
            print(f"GITHUB_EVENT_ISSUE_NUMBER: {self.issue_number}")
        else:
            print("GITHUB_EVENT_ISSUE_NUMBERが見つかりません")

        self.nomic_api_key = os.getenv("NOMIC_API_KEY")
        if self.nomic_api_key is None:
            print("NOMIC_API_KEYが見つかりません ...")
        else:
            print("NOMIC_API_KEYからトークンを正常に取得しました。")
        print("設定の初期化が完了しました。")
