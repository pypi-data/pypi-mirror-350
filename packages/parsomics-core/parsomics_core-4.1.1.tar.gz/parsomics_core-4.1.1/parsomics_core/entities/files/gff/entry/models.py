from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import ARRAY, Field, Relationship, SQLModel, String, UniqueConstraint

from parsomics_core.entities.omics.fragment.fragment_type import FragmentType
from parsomics_core.entities.omics.repeated_region.models import RepeatedRegion

if TYPE_CHECKING:
    from parsomics_core.entities.files.gff.file.models import GFFFile
    from parsomics_core.entities.omics.fragment.models import Fragment
    from parsomics_core.entities.workflow.source.models import Source


class GFFEntryBase(SQLModel):
    # Source: https://en.wikipedia.org/wiki/General_feature_format#GFF_general_structure
    gene_name: str | None = Field(default=None, index=True)
    identifier: str | None = Field(default=None, index=True)
    contig_name: str = Field(index=True)
    fragment_type: FragmentType
    coord_start: int
    coord_stop: int
    score: float | None = None
    strand: str | None = None
    phase: int | None = None
    attributes: dict = Field(default={}, sa_column=Column(JSONB))

    file_key: int = Field(default=None, foreign_key="gfffile.key")
    source_key: int = Field(default=None, foreign_key="source.key")


class GFFEntry(GFFEntryBase, table=True):
    __table_args__ = (UniqueConstraint("file_key", "identifier"),)

    key: int | None = Field(default=None, primary_key=True)

    file: "GFFFile" = Relationship(back_populates="entries")
    source: "Source" = Relationship(back_populates="gff_entries")
    fragment: "Fragment" = Relationship(back_populates="gff_entry")
    repeated_region: "RepeatedRegion" = Relationship(back_populates="gff_entry")


class GFFEntryPublic(GFFEntryBase):
    key: int


class GFFEntryCreate(GFFEntryBase):
    pass


class GFFEntryDemand(GFFEntryCreate):
    pass
