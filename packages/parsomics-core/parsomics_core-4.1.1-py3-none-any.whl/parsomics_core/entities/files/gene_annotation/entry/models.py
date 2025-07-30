from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.gene_annotation.file.models import (
        GeneAnnotationFile,
    )
    from parsomics_core.entities.omics.gene.models import Gene
    from parsomics_core.entities.workflow.source.models import Source


class GeneAnnotationEntryBase(SQLModel):
    description: str | None = None
    coord_start: int | None = None
    coord_stop: int | None = None
    accession: str | None = None
    score: float | None = None
    annotation_type: str | None = None
    details: dict = Field(default={}, sa_column=Column(JSONB))

    gene_key: int = Field(default=None, foreign_key="gene.key")
    file_key: int = Field(default=None, foreign_key="geneannotationfile.key")
    source_key: int = Field(default=None, foreign_key="source.key")


class GeneAnnotationEntry(GeneAnnotationEntryBase, table=True):
    __table_args__ = (
        UniqueConstraint(
            "coord_start",
            "coord_stop",
            "description",
            "gene_key",
            "file_key",
            "source_key",
        ),
    )

    key: int | None = Field(default=None, primary_key=True)

    gene: "Gene" = Relationship(back_populates="gene_annotation_entries")
    file: "GeneAnnotationFile" = Relationship(back_populates="entries")
    source: "Source" = Relationship(back_populates="gene_annotation_entries")


class GeneAnnotationEntryPublic(GeneAnnotationEntryBase):
    key: int


class GeneAnnotationEntryCreate(GeneAnnotationEntryBase):
    pass


class GeneAnnotationEntryDemand(GeneAnnotationEntryCreate):
    pass
