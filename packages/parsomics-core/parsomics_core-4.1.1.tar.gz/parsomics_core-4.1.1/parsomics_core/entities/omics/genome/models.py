from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from parsomics_core.entities.files.drep.entry.models import DrepEntry
    from parsomics_core.entities.files.fasta.file.models import FASTAFile
    from parsomics_core.entities.files.gff.file.models import GFFFile
    from parsomics_core.entities.files.gtdbtk.entry.models import GTDBTkEntry
    from parsomics_core.entities.files.protein_annotation.file.models import (
        ProteinAnnotationFile,
    )
    from parsomics_core.entities.omics.contig.models import Contig
    from parsomics_core.entities.omics.genome_cluster.models import GenomeCluster
    from parsomics_core.entities.omics.sample.models import Sample


class GenomeBase(SQLModel):
    drep_entry_key: int = Field(
        default=None,
        foreign_key="drepentry.key",
    )
    genome_cluster_key: int = Field(
        default=None,
        foreign_key="genomecluster.key",
    )
    sample_key: int = Field(
        default=None,
        foreign_key="sample.key",
    )


class Genome(GenomeBase, table=True):
    __table_args__ = (UniqueConstraint("drep_entry_key"),)

    key: int | None = Field(default=None, primary_key=True)

    drep_entry: "DrepEntry" = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="genome",
    )
    gtdbtk_entry: "GTDBTkEntry" = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="genome",
    )

    contigs: list["Contig"] = Relationship(back_populates="genome")

    genome_cluster: "GenomeCluster" = Relationship(
        back_populates="genomes",
    )
    sample: "Sample" = Relationship(
        back_populates="genomes",
    )

    fasta_file: "FASTAFile" = Relationship(back_populates="genome")
    gff_file: "GFFFile" = Relationship(back_populates="genome")

    protein_annotation_files: list["ProteinAnnotationFile"] = Relationship(
        back_populates="genome"
    )


class GenomePublic(GenomeBase):
    key: int


class GenomeCreate(GenomeBase):
    pass


class GenomeDemand(GenomeCreate):
    pass
