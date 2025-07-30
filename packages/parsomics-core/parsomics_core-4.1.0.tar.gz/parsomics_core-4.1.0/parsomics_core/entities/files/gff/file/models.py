from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.files.gff.validated_file import GFFValidatedFile

if TYPE_CHECKING:
    from parsomics_core.entities.files.gff.entry.models import GFFEntry
    from parsomics_core.entities.omics.genome.models import Genome
    from parsomics_core.entities.workflow.run.models import Run


class GFFFileBase(SQLModel):
    path: str
    run_key: int = Field(default=None, foreign_key="run.key")
    genome_key: int = Field(default=None, foreign_key="genome.key")

    @field_validator("path")
    def path_must_be_validated(cls, path: str) -> str:
        _ = GFFValidatedFile(path=path)
        return path


class GFFFile(GFFFileBase, table=True):
    __table_args__ = (UniqueConstraint("path"),)

    key: int | None = Field(default=None, primary_key=True)

    entries: list["GFFEntry"] = Relationship(back_populates="file")
    genome: "Genome" = Relationship(
        back_populates="gff_file",
        sa_relationship_kwargs={"uselist": False},
    )
    run: "Run" = Relationship(back_populates="gff_files")


class GFFFilePublic(GFFFileBase):
    key: int


class GFFFileCreate(GFFFileBase):
    pass


class GFFFileDemand(GFFFileCreate):
    pass
