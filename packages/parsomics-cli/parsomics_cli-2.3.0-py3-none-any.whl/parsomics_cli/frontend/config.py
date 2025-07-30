from pathlib import Path
from typing import Annotated

import typer

from parsomics_cli.frontend.helpers import print_exception, print_failure, print_success
from parsomics_cli.backend.config.exc import ConfigurationManagerException
from parsomics_cli.backend.config.types import Scope
from parsomics_cli.backend.config.utils import ConfigurationManager

from rich.prompt import Prompt
from rich import print

config_app = typer.Typer()
config_manager = ConfigurationManager()


@config_app.command("create")
def config_create(
    scope: Scope = Scope.USER,
    path: str | None = typer.Argument(
        default=None, help='Path to configuration file (if scope is "custom")'
    ),
):
    """
    Create a configuration file
    """
    try:
        match scope:
            case Scope.USER:
                config_manager.create_user_config()

            case Scope.SYSTEM:
                config_manager.create_system_config()

            case Scope.CUSTOM:
                if path is None:
                    path = Prompt.ask("Path")
                _path: Path = Path(path)
                config_manager.create_custom_config(_path)

        print_success("Config file created")

    except ConfigurationManagerException as e:
        print_exception(e)
        print_failure("Config file not created")


@config_app.command("view")
def config_view(
    scope: Scope = Scope.USER,
    path: str | None = typer.Argument(
        default=None, help='Path to configuration file (if scope is "custom")'
    ),
):
    """
    View a configuration file
    """
    try:
        match scope:
            case Scope.USER:
                config_manager.view_user_config()

            case Scope.SYSTEM:
                config_manager.view_system_config()

            case Scope.CUSTOM:
                if path is None:
                    path = Prompt.ask("Path")
                _path: Path = Path(path)
                config_manager.view_custom_config(_path)

    except ConfigurationManagerException as e:
        print_exception(e)


@config_app.command("edit")
def config_edit(
    scope: Scope = Scope.USER,
    path: str | None = typer.Argument(
        default=None, help='Path to configuration file (if scope is "custom")'
    ),
):
    """
    Edit a configuration file
    """
    try:
        match scope:
            case Scope.USER:
                config_manager.edit_user_config()

            case Scope.SYSTEM:
                config_manager.edit_system_config()

            case Scope.CUSTOM:
                if path is None:
                    path = Prompt.ask("Path")
                _path: Path = Path(path)
                config_manager.edit_custom_config(_path)

    except ConfigurationManagerException as e:
        print_exception(e)


@config_app.command("locate")
def config_locate(
    scope: Scope = Scope.USER,
    show_scope: Annotated[bool, typer.Option("--show-scope/--hide-scope")] = True,
):
    """
    Locate a configuration file
    """
    try:
        location = config_manager.locate_config(scope)
        print(f"{location}")
        if show_scope:
            print(f"(scope={scope.value})")
    except ConfigurationManagerException as e:
        print_exception(e)
