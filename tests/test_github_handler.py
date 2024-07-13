from unittest.mock import MagicMock

import pytest

from app.config import Config
from app.github_handler import GithubHandler


@pytest.fixture
def mock_github(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "fake_github_token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "fake_repository")
    monkeypatch.setenv("GITHUB_EVENT_ISSUE_NUMBER", "123")
    monkeypatch.setenv("NOMIC_API_KEY", "fake_nomic_api_key")
    monkeypatch.setenv("QD_API_KEY", "fake_qd_api_key")
    monkeypatch.setenv("QD_URL", "https://fake_qd_url")

    mock_github = MagicMock()
    monkeypatch.setattr("app.github_handler.Github", mock_github)
    return mock_github


def test_create_labels(mock_github):
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.create_labels()
    github_handler.repo.create_label.assert_any_call(name="toxic", color="ff0000")
    github_handler.repo.create_label.assert_any_call(name="duplicated", color="708090")


def test_add_label(mock_github):
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.add_label("test_label")
    github_handler.issue.add_to_labels.assert_called_with("test_label")


def test_close_issue(mock_github):
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.close_issue()
    github_handler.issue.edit.assert_called_with(state="closed")


def test_add_comment(mock_github):
    config = Config()
    github_handler = GithubHandler(config)
    github_handler.add_comment("test_comment")
    github_handler.issue.create_comment.assert_called_with("test_comment")
