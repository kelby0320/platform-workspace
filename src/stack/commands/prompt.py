"""Prompt command: output planner or implementer prompts from templates."""

import re
from pathlib import Path

import typer
from jinja2 import Template
from rich.console import Console

from stack.config import get_workspace_root

console = Console()


def prompt_plan() -> None:
    """Output the planner prompt template contents."""
    workspace = get_workspace_root()
    template_path = workspace / "templates" / "prompts" / "planner.template.md"

    if not template_path.exists():
        console.print(
            f"[red]Error: Planner template not found at {template_path.relative_to(workspace)}.[/red]"
        )
        raise typer.Exit(1)

    try:
        text = template_path.read_text()
    except OSError as e:
        console.print(f"[red]Error: Could not read planner template: {e}[/red]")
        raise typer.Exit(1)

    print(text, end="")


def _find_current_sprint_file(workspace: Path) -> Path | None:
    """Return the single state/sprint-*.md file, or None if not exactly one."""
    state_dir = workspace / "state"
    if not state_dir.is_dir():
        return None
    candidates = list(state_dir.glob("sprint-*.md"))
    if len(candidates) != 1:
        return None
    return candidates[0]


def _get_repo_for_work_item(sprint_path: Path, work_item_number: str) -> str | None:
    """Find ' - Repo: <name>' on the line following '### WI-<work_item_number>'."""
    try:
        content = sprint_path.read_text()
    except OSError:
        return None

    header = f"### WI-{work_item_number}"
    idx = content.find(header)
    if idx == -1:
        return None

    rest = content[idx:]
    lines = rest.splitlines()
    if len(lines) < 2:
        return None

    # First line is the ### WI-xx header; second should be " - Repo: <name>" or "- Repo: <name>"
    repo_line = lines[1].strip()
    match = re.match(r"^\-?\s*Repo:\s*(.+)$", repo_line, re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip()


def prompt_impl(work_item: int) -> None:
    """Output the implementer prompt for the given work item (Jinja-rendered template)."""
    if not (1 <= work_item <= 99):
        console.print("[red]Error: --work-item must be a number between 1 and 99.[/red]")
        raise typer.Exit(1)

    work_item_number = f"{work_item:02d}"
    workspace = get_workspace_root()
    state_dir = workspace / "state"
    sprint_path = _find_current_sprint_file(workspace)

    if sprint_path is None:
        console.print(
            "[red]Error: Could not find current sprint file. "
            "Expect exactly one file matching state/sprint-*.md.[/red]"
        )
        raise typer.Exit(1)

    repo_name = _get_repo_for_work_item(sprint_path, work_item_number)
    if repo_name is None:
        console.print(
            f"[red]Error: Could not find '### WI-{work_item_number}' and following "
            "' - Repo: <name>' in {0}.[/red]".format(sprint_path.relative_to(workspace))
        )
        raise typer.Exit(1)

    template_path = workspace / "templates" / "prompts" / "implementer.template.md"
    if not template_path.exists():
        console.print(
            f"[red]Error: Implementer template not found at {template_path.relative_to(workspace)}.[/red]"
        )
        raise typer.Exit(1)

    try:
        template_content = template_path.read_text()
    except OSError as e:
        console.print(f"[red]Error: Could not read implementer template: {e}[/red]")
        raise typer.Exit(1)

    try:
        template = Template(template_content)
        rendered = template.render(WI_NUMBER=work_item_number, REPO_NAME=repo_name)
    except Exception as e:
        console.print(f"[red]Error: Failed to render implementer template: {e}[/red]")
        raise typer.Exit(1)

    print(rendered, end="")
