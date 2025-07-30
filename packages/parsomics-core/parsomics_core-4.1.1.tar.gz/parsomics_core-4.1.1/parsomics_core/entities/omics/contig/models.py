from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.fasta.entry.models import FASTAEntry
    from parsomics_core.entities.omics.gene.models import Gene
    from parsomics_core.entities.omics.genome.models import Genome
    from parsomics_core.entities.omics.repeated_region.models import RepeatedRegion


class ContigBase(SQLModel):
    genome_key: int = Field(default=None, foreign_key="genome.key")
    fasta_entry_key: int = Field(default=None, foreign_key="fastaentry.key")


class Contig(ContigBase, table=True):
    __table_args__ = (UniqueConstraint("fasta_entry_key"),)

    key: int | None = Field(default=None, primary_key=True)

    genome: "Genome" = Relationship(
        back_populates="contigs",
    )
    genes: list["Gene"] = Relationship(
        back_populates="contig",
    )
    repeated_regions: list["RepeatedRegion"] = Relationship(
        back_populates="contig",
    )
    fasta_entry: "FASTAEntry" = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="contig",
    )


class ContigPublic(ContigBase):
    key: int


class ContigCreate(ContigBase):
    pass


class ContigDemand(ContigCreate):
    pass
