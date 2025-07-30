import pytest
from unittest.mock import MagicMock
from semver_tools.version_manager import VersionManager

@pytest.fixture
def version_manager():
    return VersionManager()

def test_bump_major_version(version_manager):
    latest_version = "1.0.0"
    commit_messages = ["[major]"]
    assert version_manager.bump_version(latest_version, commit_messages) == "2.0.0"

def test_bump_minor_version(version_manager):
    latest_version = "1.0.0"
    commit_messages = ["[minor]"]
    assert version_manager.bump_version(latest_version, commit_messages) == "1.1.0"

def test_bump_patch_version(version_manager):
    latest_version = "1.0.0"
    commit_messages = ["Fix typo"]
    assert version_manager.bump_version(latest_version, commit_messages) == "1.0.1"

def test_hotfix_version(version_manager):
    latest_version = "1.0.0"
    commit_messages = ["[hotfix]"]
    result = version_manager.bump_version(latest_version, commit_messages)
    assert result.startswith("1.0.0+hotfix.")

def test_get_next_version_hotfix_branch(version_manager):
    latest_version = "1.0.0"
    commit_messages = ["[hotfix]"]
    branch_name = "hotfix/fix-crash"
    result = version_manager.get_next_version(latest_version, commit_messages, branch_name)
    assert result.startswith("1.0.0+hotfix.")

def test_write_version_to_file(version_manager, tmp_path):
    version = "1.0.0"
    file_path = tmp_path / "version.env"
    version_manager.write_version_to_file(version, file_path)
    with open(file_path, "r") as file:
        assert file.read().strip() == "VERSION=1.0.0"

def test_bump_version_all_cases(version_manager):
    assert version_manager.bump_version("1.0.0", ["[major]"]) == "2.0.0"
    assert version_manager.bump_version("1.0.0", ["[minor]"]) == "1.1.0"
    assert version_manager.bump_version("1.0.0", ["[hotfix]"]).startswith("1.0.0+hotfix")
    assert version_manager.bump_version("1.0.0", ["Some random commit"]) == "1.0.1"

def test_get_next_version_hotfix_branch(version_manager):
    result = version_manager.get_next_version("1.0.0", ["[hotfix]"], "hotfix/urgent-fix")
    assert result.startswith("1.0.0+hotfix")

def test_write_version_to_file_invalid_path(version_manager):
    with pytest.raises(OSError):
        version_manager.write_version_to_file("1.0.0", "/invalid_path/version.env")

