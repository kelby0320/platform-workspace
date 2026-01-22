"""Configuration loading utilities."""

from pathlib import Path

import yaml


def get_workspace_root() -> Path:
    """Get the workspace root directory (platform-workspace)."""
    current = Path(__file__).resolve()
    # Navigate up from src/stack/config.py to workspace
    return current.parent.parent.parent


def get_repos_config() -> dict:
    """Load and return the repos.yaml configuration."""
    workspace = get_workspace_root()
    repos_yaml = workspace / "repos.yaml"

    if not repos_yaml.exists():
        raise FileNotFoundError(f"repos.yaml not found at {repos_yaml}")

    with open(repos_yaml) as f:
        return yaml.safe_load(f)


def get_repo_path(repo_key: str) -> Path:
    """Get the absolute path for a repository."""
    config = get_repos_config()
    repos = config.get("repos", {})

    if repo_key not in repos:
        raise ValueError(f"Unknown repository: {repo_key}")

    repo_config = repos[repo_key]
    relative_path = repo_config.get("path", f"../{repo_key}")

    workspace = get_workspace_root()
    return (workspace / relative_path).resolve()


def get_platform_stack_path() -> Path:
    """Get the path to the platform-stack repository."""
    return get_repo_path("stack")
