from pathlib import Path

import git


def add_to_gitignore(file_path: str | Path) -> bool:
    """Add a file path to .gitignore. Creates .gitignore if it doesn't exist.

    Args:
        file_path (str | Path): Path to the file to be added to .gitignore

    Returns:
        bool: True if file was added, False if it was already in .gitignore

    """
    # Convert file_path to Path object if it's not already
    file_path = Path(file_path).resolve()

    # Try to find the git root directory
    try:
        repo = git.Repo(file_path.parent, search_parent_directories=True)
        git_root = Path(repo.git.rev_parse("--show-toplevel"))
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        # If not in a git repository, use the parent directory of the file
        git_root = file_path.parent

    # Path to .gitignore
    gitignore_path = git_root / ".gitignore"

    # Get path to add to .gitignore - make it relative to git root
    try:
        # This ensures we get a proper relative path from git root
        relative_path = file_path.relative_to(git_root)
        path_to_add = str(relative_path)
    except ValueError:
        # If the file is not within the git root directory
        # (shouldn't happen in normal cases, but just to be safe)
        path_to_add = str(file_path)

    # Create .gitignore if it doesn't exist
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write(f"{path_to_add}\n")
        return True

    # Check if the file is already in .gitignore
    with open(gitignore_path) as f:
        lines = [line.strip() for line in f.readlines()]

    # If the path is already in .gitignore, do nothing
    if path_to_add in lines:
        return False

    # Otherwise, add the path to .gitignore
    with open(gitignore_path, "a") as f:
        f.write(f"{path_to_add}\n")

    return True


def get_default_branch(repo_path: Path) -> str:
    """Get the default branch name of a Git repository if possible.

    Args:
        repo_path (Path): Path to the Git repository.

    Returns:
        str: The default branch name.

    """
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        default_branch = repo.remotes.origin.refs["HEAD"].reference.remote_head
        return default_branch
    except Exception:
        return "main"  # Fallback to main if unable to determine
