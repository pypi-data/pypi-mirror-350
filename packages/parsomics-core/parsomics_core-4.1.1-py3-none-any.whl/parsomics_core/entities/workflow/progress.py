from enum import Enum

from pydantic import BaseModel


class ProgressStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Progress(BaseModel):
    status: ProgressStatus = ProgressStatus.IN_PROGRESS
