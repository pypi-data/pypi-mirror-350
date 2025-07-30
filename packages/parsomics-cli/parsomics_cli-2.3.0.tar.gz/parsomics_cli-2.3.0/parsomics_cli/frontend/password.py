from typing import Annotated
import typer
from rich import print

from parsomics_cli.frontend.helpers import (
    print_exception,
    print_failure,
    print_info,
    print_success,
    print_warning,
)
from parsomics_cli.backend.database.exc import (
    ContainerManagerException,
)
from parsomics_cli.backend.database.utils import ContainerManager

password_app = typer.Typer()
container_manager = ContainerManager()


@password_app.command("set")
def password_set():
    """
    Set the database password
    """
    password = typer.prompt(
        text="Password",
        confirmation_prompt=True,
        hide_input=True,
    )
    try:
        container_manager.set_password(password)
        print_success("Database password set")
        print_info("The password was saved, so you won't have to type it again")
    except ContainerManagerException as e:
        print_exception(e)
        print_failure("Database password not set")


@password_app.command("get")
def password_get():
    """
    Get the database password
    """
    try:
        print_warning("This will print your password in plain text.")
        confirm = typer.confirm("Print password?")
        if confirm:
            password = container_manager.get_password()
            print(f"Password: [bold bright_black]{password}[/bold bright_black]")
    except ContainerManagerException as e:
        print_exception(e)
