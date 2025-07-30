from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field


class Timestamp:
    created_at: datetime = Field(
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )
