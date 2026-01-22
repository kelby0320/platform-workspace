"""Down command implementation."""

import subprocess

from rich.console import Console

from stack.config import get_platform_stack_path

console = Console()


def down() -> None:
    """Stop the stack using docker compose."""
    stack_path = get_platform_stack_path()

    if not stack_path.exists():
        console.print(f"[red]Error: platform-stack not found at {stack_path}[/red]")
        console.print("Run 'stack clone' first to clone all repositories.")
        raise SystemExit(1)

    console.print("Stopping stack...", style="yellow")
    cmd = [
        "docker", "compose",
        "-f", "compose.services.yaml",
        "-f", "compose.infra.yaml",
        "down"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=stack_path,
            capture_output=True,
            text=True,
            check=True,
        )
        console.print("[green]Stack stopped successfully![/green]")
        if result.stdout:
            console.print(result.stdout)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed to stop stack:[/red]")
        console.print(e.stderr)
        raise SystemExit(1)

    _report_stack_state(stack_path)


def _report_stack_state(stack_path) -> None:
    """Report the state of the docker compose stack."""
    console.print("\n[bold]Stack State:[/bold]")
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", "compose.services.yaml", "ps"],
            cwd=stack_path,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            console.print(result.stdout)
        else:
            console.print("No running containers.", style="dim")
        if result.stderr:
            console.print(result.stderr, style="dim")
    except subprocess.CalledProcessError as e:
        console.print(f"[yellow]Could not get stack state: {e}[/yellow]")
