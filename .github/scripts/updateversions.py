import json
import logging
import os

from typing import Set, Any

from github import Github

# Set up logging
logging.basicConfig(filename='versioning.log', level=logging.INFO)

# Load processed commits and current versions.
def load_processed_commits() -> Set[str]:
    try:
        with open('processed_commits.json', 'r') as file_obj:
            return set(json.load(file_obj))
    except FileNotFoundError:
        return set()

def save_processed_commits(commits_obj: Set[str]) -> None:
    with open('processed_commits.json', 'w') as file_obj:
        json.dump(list(commits_obj), file_obj, indent=4)

def is_file_modified_or_new(commit_obj: Any, file_path: str) -> bool:
    for file_obj in commit_obj.files:
        if file_obj.filename == file_path:
            if file_obj.status == "added" or (file_obj.status == "modified" and file_obj.patch):
                # Consider file as modified if it's newly added or has modifications with patch and status
                return True
            return False

class Versioning:
    def __init__(self):
        self.modified_files = None
        self.versions = None
        self.processed_commits = None
        self.pushed_commits = None
        self.g = None
        self.repo = None
        self.rate_limit = None

    def init(self) -> None:
        self.g = Github(os.getenv('GITHUB_TOKEN'))
        self.repo = self.g.get_repo(os.getenv('GITHUB_REPOSITORY'))

        try:
            self.pushed_commits = json.loads(os.getenv('PUSHED_COMMITS', '[]'))
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse PUSHED_COMMITS_JSON: {e}")
            self.pushed_commits = []

        self.rate_limit = self.g.get_rate_limit()
        logging.info(f"API Rate Limit Remaining: {self.rate_limit.core.remaining}")

    # Updates version and checks if the minor version is going to hit 100 if true resets to 0
    # andupdates major version
    def update_version(self, file_name: str) -> None:
        if file_name.endswith(('.js', '.py', '.html', '.css', '.txt', '.md', '.yml')):
            parts = self.versions.get(file_name, "0.0.0").split('.')
            minor_version = int(parts[-1]) + 1

            if minor_version == 100:
                parts[-1] = "0"
                parts[-2] = str(int(parts[-2]) + 1)
            else:
                parts[-1] = str(minor_version)

            self.versions[file_name] = '.'.join(parts)

    def process_commits(self) -> None:
        self.processed_commits = load_processed_commits()
        with open('versions.json', 'r') as file:
            self.versions = json.load(file)
        self.modified_files = set()

        for commit_data in self.pushed_commits:
            commit_sha = commit_data['id']
            commit = self.repo.get_commit(commit_sha)
            if commit_sha in self.processed_commits:
                continue

            all_files_processed_successfully = True
            # Mark commit as processed only if all files are successfully processed
            try:
                for file in commit.files:
                    if file.filename not in self.modified_files and is_file_modified_or_new(commit, file.filename):
                        logging.info(f"Processing file: {file.filename}")
                        self.update_version(file.filename)
                        self.modified_files.add(file.filename)
                    else:
                        all_files_processed_successfully = False  # Mark as false if any file fails to process
            except Exception as e:
                logging.error(f"Error processing commit {commit.sha}: {e}")
                all_files_processed_successfully = False  # Mark as false if an exception occurs

            if all_files_processed_successfully:
                self.processed_commits.add(commit.sha)

        if self.modified_files:
            with open('versions.json', 'w') as file:
                json.dump(self.versions, file, indent=4)
            save_processed_commits(self.processed_commits)

versioning = Versioning()
versioning.init()
versioning.process_commits()
