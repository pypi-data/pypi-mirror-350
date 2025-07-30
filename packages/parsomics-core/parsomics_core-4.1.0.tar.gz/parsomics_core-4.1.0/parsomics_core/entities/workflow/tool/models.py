from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.workflow.run.models import Run
    from parsomics_core.entities.workflow.source.models import Source


class ToolBase(SQLModel):
    name: str


class Tool(ToolBase, table=True):
    __table_args__ = (UniqueConstraint("name"),)

    key: int | None = Field(default=None, primary_key=True)

    sources: list["Source"] = Relationship(back_populates="tool")
    runs: list["Run"] = Relationship(back_populates="tool")


class ToolPublic(ToolBase):
    key: int


class ToolCreate(ToolBase):
    pass


class ToolDemand(ToolCreate):
    pass
