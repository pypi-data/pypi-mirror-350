from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from parsomics_core.entities.omics.fragment.models import Fragment
    from parsomics_core.entities.omics.protein.models import Protein


class FragmentProteinLinkBase(SQLModel):
    fragment_key: int | None = Field(
        default=None,
        foreign_key="fragment.key",
        primary_key=True,
    )
    protein_key: int | None = Field(
        default=None,
        foreign_key="protein.key",
        primary_key=True,
    )


class FragmentProteinLink(FragmentProteinLinkBase, table=True):
    protein: "Protein" = Relationship(sa_relationship_kwargs={"viewonly": True})
    fragment: "Fragment" = Relationship(sa_relationship_kwargs={"viewonly": True})


class FragmentProteinLinkPublic(FragmentProteinLinkBase):
    pass


class FragmentProteinLinkCreate(FragmentProteinLinkBase):
    pass


class FragmentProteinLinkDemand(FragmentProteinLinkCreate):
    pass
