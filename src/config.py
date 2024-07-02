import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.qd_api_key = os.getenv("QD_API_KEY")
        self.qd_url = os.getenv("QD_URL")
        self.db_connection_str = os.getenv("DB_CONNECTION_STR")
        self.github_repo = os.getenv("GITHUB_REPOSITORY")
        self.issue_number = int(os.getenv("GITHUB_EVENT_ISSUE_NUMBER", 0))
        self.ai_model_type = os.getenv("AI_MODEL_TYPE", "openai")
        self.azure_api_key = os.getenv("AZURE_API_KEY")
        self.local_model_path = os.getenv("LOCAL_MODEL_PATH")
