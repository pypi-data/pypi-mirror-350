from pathlib import Path
import typer
from rich import print
from rich.table import Table
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from parsomics_cli.frontend.helpers import (
    bool_to_checkbox,
    bool_to_yn,
    print_exception,
    print_failure,
    print_info,
    print_success,
    print_warning,
)
from parsomics_cli.backend.plugins.exc import (
    PluginDoesNotExistException,
    PluginMakerException,
    PluginManagerException,
)
from parsomics_cli.backend.plugins.utils import (
    PluginMaker,
    PluginManager,
    PluginMetadata,
)

console = Console()
plugin_app = typer.Typer()
plugin_manager = PluginManager()


@plugin_app.command("install")
def plugin_install(
    plugin_names: list[str] = typer.Argument(..., help="Names of plugins to install"),
):
    """
    Install plugins
    """
    for plugin_name in plugin_names:
        try:
            plugin_manager.check_plugin_installable(plugin_name)
        except PluginManagerException as e:
            print_exception(e)
            print_failure("Plugin not installed")
            return

        plugin_metadata = plugin_manager.available_plugin_index[plugin_name]
        if not plugin_metadata.official:
            print_warning(
                f'The plugin "{plugin_name}" is not an official plugin.\n'
                "This means it was not made by the same team that developed "
                "parsomics itself.",
            )
            install = typer.confirm("Install plugin?")
            if install:
                plugin_manager.install_plugin(plugin_name)
            else:
                print_info("Plugin installation aborted")
        else:

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description=f'Installing plugin "{plugin_name}"...', total=None
                )
                plugin_manager.install_plugin(plugin_name)
            print_success(f'Plugin "{plugin_name}" installed')


@plugin_app.command("uninstall")
def plugin_uninstall(
    plugin_names: list[str] = typer.Argument(..., help="Names of plugins to install"),
):
    """
    Uninstall plugins
    """
    for plugin_name in plugin_names:
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description=f'Uninstalling plugin "{plugin_name}"...', total=None
                )
                plugin_manager.uninstall_plugin(plugin_name)
            print_success(f'Plugin "{plugin_name}" uninstalled')
        except PluginManagerException as e:
            print_exception(e)


@plugin_app.command("list")
def plugin_list():
    """
    List plugins
    """
    plugins = plugin_manager.list_plugins()
    table = Table("Plugin name", "Installed")

    for p in plugins:
        checkbox = bool_to_checkbox(p["installed"])
        table.add_row(p["name"], checkbox)
    console.print(table)


def _print_plugin_metadata(plugin_metadata: PluginMetadata):
    """
    Pretty-prints a PluginMetadata object
    """
    installed = plugin_manager.is_plugin_installed(plugin_metadata.name)

    print(f"[bold]Name[/bold]: {plugin_metadata.name}")
    print(f'[bold]Description[/bold]: "{plugin_metadata.description}"')
    print(f"[bold]Plugin URL[/bold]: {plugin_metadata.url}")
    print(f"[bold]Tool URL[/bold]: {plugin_metadata.tool_url}")
    print(f"[bold]PyPI package[/bold]: {plugin_metadata.pypi_package}")

    # Disable rich's highlighting for some fields
    console.print(
        f"[bold]Date added[/bold]: {plugin_metadata.date_added.strftime("%Y/%m/%d at %H:%M:%S")}",
        highlight=False,
    )
    console.print(
        f"[bold]License[/bold]: {plugin_metadata.license}",
        highlight=False,
    )

    print(f"[bold]Official[/bold]: {bool_to_yn(plugin_metadata.official)}")
    print(f"[bold]Installed[/bold]: {bool_to_checkbox(installed)}")


@plugin_app.command("info")
def plugin_info(
    plugin_name: str = typer.Argument(
        ..., help="Name of plugin to display information"
    ),
):
    """
    Display information of a plugin
    """
    if plugin_name in plugin_manager.available_plugin_index:
        plugin_metadata = plugin_manager.available_plugin_index[plugin_name]
        _print_plugin_metadata(plugin_metadata)
    else:
        print_exception(PluginDoesNotExistException(plugin_name))


@plugin_app.command("create")
def plugin_create(
    name: str = typer.Argument(
        ..., help="Name of the tool that plugin will add support for"
    ),
    path: Path = typer.Argument(..., help="Directory where to create the plugin"),
):
    """
    Create a plugin from a template
    """
    try:
        PluginMaker.make_plugin(name, path)
    except PluginMakerException as e:
        print_exception(e)
