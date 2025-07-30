from sqlmodel import Field, SQLModel

from parsomics_core.entities.workflow.progress import Progress
from parsomics_core.entities.workflow.timestamp import Timestamp


class MetadataBase(SQLModel, Progress):
    pass


class Metadata(MetadataBase, Timestamp, table=True):
    key: int | None = Field(default=None, primary_key=True)


class MetadataPublic(MetadataBase):
    key: int


class MetadataCreate(MetadataBase):
    pass


class MetadataDemand(MetadataBase):
    pass
