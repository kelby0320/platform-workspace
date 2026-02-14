"""New-sprint command: archive current sprint and create a new one from template."""

import shutil
from datetime import datetime, timezone
from pathlib import Path

import typer
from rich.console import Console

from stack.config import get_workspace_root

console = Console()


def _find_current_sprint_file(state_dir: Path) -> Path | None:
    """Return the single state/sprint-*.md file, or None if not exactly one."""
    if not state_dir.is_dir():
        return None
    candidates = list(state_dir.glob("sprint-*.md"))
    if len(candidates) != 1:
        return None
    return candidates[0]


def new_sprint(sprint_name: str) -> None:
    """Archive the current sprint file and create a new one from the template."""
    workspace = get_workspace_root()
    state_dir = workspace / "state"
    archive_dir = state_dir / "archive"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    template_path = workspace / "templates" / "sprint.template.md"

    current_sprint = _find_current_sprint_file(state_dir)
    if current_sprint is None:
        console.print(
            "[red]Error: Could not find current sprint file. "
            "Expect exactly one file matching state/sprint-*.md to archive.[/red]"
        )
        raise typer.Exit(1)

    archived_sprint = archive_dir / current_sprint.name
    new_sprint_path = state_dir / f"sprint-{sprint_name}-{timestamp}.md"

    if not template_path.exists():
        console.print(
            f"[red]Error: Sprint template not found at {template_path.relative_to(workspace)}.[/red]"
        )
        raise typer.Exit(1)

    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        console.print(f"[red]Error: Could not create archive directory {archive_dir.relative_to(workspace)}: {e}[/red]")
        raise typer.Exit(1)

    try:
        shutil.move(str(current_sprint), str(archived_sprint))
    except OSError as e:
        console.print(
            f"[red]Error: Could not move {current_sprint.relative_to(workspace)} to archive: {e}[/red]"
        )
        raise typer.Exit(1)

    try:
        shutil.copy2(str(template_path), str(new_sprint_path))
    except OSError as e:
        console.print(
            f"[red]Error: Could not copy template to {new_sprint_path.relative_to(workspace)}: {e}[/red]"
        )
        raise typer.Exit(1)

    console.print(
        f"[green]Sprint archived to {archived_sprint.relative_to(workspace)}[/green]"
    )
    console.print(
        f"[green]New sprint created at {new_sprint_path.relative_to(workspace)}[/green]"
    )
