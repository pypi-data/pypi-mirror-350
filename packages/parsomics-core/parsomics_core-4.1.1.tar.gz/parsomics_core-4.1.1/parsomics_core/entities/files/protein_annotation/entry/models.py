from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.protein_annotation.file.models import (
        ProteinAnnotationFile,
    )
    from parsomics_core.entities.omics.protein.models import Protein
    from parsomics_core.entities.workflow.source.models import Source


class ProteinAnnotationEntryBase(SQLModel):
    description: str | None = None
    coord_start: int | None = None
    coord_stop: int | None = None
    accession: str | None = None
    score: float | None = None
    annotation_type: str | None = None
    details: dict = Field(default={}, sa_column=Column(JSONB))

    protein_key: int = Field(default=None, foreign_key="protein.key")
    file_key: int = Field(default=None, foreign_key="proteinannotationfile.key")
    source_key: int | None = Field(default=None, foreign_key="source.key")


class ProteinAnnotationEntry(ProteinAnnotationEntryBase, table=True):
    __table_args__ = (
        UniqueConstraint(
            "coord_start",
            "coord_stop",
            "description",
            "protein_key",
            "file_key",
            "source_key",
        ),
    )

    key: int | None = Field(default=None, primary_key=True)

    protein: "Protein" = Relationship(back_populates="protein_annotation_entries")
    file: "ProteinAnnotationFile" = Relationship(back_populates="entries")
    source: "Source" = Relationship(back_populates="protein_annotation_entries")


class ProteinAnnotationEntryPublic(ProteinAnnotationEntryBase):
    key: int


class ProteinAnnotationEntryCreate(ProteinAnnotationEntryBase):
    pass


class ProteinAnnotationEntryDemand(ProteinAnnotationEntryCreate):
    pass
