from typing import TYPE_CHECKING, Union

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.fasta.file.models import FASTAFile
    from parsomics_core.entities.omics.contig.models import Contig
    from parsomics_core.entities.omics.gene.models import Gene
    from parsomics_core.entities.omics.protein.models import Protein
    from parsomics_core.entities.workflow.source.models import Source


class FASTAEntryBase(SQLModel):
    # Source: https://en.wikipedia.org/wiki/FASTA_format#Overview
    sequence_name: str = Field(index=True)
    description: str | None = None
    sequence: str

    file_key: int = Field(default=None, foreign_key="fastafile.key")
    source_key: int | None = Field(default=None, foreign_key="source.key")


class FASTAEntry(FASTAEntryBase, table=True):
    __table_args__ = (UniqueConstraint("file_key", "sequence_name"),)

    key: int | None = Field(default=None, primary_key=True)

    file: "FASTAFile" = Relationship(back_populates="entries")
    source: Union["Source", None] = Relationship(back_populates="fasta_entries")

    contig: Union["Contig", None] = Relationship(
        back_populates="fasta_entry",
    )
    gene: Union["Gene", None] = Relationship(
        back_populates="fasta_entry",
    )
    protein: Union["Protein", None] = Relationship(
        back_populates="fasta_entry",
    )


class FASTAEntryPublic(FASTAEntryBase):
    key: int


class FASTAEntryCreate(FASTAEntryBase):
    pass


class FASTAEntryDemand(FASTAEntryCreate):
    pass
