from pathlib import Path

from parsomics_core import Runner
from parsomics_core.entities import Metadata
from parsomics_core.entities.workflow.progress import ProgressStatus
from parsomics_core.globals.database import engine
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlmodel import Session, select

from parsomics_cli.backend.analysis.types import AnalysisProgress, AnalysisStatus
from parsomics_cli.backend.database.exc import ContainerManagerException
from parsomics_cli.backend.database.utils import ContainerManager

container_manager = ContainerManager()


class AnalysisManager(BaseModel):
    def check_reachable(self) -> None:
        container_manager.check_podman_executable()
        container_manager.check_podman_socket()
        container_manager.check_container_exists()
        container_manager.check_container_is_running()

    def run(self, config_file_path: Path | None = None):
        self.check_reachable()
        runner = Runner(config_file_path)
        runner.run()

    def get_status(self) -> AnalysisStatus:
        # First, check if database is reachable.
        # If it isn't, run status is UNKNOWN.
        try:
            self.check_reachable()
        except ContainerManagerException:
            return AnalysisStatus(progress=AnalysisProgress.UNKNOWN)

        # Second, check if the "metadata" table has already been created.
        # If it hasn't, run status is NEVER_RAN
        inspector = inspect(engine)
        if not inspector.has_table(str(Metadata.__tablename__)):
            return AnalysisStatus(progress=AnalysisProgress.NEVER_RAN)

        with Session(engine) as session:
            statement = select(Metadata).where(Metadata.key == 1)
            result = session.exec(statement).all()

            if not result:
                status = AnalysisStatus(progress=AnalysisProgress.NEVER_RAN)
            else:
                metadata = result[0]
                match metadata.status:
                    case ProgressStatus.IN_PROGRESS:
                        status = AnalysisStatus(progress=AnalysisProgress.IN_PROGRESS)
                    case ProgressStatus.DONE:
                        status = AnalysisStatus(
                            progress=AnalysisProgress.DONE,
                            updated_at=metadata.updated_at,
                        )
        return status
