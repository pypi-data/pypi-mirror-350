import datetime as dt
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.files.gene_annotation.file.models import GeneAnnotationFile

from parsomics_core.entities.workflow.progress import Progress
from parsomics_core.entities.workflow.timestamp import Timestamp

if TYPE_CHECKING:
    from parsomics_core.entities.files.drep.directory.models import DrepDirectory
    from parsomics_core.entities.files.fasta.file.models import FASTAFile
    from parsomics_core.entities.files.gff.file.models import GFFFile
    from parsomics_core.entities.files.gtdbtk.file.models import GTDBTkFile
    from parsomics_core.entities.files.protein_annotation.file.models import (
        ProteinAnnotationFile,
    )
    from parsomics_core.entities.workflow.assembly.models import Assembly
    from parsomics_core.entities.workflow.tool.models import Tool


class RunBase(SQLModel, Progress):
    output_directory: str
    version: str | None = None
    date: dt.date | None = None

    tool_key: int = Field(default=None, foreign_key="tool.key")
    assembly_key: int = Field(default=None, foreign_key="assembly.key")


class Run(RunBase, Timestamp, table=True):
    __table_args__ = (UniqueConstraint("output_directory"),)

    key: int | None = Field(default=None, primary_key=True)

    tool: "Tool" = Relationship(back_populates="runs")

    assembly: "Assembly" = Relationship(back_populates="runs")

    protein_annotation_files: list["ProteinAnnotationFile"] = Relationship(
        back_populates="run"
    )
    gene_annotation_files: list["GeneAnnotationFile"] = Relationship(
        back_populates="run"
    )
    fasta_files: list["FASTAFile"] = Relationship(back_populates="run")
    gff_files: list["GFFFile"] = Relationship(back_populates="run")
    gtdbtk_files: list["GTDBTkFile"] = Relationship(back_populates="run")
    drep_directories: list["DrepDirectory"] = Relationship(back_populates="run")


class RunPublic(RunBase):
    key: int


class RunCreate(RunBase):
    pass


class RunDemand(RunCreate):
    pass
