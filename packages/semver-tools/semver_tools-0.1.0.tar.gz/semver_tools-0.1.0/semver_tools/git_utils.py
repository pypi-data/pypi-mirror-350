from os import getenv
from git import Repo
from semantic_version import Version

class GitUtils:
    """Utilities for interacting with a Git repository"""

    def __init__(self, repo_path="."):
        """
        Initialize the GitUtils class.
        
        :param repo_path: Path to the Git repository (default: current directory)
        """
        self.repo = Repo(repo_path)

    def get_current_branch(self):
        """
        Get the current branch name.
        
        :return: The name of the current branch.
        """
        return getenv("GITHUB_REF").replace("refs/heads/", "")
    
    def get_current_commit(self):
        """
        Get the current commit message.
        
        :return: The current commit message.
        """
        return self.repo.head.commit.message
    
    
    def check_if_commit_is_tagged(self):
        """
        Check if the current commit is tagged.
        
        :return: True if the current commit is tagged, False otherwise.
        """
        return any(tag.commit.hexsha == self.repo.head.commit.hexsha for tag in self.repo.tags)

    def get_latest_tag(self):
        """
        Get the latest semantic version tag in the current branch.
        
        :return: Latest tag (str) or None if no valid tags are found.
        """
        tags_in_branch = []
        for tag in self.repo.tags:
            if self.repo.git.merge_base('--is-ancestor', tag.commit.hexsha, self.repo.head.commit.hexsha, with_exception=False) == "":
                tags_in_branch.append(tag.name)
        if not tags_in_branch:
            return None
        latest_tag = sorted(tags_in_branch, key=Version)[-1]
        try:
            Version(latest_tag)
            return latest_tag
        except ValueError:
            return None

    def tag_exists(self, tag_name):
        """
        Check if a tag exists in the repository.
        
        :param tag_name: The tag name to check.
        :return: True if the tag exists, False otherwise.
        """
        return any(tag.name == tag_name for tag in self.repo.tags)

    def create_tag(self, tag_name):
        """
        Create a new Git tag and push it to the remote repository.
        
        :param tag_name: The tag name to create.
        """
        if self.tag_exists(tag_name):
            raise ValueError(f"Tag '{tag_name}' already exists.")
        tag = self.repo.create_tag(tag_name)
        self.repo.remote(name="origin").push(tag)

