import pytest
from unittest.mock import patch, MagicMock
from semver_tools.git_utils import GitUtils
from semver_tools.version_manager import VersionManager
from semver_tools.main import main 

@patch("semver_tools.main.GitUtils")
@patch("semver_tools.main.VersionManager")
@patch("sys.argv", ["main.py", "--repo-path", "."]) 
def test_main_no_tags(MockVersionManager, MockGitUtils, capsys):
    
    mock_git_utils = MagicMock(spec=GitUtils)
    MockGitUtils.return_value = mock_git_utils
    mock_git_utils.get_latest_tag.return_value = None
    mock_git_utils.get_current_branch.return_value = "develop"
    mock_git_utils.get_current_commit.return_value = "Initial commit"

    
    mock_version_manager = MagicMock(spec=VersionManager)
    MockVersionManager.return_value = mock_version_manager

    main()

    captured = capsys.readouterr()
    assert "No tags found, starting from 0.1.0" in captured.out
    mock_git_utils.create_tag.assert_called_once_with("0.1.0")


