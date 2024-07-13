import pytest

from app.config import Config
from app.github_handler import GithubHandler


@pytest.fixture
def mock_github(mocker):
    return mocker.patch("app.github_handler.Github")


def test_create_labels(mock_github):
    config = Config()
    mock_repo = mock_github.return_value.get_repo.return_value
    github_handler = GithubHandler(config)
    github_handler.create_labels()
    mock_repo.create_label.assert_any_call(name="toxic", color="ff0000")
    mock_repo.create_label.assert_any_call(name="duplicated", color="708090")


def test_add_label(mock_github):
    config = Config()
    mock_issue = mock_github.return_value.get_repo.return_value.get_issue.return_value
    github_handler = GithubHandler(config)
    github_handler.add_label("test_label")
    mock_issue.add_to_labels.assert_called_once_with("test_label")


def test_close_issue(mock_github):
    config = Config()
    mock_issue = mock_github.return_value.get_repo.return_value.get_issue.return_value
    github_handler = GithubHandler(config)
    github_handler.close_issue()
    mock_issue.edit.assert_called_once_with(state="closed")


def test_add_comment(mock_github):
    config = Config()
    mock_issue = mock_github.return_value.get_repo.return_value.get_issue.return_value
    github_handler = GithubHandler(config)
    github_handler.add_comment("test_comment")
    mock_issue.create_comment.assert_called_once_with("test_comment")
