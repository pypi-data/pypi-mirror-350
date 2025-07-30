from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.omics.fragment_protein_link.models import (
    FragmentProteinLink,
)

if TYPE_CHECKING:
    from parsomics_core.entities.files.gff.entry.models import GFFEntry
    from parsomics_core.entities.omics.gene.models import Gene
    from parsomics_core.entities.omics.protein.models import Protein


class FragmentBase(SQLModel):
    gene_key: int = Field(default=None, foreign_key="gene.key")

    gff_entry_key: int = Field(default=None, foreign_key="gffentry.key")


class Fragment(FragmentBase, table=True):
    __table_args__ = (UniqueConstraint("gff_entry_key"),)

    key: int | None = Field(default=None, primary_key=True)

    gene: "Gene" = Relationship(back_populates="fragments")
    gff_entry: "GFFEntry" = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="fragment",
    )

    proteins: list["Protein"] = Relationship(
        back_populates="fragments", link_model=FragmentProteinLink
    )


class FragmentPublic(FragmentBase):
    key: int


class FragmentCreate(FragmentBase):
    pass


class FragmentDemand(FragmentCreate):
    pass
