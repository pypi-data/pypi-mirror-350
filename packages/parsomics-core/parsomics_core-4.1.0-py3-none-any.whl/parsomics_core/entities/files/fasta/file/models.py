from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from parsomics_core.entities.files.fasta.sequence_type import SequenceType
from parsomics_core.entities.files.fasta.validated_file import FASTAValidatedFile

if TYPE_CHECKING:
    from parsomics_core.entities.files.fasta.entry.models import FASTAEntry
    from parsomics_core.entities.omics.genome.models import Genome
    from parsomics_core.entities.workflow.run.models import Run


class FASTAFileBase(SQLModel):
    path: str
    run_key: int = Field(default=None, foreign_key="run.key")
    genome_key: int = Field(default=None, foreign_key="genome.key")
    sequence_type: SequenceType

    @field_validator("path")
    def path_must_be_validated(cls, path: str) -> str:
        _ = FASTAValidatedFile(path=path)
        return path


class FASTAFile(FASTAFileBase, table=True):
    __table_args__ = (UniqueConstraint("path"),)

    key: int | None = Field(default=None, primary_key=True)

    entries: list["FASTAEntry"] = Relationship(back_populates="file")
    genome: "Genome" = Relationship(
        back_populates="fasta_file",
        sa_relationship_kwargs={"uselist": False},
    )
    run: "Run" = Relationship(back_populates="fasta_files")


class FASTAFilePublic(FASTAFileBase):
    key: int


class FASTAFileCreate(FASTAFileBase):
    pass


class FASTAFileDemand(FASTAFileCreate):
    pass
