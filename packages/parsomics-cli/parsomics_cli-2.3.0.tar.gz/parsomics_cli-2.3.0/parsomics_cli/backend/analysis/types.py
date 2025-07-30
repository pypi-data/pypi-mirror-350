from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class AnalysisProgress(Enum):
    UNKNOWN = 0
    NEVER_RAN = 1
    IN_PROGRESS = 2
    DONE = 3


class AnalysisStatus(BaseModel):
    progress: AnalysisProgress
    updated_at: datetime | None = None
