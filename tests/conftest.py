import pytest


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy_groq_api_key")
    monkeypatch.setenv("GITHUB_TOKEN", "dummy_github_token")
    monkeypatch.setenv("QD_API_KEY", "dummy_qd_api_key")
    monkeypatch.setenv("QD_URL", "https://dummy.qd.url")
    monkeypatch.setenv("GITHUB_REPOSITORY", "dummy_repo")
    monkeypatch.setenv("GITHUB_EVENT_ISSUE_NUMBER", "1")
    monkeypatch.setenv("NOMIC_API_KEY", "dummy_nomic_api_key")
