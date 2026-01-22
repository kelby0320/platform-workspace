"""Stack management CLI entry point."""

from typing import Annotated

import typer

from stack.commands.clone import clone as clone_cmd
from stack.commands.down import down as down_cmd
from stack.commands.logs import logs as logs_cmd
from stack.commands.smoke import smoke as smoke_cmd
from stack.commands.up import up as up_cmd
from stack.commands.validate import validate as validate_cmd

app = typer.Typer(
    name="stack",
    help="Stack management CLI for platform workspace.",
    no_args_is_help=True,
)


@app.command()
def clone() -> None:
    """Clone all repositories defined in repos.yaml."""
    clone_cmd()


@app.command()
def up(
    with_observability: Annotated[
        bool,
        typer.Option("--with-observability", help="Include observability infrastructure"),
    ] = False,
) -> None:
    """Start the stack using docker compose."""
    up_cmd(with_observability=with_observability)


@app.command()
def down() -> None:
    """Stop the stack using docker compose."""
    down_cmd()


@app.command()
def validate(
    quick: Annotated[
        bool,
        typer.Option("--quick", help="Run validation only on changed repos (default)"),
    ] = False,
    full: Annotated[
        bool,
        typer.Option("--full", help="Run validation on all repos"),
    ] = False,
) -> None:
    """Validate repositories by running build/format/lint/test."""
    # Default to quick if neither flag is specified
    if not quick and not full:
        quick = True

    # If both are specified, full takes precedence
    run_full = full

    validate_cmd(full=run_full)


@app.command()
def smoke() -> None:
    """Run a smoke test of the entire stack."""
    smoke_cmd()


@app.command()
def logs(
    service: Annotated[
        str,
        typer.Argument(help="Service to view logs for (pcp, aisp, or uip)"),
    ],
    follow: Annotated[
        bool,
        typer.Option("-f", "--follow", help="Follow log output"),
    ] = False,
) -> None:
    """View docker compose logs for a service."""
    logs_cmd(service=service, follow=follow)


if __name__ == "__main__":
    app()
