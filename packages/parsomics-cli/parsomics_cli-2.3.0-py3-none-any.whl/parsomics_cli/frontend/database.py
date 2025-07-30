import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from parsomics_cli.frontend.helpers import (
    print_exception,
    print_failure,
    print_info,
    print_success,
    print_warning,
)
from parsomics_cli.backend.database.exc import (
    ContainerDoesNotExist,
    ContainerIsRunning,
    ContainerManagerException,
)
from parsomics_cli.backend.database.types import DatabaseStatus
from parsomics_cli.backend.database.utils import ContainerManager

from .password import password_app


database_app = typer.Typer()
container_manager = ContainerManager()

database_app.add_typer(
    password_app, name="password", help="Manage the database password"
)


@database_app.command("status")
def database_status():
    """
    Get the status of the database
    """
    try:
        status = container_manager.get_status()
        match status:
            case DatabaseStatus.UNKNOWN:
                print("Database status [bold red]unknown[/bold red].")
            case DatabaseStatus.NOT_CREATED:
                print("Database [bold red]not created[/bold red].")
            case DatabaseStatus.NOT_RUNNING:
                print("Database is [bold yellow]not running[/bold yellow].")
            case DatabaseStatus.RUNNING:
                print("Database is [bold green]running[/bold green].")
    except ContainerManagerException as e:
        print_exception(e)


@database_app.command("create")
def database_create():
    """
    Create the database
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Creating database...", total=None)
            container_manager.create_container()
        print_success("Database created")
    except ContainerManagerException as e:
        print_exception(e)
        print_failure("Database not created")


@database_app.command("delete")
def database_delete():
    """
    Delete the database
    """
    try:
        container_manager.check_container_deletable()
    except ContainerIsRunning as e:
        print_exception(e)
        stop = typer.confirm("Stop database?")
        if stop:
            database_stop()
        else:
            print_info("Database deletion aborted")
            return
    except ContainerManagerException as e:
        print_exception(e)
        print_failure("Database not deleted")
        return

    print_warning("This will erase all the data in your database")
    delete = typer.confirm("Delete database?")
    if delete:
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Deleting database...", total=None)
                container_manager.delete_container()
            print_success("Database deleted")
        except ContainerManagerException as e:
            print_exception(e)
            print_failure("Database not deleted")
    else:
        print_info("Database deletion aborted")


@database_app.command("start")
def database_start(iteration: int = 1):
    """
    Start the database process
    """
    # Safeguard against infinite recursion
    if iteration > 2:
        print("[bold]Multiple attempts to stop the database have failed.[/bold]")
        print_failure("Database not started")
        return

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Starting database...", total=None)
            container_manager.start_container()
        print_success("Database started")
    except ContainerDoesNotExist as e:
        print_exception(e)
        create = typer.confirm("Create database?", default=True)
        if create:
            database_create()
            database_start(iteration=iteration + 1)
        else:
            print_info("Database creation aborted")

    except ContainerIsRunning:
        print_info("Database is already running")

    except ContainerManagerException as e:
        print_exception(e)
        print_failure("Database not started")


@database_app.command("stop")
def database_stop():
    """
    Stop the database process
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Stopping database...", total=None)
            container_manager.stop_container()
        print_success("Database stopped")
    except ContainerManagerException as e:
        print_exception(e)
        print_failure("Database not stopped")
