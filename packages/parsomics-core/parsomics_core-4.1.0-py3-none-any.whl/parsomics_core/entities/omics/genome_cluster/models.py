from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.omics.genome.models import Genome

if TYPE_CHECKING:
    from parsomics_core.entities.files.drep.directory.models import DrepDirectory
    from parsomics_core.entities.omics.sample.models import Sample


class GenomeClusterBase(SQLModel):
    name: str
    drep_directory_key: int = Field(default=None, foreign_key="drepdirectory.key")


class GenomeCluster(GenomeClusterBase, table=True):
    __table_args__ = (UniqueConstraint("name", "drep_directory_key"),)

    key: int | None = Field(default=None, primary_key=True)

    drep_directory: "DrepDirectory" = Relationship(
        back_populates="genome_clusters",
    )
    genomes: list["Genome"] = Relationship(
        back_populates="genome_cluster",
    )
    samples: list["Sample"] = Relationship(
        sa_relationship_kwargs={"overlaps": "genome_cluster,genomes,sample"},
        back_populates="genome_clusters",
        link_model=Genome,
    )


class GenomeClusterPublic(GenomeClusterBase):
    key: int


class GenomeClusterCreate(GenomeClusterBase):
    pass


class GenomeClusterDemand(GenomeClusterCreate):
    pass
