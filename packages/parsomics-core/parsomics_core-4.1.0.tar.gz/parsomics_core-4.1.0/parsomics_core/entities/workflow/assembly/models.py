from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.workflow.progress import Progress
from parsomics_core.entities.workflow.timestamp import Timestamp

if TYPE_CHECKING:
    from parsomics_core.entities.workflow.project.models import Project
    from parsomics_core.entities.workflow.run.models import Run


class AssemblyBase(SQLModel, Progress):
    project_key: int = Field(default=None, foreign_key="project.key")
    name: str


class Assembly(AssemblyBase, Timestamp, table=True):
    __table_args__ = (UniqueConstraint("name", "project_key"),)

    key: int | None = Field(default=None, primary_key=True)

    runs: list["Run"] = Relationship(back_populates="assembly")
    project: "Project" = Relationship(back_populates="assemblies")


class AssemblyPublic(AssemblyBase):
    key: int


class AssemblyCreate(AssemblyBase):
    pass


class AssemblyDemand(AssemblyCreate):
    pass
