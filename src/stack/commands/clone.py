"""Clone command implementation."""

import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from stack.config import get_repos_config, get_workspace_root

console = Console()


def clone() -> None:
    """Clone all repositories defined in repos.yaml."""
    config = get_repos_config()
    repos = config.get("repos", {})
    workspace = get_workspace_root()

    table = Table(title="Repository Status")
    table.add_column("Repository", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Path", style="dim")

    for repo_key, repo_config in repos.items():
        url = repo_config.get("url")
        relative_path = repo_config.get("path", f"../{repo_key}")
        repo_path = (workspace / relative_path).resolve()

        if repo_path.exists():
            table.add_row(repo_key, "Already exists", str(repo_path))
        else:
            console.print(f"Cloning {repo_key}...", style="yellow")
            try:
                result = subprocess.run(
                    ["git", "clone", url, str(repo_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                table.add_row(repo_key, "Cloned", str(repo_path))
            except subprocess.CalledProcessError as e:
                table.add_row(repo_key, f"[red]Failed: {e.stderr.strip()}[/red]", str(repo_path))

    console.print(table)
