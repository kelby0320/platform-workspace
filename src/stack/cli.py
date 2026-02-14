"""Stack management CLI entry point."""

from typing import Annotated

import typer

from stack.commands.clone import clone as clone_cmd
from stack.commands.down import down as down_cmd
from stack.commands.logs import logs as logs_cmd
from stack.commands.new_sprint import new_sprint as new_sprint_cmd
from stack.commands.prompt import prompt_impl as prompt_impl_cmd
from stack.commands.prompt import prompt_plan as prompt_plan_cmd
from stack.commands.smoke import smoke as smoke_cmd
from stack.commands.up import up as up_cmd
from stack.commands.validate import validate as validate_cmd

prompt_app = typer.Typer(help="Output planner or implementer prompt from templates.")

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


@app.command()
def new_sprint(
    sprint_name: Annotated[
        str,
        typer.Argument(help="Name of the sprint (e.g. 'foo' for sprint-foo.md)"),
    ],
) -> None:
    """Archive the current sprint file and create a new one from the template."""
    new_sprint_cmd(sprint_name)


@prompt_app.command("plan")
def prompt_plan() -> None:
    """Output the planner prompt template."""
    prompt_plan_cmd()


@prompt_app.command("impl")
def prompt_impl(
    work_item: Annotated[
        int,
        typer.Option("--work-item", help="Work item number (1-99)"),
    ],
) -> None:
    """Output the implementer prompt for a work item."""
    prompt_impl_cmd(work_item)


app.add_typer(prompt_app, name="prompt")


if __name__ == "__main__":
    app()
