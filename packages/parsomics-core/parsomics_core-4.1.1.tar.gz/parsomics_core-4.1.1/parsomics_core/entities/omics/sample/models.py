from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.omics.genome.models import Genome

if TYPE_CHECKING:
    from parsomics_core.entities.files.drep.directory.models import DrepDirectory
    from parsomics_core.entities.omics.genome_cluster.models import GenomeCluster


class SampleBase(SQLModel):
    name: str
    drep_directory_key: int = Field(default=None, foreign_key="drepdirectory.key")


class Sample(SampleBase, table=True):
    __table_args__ = (UniqueConstraint("name", "drep_directory_key"),)

    key: int | None = Field(default=None, primary_key=True)

    drep_directory: "DrepDirectory" = Relationship(
        back_populates="samples",
    )
    genomes: list["Genome"] = Relationship(
        sa_relationship_kwargs={"overlaps": "samples"},
        back_populates="sample",
    )
    genome_clusters: list["GenomeCluster"] = Relationship(
        sa_relationship_kwargs={"overlaps": "genome_cluster,genomes,sample"},
        back_populates="samples",
        link_model=Genome,
    )


class SamplePublic(SampleBase):
    key: int


class SampleCreate(SampleBase):
    pass


class SampleDemand(SampleCreate):
    pass
