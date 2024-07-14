from unittest.mock import MagicMock, patch


from app.github_handler import GithubHandler


@patch("app.github_handler.Github")
def test_create_labels(mock_github):
    # Mock the necessary GitHub objects and methods
    mock_repo = MagicMock()
    mock_github_instance = mock_github.return_value
    mock_github_instance.get_repo.return_value = mock_repo

    # Create GithubHandler instance
    handler = GithubHandler()

    # Call the method and verify the expected interactions
    handler.create_labels()
    mock_repo.create_label.assert_any_call(name="toxic", color="ff0000")
    mock_repo.create_label.assert_any_call(name="duplicated", color="708090")


@patch("app.github_handler.Github")
def test_add_label(mock_github):
    # Mock the necessary GitHub objects and methods
    mock_issue = MagicMock()
    mock_repo = MagicMock()
    mock_github_instance = mock_github.return_value
    mock_github_instance.get_repo.return_value = mock_repo
    mock_repo.get_issue.return_value = mock_issue

    # Create GithubHandler instance
    handler = GithubHandler()

    # Call add_label and verify the expected interactions
    handler.add_label("toxic")
    mock_issue.add_to_labels.assert_called_once_with("toxic")


@patch("app.github_handler.Github")
def test_close_issue(mock_github):
    # Mock the necessary GitHub objects and methods
    mock_issue = MagicMock()
    mock_repo = MagicMock()
    mock_github_instance = mock_github.return_value
    mock_github_instance.get_repo.return_value = mock_repo
    mock_repo.get_issue.return_value = mock_issue

    # Create GithubHandler instance
    handler = GithubHandler()

    # Call close_issue and verify the expected interactions
    handler.close_issue()
    mock_issue.edit.assert_called_once_with(state="closed")


@patch("app.github_handler.Github")
def test_add_comment(mock_github):
    # Mock the necessary GitHub objects and methods
    mock_issue = MagicMock()
    mock_repo = MagicMock()
    mock_github_instance = mock_github.return_value
    mock_github_instance.get_repo.return_value = mock_repo
    mock_repo.get_issue.return_value = mock_issue

    # Create GithubHandler instance
    handler = GithubHandler()

    # Call add_comment and verify the expected interactions
    handler.add_comment("This is a test comment.")
    mock_issue.create_comment.assert_called_once_with("This is a test comment.")
