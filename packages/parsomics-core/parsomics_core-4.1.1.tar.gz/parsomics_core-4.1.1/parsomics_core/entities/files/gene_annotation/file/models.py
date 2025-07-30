from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.gene_annotation.entry.models import (
        GeneAnnotationEntry,
    )
    from parsomics_core.entities.workflow.run.models import Run


class GeneAnnotationFileBase(SQLModel):
    path: str
    run_key: int = Field(default=None, foreign_key="run.key")


class GeneAnnotationFile(GeneAnnotationFileBase, table=True):
    __table_args__ = (UniqueConstraint("path"),)

    key: int | None = Field(default=None, primary_key=True)

    entries: list["GeneAnnotationEntry"] = Relationship(back_populates="file")
    run: "Run" = Relationship(back_populates="gene_annotation_files")


class GeneAnnotationFilePublic(GeneAnnotationFileBase):
    key: int


class GeneAnnotationFileCreate(GeneAnnotationFileBase):
    pass


class GeneAnnotationFileDemand(GeneAnnotationFileCreate):
    pass
