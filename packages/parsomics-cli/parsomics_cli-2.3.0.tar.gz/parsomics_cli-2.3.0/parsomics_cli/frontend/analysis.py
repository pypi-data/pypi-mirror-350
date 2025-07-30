from pathlib import Path

import typer

from parsomics_cli.frontend.helpers import print_exception
from parsomics_cli.backend.analysis.types import AnalysisProgress, AnalysisStatus
from parsomics_cli.backend.analysis.utils import AnalysisManager
from parsomics_cli.backend.database.exc import ContainerManagerException

from rich import print

analysis_app = typer.Typer()
analysis_manager = AnalysisManager()


@analysis_app.command("status")
def analysis_status():
    """
    Get analysis status
    """
    try:
        status: AnalysisStatus = analysis_manager.get_status()
        match status.progress:
            case AnalysisProgress.UNKNOWN:
                print(
                    "The parsomics analysis status is [bold bright_black]unknown[/bold bright_black]",
                )
            case AnalysisProgress.NEVER_RAN:
                print(
                    "The parsomics analysis program [bold red]never ran[/bold red].",
                )
            case AnalysisProgress.IN_PROGRESS:
                print(
                    "The parsomics analysis program [bold yellow]is running[/bold yellow].",
                )
            case AnalysisProgress.DONE:
                print(
                    "The parsomics program [bold green]ran successfully[/bold green] at least once.\n"
                    f"[bold bright_black]It was last ran on {status.updated_at}.[/bold bright_black]"
                )
    except ContainerManagerException as e:
        print_exception(e)


@analysis_app.command("run")
def analysis_run(
    config_file_path: Path | None = typer.Argument(
        default=None, help="Path to configuration file"
    )
):
    """
    Process data
    """
    try:
        analysis_manager.run(config_file_path)
    except ContainerManagerException as e:
        print_exception(e)
