from app.config import Config


def test_load_env_variables(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_github_token")
    monkeypatch.setenv("QD_API_KEY", "test_qd_api_key")
    monkeypatch.setenv("QD_URL", "test_qd_url")
    monkeypatch.setenv("GITHUB_REPOSITORY", "test_repo")
    monkeypatch.setenv("GITHUB_EVENT_ISSUE_NUMBER", "42")
    monkeypatch.setenv("NOMIC_API_KEY", "test_nomic_api_key")

    config = Config()
    assert config.github_token == "test_github_token"
    assert config.qd_api_key == "test_qd_api_key"
    assert config.qd_url == "test_qd_url"
    assert config.github_repo == "test_repo"
    assert config.issue_number == 42
    assert config.nomic_api_key == "test_nomic_api_key"
