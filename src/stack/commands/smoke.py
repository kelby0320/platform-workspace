"""Smoke test command implementation."""

import subprocess
import time

import httpx
from rich.console import Console

from stack.config import get_platform_stack_path

console = Console()

BASE_URL = "http://localhost:8000/api/v1"
ASSISTANT_ID = "733750f6-66bb-4365-abcc-7ee1e989b339"


def smoke() -> None:
    """Run a smoke test of the entire stack."""
    stack_path = get_platform_stack_path()

    if not stack_path.exists():
        console.print(f"[red]Error: platform-stack not found at {stack_path}[/red]")
        console.print("Run 'stack clone' first to clone all repositories.")
        raise SystemExit(1)

    # Check if stack is up, bring it up if not
    stack_was_down = False
    if not _is_stack_up(stack_path):
        console.print("[yellow]Stack is not running. Starting it...[/yellow]")
        stack_was_down = True
        _bring_stack_up(stack_path)
        _wait_for_stack_ready()

    console.print("\n[bold]Running smoke test...[/bold]\n")

    success = False
    try:
        success = _run_smoke_test()
    except Exception as e:
        console.print(f"[red]Smoke test error: {e}[/red]")
        success = False

    if success:
        console.print("\n[bold green]Smoke test PASSED![/bold green]")
        if stack_was_down:
            console.print("[yellow]Bringing stack down...[/yellow]")
            _bring_stack_down(stack_path)
    else:
        console.print("\n[bold red]Smoke test FAILED![/bold red]")
        console.print("[yellow]Leaving stack up for debugging.[/yellow]")
        raise SystemExit(1)


def _is_stack_up(stack_path) -> bool:
    """Check if the docker compose stack is running."""
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", "compose.services.yaml", "ps", "-q"],
            cwd=stack_path,
            capture_output=True,
            text=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def _bring_stack_up(stack_path) -> None:
    """Start the docker compose stack."""
    cmd = ["docker", "compose", "-f", "compose.services.yaml", "up", "-d"]
    result = subprocess.run(
        cmd,
        cwd=stack_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        console.print(f"[red]Failed to start stack: {result.stderr}[/red]")
        raise SystemExit(1)


def _bring_stack_down(stack_path) -> None:
    """Stop the docker compose stack."""
    cmd = [
        "docker",
        "compose",
        "-f",
        "compose.services.yaml",
        "-f",
        "compose.infra.yaml",
        "down",
    ]
    subprocess.run(cmd, cwd=stack_path, capture_output=True, text=True)


def _wait_for_stack_ready(max_wait: int = 60) -> None:
    """Wait for the stack to be ready to accept requests."""
    console.print("Waiting for stack to be ready...", style="dim")

    start = time.time()
    while time.time() - start < max_wait:
        try:
            response = httpx.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                console.print("[green]Stack is ready![/green]")
                return
        except httpx.RequestError:
            pass
        time.sleep(2)

    console.print("[yellow]Warning: Stack may not be fully ready yet.[/yellow]")


def _run_smoke_test() -> bool:
    """Execute the smoke test workflow."""
    # Step 1: Create a new Chat Session
    console.print("[cyan]Step 1:[/cyan] Creating chat session...")

    try:
        response = httpx.post(
            f"{BASE_URL}/chat/sessions",
            json={
                "title": "Smoke Test Chat",
                "assistant_id": ASSISTANT_ID,
            },
            timeout=30,
        )
    except httpx.RequestError as e:
        console.print(f"[red]Failed to connect to API: {e}[/red]")
        return False

    if response.status_code != 200 and response.status_code != 201:
        console.print(f"[red]Failed to create session: {response.status_code}[/red]")
        console.print(response.text)
        return False

    session_data = response.json()
    session_id = session_data.get("id")
    console.print(f"  Session created: {session_id}")

    # Step 2: Send a Chat Turn
    console.print("[cyan]Step 2:[/cyan] Sending chat turn...")

    try:
        with httpx.stream(
            "POST",
            f"{BASE_URL}/chat/sessions/{session_id}/turns",
            json={"message": "What is 7 * 5? Response only with the answer."},
            timeout=60,
        ) as response:
            if response.status_code != 200:
                console.print(f"[red]Failed to send turn: {response.status_code}[/red]")
                return False

            full_response = ""
            for line in response.iter_lines():
                if not line:
                    continue

                # Parse SSE format
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if data:
                        try:
                            import json

                            event_data = json.loads(data)
                            if "content" in event_data:
                                full_response += event_data["content"]
                        except json.JSONDecodeError:
                            pass
                elif line.startswith("event:"):
                    event_type = line[6:].strip()
                    if event_type == "Done":
                        break

            console.print(f"  Response received: {full_response.strip()}")

            # Verify the response contains "35"
            if "35" in full_response:
                console.print("  [green]Response validation: PASSED[/green]")
                return True
            else:
                console.print(
                    f"  [red]Response validation: FAILED (expected '35')[/red]"
                )
                return False

    except httpx.RequestError as e:
        console.print(f"[red]Request failed: {e}[/red]")
        return False
