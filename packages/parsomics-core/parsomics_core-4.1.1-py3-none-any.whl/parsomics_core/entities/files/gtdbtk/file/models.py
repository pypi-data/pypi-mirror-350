from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.files.gtdbtk.validated_file import GTDBTkValidatedFile

if TYPE_CHECKING:
    from parsomics_core.entities.workflow.run.models import Run
    from parsomics_core.entities.files.gtdbtk.entry.models import GTDBTkEntry

# File -----------------------------------------------------------------------


class GTDBTkFileBase(SQLModel):
    path: str
    run_key: int = Field(default=None, foreign_key="run.key")

    @field_validator("path")
    def path_must_be_validated(cls, path: str) -> str:
        _ = GTDBTkValidatedFile(path=path)
        return path


class GTDBTkFile(GTDBTkFileBase, table=True):
    __table_args__ = (UniqueConstraint("path"),)

    key: int | None = Field(default=None, primary_key=True)

    entries: list["GTDBTkEntry"] = Relationship(back_populates="file")
    run: "Run" = Relationship(back_populates="gtdbtk_files")


class GTDBTkFilePublic(GTDBTkFileBase):
    key: int


class GTDBTkFileCreate(GTDBTkFileBase):
    pass


class GTDBTkFileDemand(GTDBTkFileCreate):
    pass
