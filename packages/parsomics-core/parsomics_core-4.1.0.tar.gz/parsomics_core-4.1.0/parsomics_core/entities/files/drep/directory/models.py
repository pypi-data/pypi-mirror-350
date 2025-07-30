from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.files.drep.validated_directory import (
    DrepValidatedDirectory,
)

if TYPE_CHECKING:
    from parsomics_core.entities.files.drep.entry.models import DrepEntry
    from parsomics_core.entities.omics.genome_cluster.models import GenomeCluster
    from parsomics_core.entities.omics.sample.models import Sample
    from parsomics_core.entities.workflow.run.models import Run


class DrepDirectoryBase(SQLModel):
    path: str
    run_key: int = Field(default=None, foreign_key="run.key")

    @field_validator("path")
    def path_must_be_validated(cls, path: str) -> str:
        try:
            _ = DrepValidatedDirectory(path=path)
        except ValueError as e:
            raise e
        return path


class DrepDirectory(DrepDirectoryBase, table=True):
    __table_args__ = (UniqueConstraint("path"),)

    key: int | None = Field(default=None, primary_key=True)

    samples: list["Sample"] = Relationship(
        back_populates="drep_directory",
    )
    genome_clusters: list["GenomeCluster"] = Relationship(
        back_populates="drep_directory"
    )
    entries: list["DrepEntry"] = Relationship(back_populates="directory")
    run: "Run" = Relationship(back_populates="drep_directories")


class DrepDirectoryPublic(DrepDirectoryBase):
    key: int


class DrepDirectoryCreate(DrepDirectoryBase):
    pass


class DrepDirectoryDemand(DrepDirectoryCreate):
    pass
