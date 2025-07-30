import pytest
from unittest.mock import MagicMock, patch
from git import Repo
from semver_tools.git_utils import GitUtils
import os

@pytest.fixture
def mock_repo():
    """Fixture to mock the Repo object."""
    repo_mock = MagicMock(spec=Repo)
    repo_mock.active_branch.name = "main"
    repo_mock.head.commit.message = "Initial commit"
    repo_mock.tags = []
    return repo_mock

def test_get_current_branch(mock_repo):
    with patch("semver_tools.git_utils.Repo", return_value=mock_repo), \
        patch.dict(os.environ, {"GITHUB_REF": "refs/heads/main"}):
        git_utils = GitUtils()
        assert git_utils.get_current_branch() == "main"

def test_get_current_commit(mock_repo):
    with patch("semver_tools.git_utils.Repo", return_value=mock_repo):
        git_utils = GitUtils()
        assert git_utils.get_current_commit() == "Initial commit"

def test_get_latest_tag_no_tags(mock_repo):
    with patch("semver_tools.git_utils.Repo", return_value=mock_repo):
        git_utils = GitUtils()
        assert git_utils.get_latest_tag() is None

def test_create_tag(mock_repo):
    with patch("semver_tools.git_utils.Repo", return_value=mock_repo):
        git_utils = GitUtils()
        mock_repo.create_tag.return_value.name = "v1.0.0"
        git_utils.create_tag("v1.0.0")
        mock_repo.create_tag.assert_called_with("v1.0.0")
        mock_repo.remote(name="origin").push.assert_called()
