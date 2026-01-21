"""Logs command implementation."""

import subprocess
import sys

from rich.console import Console

from stack.config import get_repo_path

console = Console()

# Map short names to repository keys
REPO_MAP = {
    "pcp": "pcp",
    "aisp": "aisp",
    "uip": "uip",
}


def logs(service: str, follow: bool = False) -> None:
    """View docker compose logs for a service.

    Args:
        service: Service identifier (pcp, aisp, or uip)
        follow: If True, follow the logs output
    """
    if service not in REPO_MAP:
        console.print(f"[red]Unknown service: {service}[/red]")
        console.print(f"Valid services: {', '.join(REPO_MAP.keys())}")
        raise SystemExit(1)

    repo_key = REPO_MAP[service]

    try:
        repo_path = get_repo_path(repo_key)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)

    if not repo_path.exists():
        console.print(f"[red]Error: Repository not found at {repo_path}[/red]")
        console.print("Run 'stack clone' first to clone all repositories.")
        raise SystemExit(1)

    # Check for docker-compose.yaml or compose.yaml
    compose_file = None
    for filename in ["compose.yaml", "compose.yml", "docker-compose.yaml", "docker-compose.yml"]:
        if (repo_path / filename).exists():
            compose_file = filename
            break

    cmd = ["docker", "compose"]
    if compose_file:
        cmd.extend(["-f", compose_file])

    cmd.append("logs")

    if follow:
        cmd.append("-f")

    console.print(f"[dim]Running: {' '.join(cmd)} in {repo_path}[/dim]\n")

    # Use subprocess with no capture to stream output directly
    try:
        subprocess.run(cmd, cwd=repo_path, check=False)
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        sys.exit(0)
