import typer

from .analysis import analysis_app
from .config import config_app
from .database import database_app
from .plugins import plugin_app
from .setup import setup_app

# Create the main app
app = typer.Typer(help="A command-line interface (CLI) for parsomics")
app.add_typer(setup_app, name="setup", help="Setup parsomics")
app.add_typer(analysis_app, name="analysis", help="Manage analyses")
app.add_typer(config_app, name="config", help="Manage configurations")
app.add_typer(database_app, name="database", help="Manage database")
app.add_typer(plugin_app, name="plugin", help="Manage plugins")
