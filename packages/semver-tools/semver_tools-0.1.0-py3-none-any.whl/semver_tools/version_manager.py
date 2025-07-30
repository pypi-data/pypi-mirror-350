from semantic_version import Version
from semver_tools.git_utils import GitUtils

class VersionManager:
    """Manages semantic versioning for a Git repository"""

    def __init__(self, repo_path="."):
        """
        Initialize the VersionManager.
        
        :param repo_path: Path to the Git repository.
        """
        self.git_utils = GitUtils(repo_path)

    def bump_version(self, latest_version, commit_messages, branch_name):
        """
        Determine the next version based on commit messages.
        
        :param latest_version: The current latest semantic version (str).
        :param commit_messages: A list of commit messages (list of str).
        :return: The next semantic version (str).
        """
        version = Version(latest_version)
        if "[major]" in commit_messages.lower() and branch_name in ["develop", "dev"]:
            print("Bumping major version")
            return str(version.next_major())
        elif "[minor]" in commit_messages.lower() and branch_name in ["develop", "dev"]:
            print("Bumping minor version")
            return str(version.next_minor())
        elif "[hotfix]" in commit_messages.lower() and branch_name.startswith("hotfix"):
            print("Bumping hotfix version")
            if version.build:
                try:
                    build_parts = list(version.build)
                    if build_parts[-1].isdigit():
                        current_number = int(build_parts[-1])
                        build_parts[-1] = str(current_number + 1) 
                except Exception as e:
                    print(f"Error bumping hotfix version: {e}")
            else:
                build_parts = ["hotfix", "1"]
            new_version = Version(
            major=version.major,
            minor=version.minor,
            patch=version.patch,
            prerelease=version.prerelease,
            build=tuple(build_parts)
        )
            return str(new_version)
        else:
            print("Bumping patch version")
            return str(version.next_patch())
        
    def get_next_version(self, latest_version, commit_messages, branch_name):
        """
        Get the next version based on commit messages and branch name.
        
        :param latest_version: The current latest semantic version (str).
        :param commit_messages: A list of commit messages (list of str).
        :param branch_name: The name of the current branch (str).
        :return: The next semantic version (str).
        """
        print(f"Branch name: {branch_name}")
        print(f"Commit messages: {commit_messages}")
        print(f"Latest version: {latest_version}")
        if "hotfix" in branch_name:
            print("Hotfix branch, creating hotfix tag")
            return self.bump_version(latest_version, commit_messages)
        elif branch_name not in ["dev", "develop"] or self.git_utils.check_if_commit_is_tagged():
            print("Not on dev or develop branch OR commit is tagged, skipping version bump")
            return latest_version
        else:
            print("Bumping version...")
            return self.bump_version(latest_version, commit_messages, branch_name)

    def write_version_to_file(self, version, file_path):
        """
        Write the version to a file.
        
        :param version: The version to write.
        :param file_path: Path to the file (default: version.env).
        """
        with open(file_path, "w") as f:
            f.write(f"VERSION={version}")
