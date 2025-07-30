import argparse
import os
from semver_tools.git_utils import GitUtils
from semver_tools.version_manager import VersionManager

def main():
    """
    Main entry point for the versioning tool.
    Handles version bumping, tagging, and writing to file.
    """
    parser = argparse.ArgumentParser(description='Semantic versioning tool for Git repositories')
    parser.add_argument('--repo-path', default=".", help='Path to the Git repository (default: current directory)')
    args = parser.parse_args()

    git_utils = GitUtils(args.repo_path)
    version_manager = VersionManager(args.repo_path)
    
    latest_tag = git_utils.get_latest_tag()
    current_branch = git_utils.get_current_branch()
    current_commit = git_utils.get_current_commit()
    if latest_tag is None:
        print(f"Branch: {current_branch}")
        print("No tags found, starting from 0.1.0")
        git_utils.create_tag("0.1.0")
        version_manager.write_version_to_file("0.1.0", os.path.join(args.repo_path, "version.env"))
        print(f"Created tag 0.1.0")
    else:
        version = version_manager.get_next_version(latest_tag, current_commit, current_branch)
        if current_branch in ["develop", "dev"] or current_branch.startswith("hotfix"):
            if git_utils.check_if_commit_is_tagged():
                print(f"Current commit is tagged, skipping tag creation")
                version_manager.write_version_to_file(version, os.path.join(args.repo_path, "version.env"))
            else:
                git_utils.create_tag(version)
                version_manager.write_version_to_file(version, os.path.join(args.repo_path, "version.env"))
                print(f"Created tag {version}")
        else:
            version_manager.write_version_to_file(version, os.path.join(args.repo_path, "version.env"))
            print(f"Current version: {version}")

def cli():
    """Entry point for the CLI"""
    main()

if __name__ == "__main__":
    main()