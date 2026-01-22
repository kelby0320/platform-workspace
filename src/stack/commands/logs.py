"""Logs command implementation."""

import subprocess
import sys

from rich.console import Console

from stack.config import get_platform_stack_path

console = Console()

# Map short names to docker compose service names in platform-stack
SERVICE_MAP = {
    "pcp": "platform-api",
    "aisp": "ai-orchestrator",
    "uip": "web-app",
}


def logs(service: str, follow: bool = False) -> None:
    """View docker compose logs for a service from platform-stack.

    Args:
        service: Service identifier (pcp, aisp, or uip)
        follow: If True, follow the logs output
    """
    if service not in SERVICE_MAP:
        console.print(f"[red]Unknown service: {service}[/red]")
        console.print(f"Valid services: {', '.join(SERVICE_MAP.keys())}")
        raise SystemExit(1)

    compose_service = SERVICE_MAP[service]
    stack_path = get_platform_stack_path()

    if not stack_path.exists():
        console.print(f"[red]Error: platform-stack not found at {stack_path}[/red]")
        console.print("Run 'stack clone' first to clone all repositories.")
        raise SystemExit(1)

    cmd = ["docker", "compose", "-f", "compose.services.yaml", "logs"]

    if follow:
        cmd.append("-f")

    cmd.append(compose_service)

    console.print(f"[dim]Running: {' '.join(cmd)} in {stack_path}[/dim]\n")

    # Use subprocess with no capture to stream output directly
    try:
        subprocess.run(cmd, cwd=stack_path, check=False)
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        sys.exit(0)
