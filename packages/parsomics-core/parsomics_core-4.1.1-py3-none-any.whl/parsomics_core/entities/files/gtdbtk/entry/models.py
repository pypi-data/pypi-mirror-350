from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.gtdbtk.file.models import GTDBTkFile
    from parsomics_core.entities.omics.genome.models import Genome


class GTDBTkEntryBase(SQLModel):
    # Source: https://ecogenomics.github.io/GTDBTk/files/summary.tsv.html
    reference: str | None
    radius: float | None
    ani: float | None
    af: float | None

    classification_method: str
    note: str | None
    red_value: float | None
    warnings: str | None

    domain: str
    phylum: str
    klass: str  # NOTE: cannot be "class" because it is a reserved word
    order: str
    family: str
    genus: str
    species: str
    taxonomic_novelty: bool

    genome_key: int = Field(default=None, foreign_key="genome.key")
    file_key: int = Field(default=None, foreign_key="gtdbtkfile.key")


class GTDBTkEntry(GTDBTkEntryBase, table=True):
    __table_args__ = (UniqueConstraint("file_key", "genome_key"),)

    key: int | None = Field(default=None, primary_key=True)

    file: "GTDBTkFile" = Relationship(back_populates="entries")
    genome: "Genome" = Relationship(back_populates="gtdbtk_entry")


class GTDBTkEntryPublic(GTDBTkEntryBase):
    key: int


class GTDBTkEntryCreate(GTDBTkEntryBase):
    pass


class GTDBTkEntryDemand(GTDBTkEntryCreate):
    pass
