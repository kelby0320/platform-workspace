"""Validate command implementation."""

import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

from stack.config import get_repos_config, get_workspace_root

console = Console()


def validate(full: bool = False) -> None:
    """Validate repositories by running build/format/lint/test.

    Args:
        full: If True, validate all repos. If False (default), only validate changed repos.
    """
    config = get_repos_config()
    repos = config.get("repos", {})
    workspace = get_workspace_root()

    if full:
        console.print("[bold]Running full validation on all repositories...[/bold]")
        repos_to_validate = list(repos.keys())
    else:
        console.print("[bold]Running quick validation on changed repositories...[/bold]")
        repos_to_validate = _get_changed_repos(repos, workspace)

        if not repos_to_validate:
            console.print("[green]No changed repositories found. Nothing to validate.[/green]")
            return

        console.print(f"\n[cyan]Changed repositories:[/cyan] {', '.join(repos_to_validate)}\n")

    results = {}
    for repo_key in repos_to_validate:
        repo_config = repos.get(repo_key)
        if not repo_config:
            continue

        relative_path = repo_config.get("path", f"../{repo_key}")
        repo_path = (workspace / relative_path).resolve()

        if not repo_path.exists():
            results[repo_key] = {"status": "missing", "details": "Repository not found"}
            continue

        console.print(f"\n[bold cyan]Validating {repo_key}...[/bold cyan]")
        results[repo_key] = _validate_repo(repo_path)

    _report_results(results)


def _get_changed_repos(repos: dict, workspace: Path) -> list[str]:
    """Get list of repositories with uncommitted changes."""
    changed = []

    for repo_key, repo_config in repos.items():
        relative_path = repo_config.get("path", f"../{repo_key}")
        repo_path = (workspace / relative_path).resolve()

        if not repo_path.exists():
            continue

        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stdout.strip():
                changed.append(repo_key)
        except subprocess.CalledProcessError:
            continue

    return changed


def _validate_repo(repo_path: Path) -> dict:
    """Run validation steps on a repository."""
    results = {
        "status": "success",
        "build": None,
        "format": None,
        "lint": None,
        "test": None,
    }

    validation_steps = [
        ("build", ["uv", "sync"]),
        ("format", ["uv", "run", "ruff", "format", "--check", "."]),
        ("lint", ["uv", "run", "ruff", "check", "."]),
        ("test", ["uv", "run", "pytest", "-q"]),
    ]

    # Check if it's a UV project
    if not (repo_path / "pyproject.toml").exists():
        results["status"] = "skipped"
        results["details"] = "Not a Python project (no pyproject.toml)"
        return results

    for step_name, cmd in validation_steps:
        console.print(f"  Running {step_name}...", style="dim")
        try:
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0:
                results[step_name] = "passed"
            else:
                results[step_name] = "failed"
                results["status"] = "failed"
                console.print(f"    [red]{step_name} failed[/red]")
                if result.stdout:
                    console.print(result.stdout, style="dim")
                if result.stderr:
                    console.print(result.stderr, style="dim red")
        except FileNotFoundError:
            results[step_name] = "skipped"
            console.print(f"    [yellow]{step_name} skipped (command not found)[/yellow]")
        except subprocess.TimeoutExpired:
            results[step_name] = "timeout"
            results["status"] = "failed"
            console.print(f"    [red]{step_name} timed out[/red]")

    return results


def _report_results(results: dict) -> None:
    """Report validation results in a table."""
    console.print("\n")
    table = Table(title="Validation Results")
    table.add_column("Repository", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Build")
    table.add_column("Format")
    table.add_column("Lint")
    table.add_column("Test")

    def status_style(status: str | None) -> str:
        if status == "passed":
            return "[green]✓[/green]"
        elif status == "failed":
            return "[red]✗[/red]"
        elif status == "skipped":
            return "[yellow]-[/yellow]"
        elif status == "timeout":
            return "[red]⏱[/red]"
        return "[dim]-[/dim]"

    for repo_key, result in results.items():
        overall = result.get("status", "unknown")
        if overall == "success":
            status_col = "[green]Success[/green]"
        elif overall == "failed":
            status_col = "[red]Failed[/red]"
        elif overall == "missing":
            status_col = "[red]Missing[/red]"
        elif overall == "skipped":
            status_col = "[yellow]Skipped[/yellow]"
        else:
            status_col = overall

        table.add_row(
            repo_key,
            status_col,
            status_style(result.get("build")),
            status_style(result.get("format")),
            status_style(result.get("lint")),
            status_style(result.get("test")),
        )

    console.print(table)

    # Summary
    total = len(results)
    success = sum(1 for r in results.values() if r.get("status") == "success")
    failed = sum(1 for r in results.values() if r.get("status") == "failed")

    console.print(f"\n[bold]Summary:[/bold] {success}/{total} passed, {failed} failed")

    if failed > 0:
        raise SystemExit(1)
