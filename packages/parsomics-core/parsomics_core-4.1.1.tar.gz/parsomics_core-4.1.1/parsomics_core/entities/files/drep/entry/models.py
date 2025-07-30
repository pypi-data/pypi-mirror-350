from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.drep.directory.models import DrepDirectory
    from parsomics_core.entities.omics.genome.models import Genome


class DrepEntryBase(SQLModel):
    genome_name: str
    genome_cluster_name: str
    is_winner: bool

    directory_key: int = Field(default=None, foreign_key="drepdirectory.key")


class DrepEntry(DrepEntryBase, table=True):
    __table_args__ = (UniqueConstraint("genome_name", "directory_key"),)

    key: int | None = Field(default=None, primary_key=True)

    directory: "DrepDirectory" = Relationship(back_populates="entries")
    genome: "Genome" = Relationship(back_populates="drep_entry")


class DrepEntryPublic(DrepEntryBase):
    key: int


class DrepEntryCreate(DrepEntryBase):
    pass


class DrepEntryDemand(DrepEntryCreate):
    pass
