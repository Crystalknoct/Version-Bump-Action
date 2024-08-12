# Version-Bump-Bot
This will host a backup of the websites version bump bot and will be subject to change as the websites is as well.

As of August 12, 2024 current version of Version-Bump-Bot is: 0.60

For the Python script, the following functionality is as follows.

 ## Functionality and use cases of the given `Versioning` class:

1. **GitHub Integration**: The class is designed to interact with GitHub using the provided Github token to access
repositories, commits, and rate limits. This integration allows version management based on commit data.

2. **Loading and Saving Processed Commits**: The `load_processed_commits()` and
`save_processed_commits(commits_obj: Set[str])` functions are used to save and load the set of processed commits,
ensuring no duplicate processing. This feature helps maintain the efficiency and accuracy of version management.

3. **Checking File Modifications**: The `is_file_modified_or_new(commit_obj: Any, file_path: str)` function checks
if a given file is modified or new based on its status in the provided commit object. This functionality assists
in identifying which files need to be processed during version management.

4. **Versioning**: The `update_version(self, file_name: str)` method updates the minor and major versions based on
the given file name. When the minor version number reaches 100, it resets to 0, and the major version is
incremented if needed. This feature facilitates proper version management for files with specific extensions like
.js, .py, .html, etc.

5. **Processing Commits**: The `process_commits()` method processes all unprocessed commits by iterating through
the pushed commits and checking for file modifications or new files. During this process, versions are updated
based on the identified changes, ensuring consistent versioning across the repository.

6. **Logging**: Logging functionality is present in the script to keep track of important events like API rate
limit information, processing commit messages, and error messages during file processing. This feature helps
developers debug issues and monitor the progress of the versioning process.

7. **Dynamic Processing**: The class dynamically processes commits as they are pushed to the repository without
the need for manual intervention. This feature saves time and ensures that versions are updated as soon as new
modifications are made, maintaining an up-to-date versioning system.

8. **Handling Multiple Commits at Once**: The `process_commits()` method processes all unprocessed commits in
parallel, making it capable of handling multiple commits at once. This feature increases the efficiency and
productivity of the versioning process by minimizing the time required for processing individual commits
one-by-one.


As for the YAML script, the functionality is as follows.

 ## File Versioning Workflow: Overview and Use Cases

The provided YAML code defines a GitHub Action named `File Versioning` with the following functionality and use
cases:

1. **Trigger**: The workflow is triggered on a `push` event, making it suitable for updating file versions as soon
as new modifications are pushed to the repository.
2. **GitHub Integration**: The workflow includes the `secrets.GITHUB_TOKEN` variable which is used to authenticate
with GitHub API during versioning processing, ensuring that the script has access to required commit data.
3. **Processing Multiple Commits at Once**: The workflow collects all pushed commits in an event and processes
them in parallel as part of the `update-versions` job. This increases efficiency and productivity by handling
multiple commits simultaneously.
4. **Python Dependencies and Setup**: The workflow uses a Python script for versioning, ensuring that necessary
dependencies are available by installing them using pip.
5. **Versioning Script Execution**: The `updateversions.py` script is executed to perform file versioning based on
commit data. This includes processing each push commit, identifying file modifications or new files, and updating
the corresponding versions.
6. **Commit and Push Changes**: After successful execution of the versioning script, the updated `versions.json`
file is committed and pushed to the repository, ensuring that consistent and up-to-date versions are available for
all files in the repository.

The `File Versioning` workflow offers a dynamic and efficient solution for managing file versions by processing
multiple commits at once and integrating seamlessly with GitHub, providing a convenient and automated way to
manage version updates.
