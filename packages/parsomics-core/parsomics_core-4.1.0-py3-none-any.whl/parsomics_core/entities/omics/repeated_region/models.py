from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.gff.entry.models import GFFEntry
    from parsomics_core.entities.omics.contig.models import Contig


class RepeatedRegionBase(SQLModel):
    contig_key: int = Field(default=None, foreign_key="contig.key")
    gff_entry_key: int = Field(default=None, foreign_key="gffentry.key")


class RepeatedRegion(RepeatedRegionBase, table=True):
    __table_args__ = (UniqueConstraint("gff_entry_key"),)

    key: int | None = Field(default=None, primary_key=True)

    contig: "Contig" = Relationship(back_populates="repeated_regions")
    gff_entry: "GFFEntry" = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="repeated_region",
    )


class RepeatedRegionPublic(RepeatedRegionBase):
    key: int


class RepeatedRegionCreate(RepeatedRegionBase):
    pass


class RepeatedRegionDemand(RepeatedRegionCreate):
    pass
