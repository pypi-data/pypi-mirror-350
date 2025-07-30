from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from parsomics_cli.frontend.analysis import analysis_run
from parsomics_cli.frontend.config import config_create, config_edit
from parsomics_cli.frontend.helpers import (
    print_exception,
    print_failure,
    print_info,
    print_success,
    print_warning,
)
from parsomics_cli.backend.database.exc import ContainerManagerException
from parsomics_cli.backend.database.utils import ContainerManager
from parsomics_cli.frontend.database import database_create, database_start
from parsomics_cli.frontend.password import password_set

setup_app = typer.Typer()
container_manager = ContainerManager()


def _print_step(n: int, description: str):
    print(f"\n• Step {n}: {description}")


@setup_app.command("start")
def setup_start():
    """
    Start a setup wizard
    """

    # TODO: check if container is already created. If it is, exit
    # TODO: stop setup in case of errors

    _print_step(1, "Ensure podman is available")
    try:
        # Check if podman is installed
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description="Checking podman installation...",
                total=None,
            )
            container_manager.check_podman_executable()
        print_success("Podman installed")

        # Check if podman is reachable
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description="Checking podman socket reachability...",
                total=None,
            )
            container_manager.check_podman_socket()
        print_success("Podman socket reachable")

    except ContainerManagerException as e:
        print_exception(e)

    _print_step(2, "Set a password for the database")
    password_set()

    _print_step(3, "Create and start the database")
    database_create()
    database_start()

    _print_step(4, "Create and edit the configuration file")
    config_create()
    edit = typer.confirm("Do you want to edit the configuration file?")
    if edit:
        config_edit()

    _print_step(5, "Run the parsomics analysis")
    edit = typer.confirm("Do you want to run the parsomics analysis?")
    if edit:
        analysis_run()
