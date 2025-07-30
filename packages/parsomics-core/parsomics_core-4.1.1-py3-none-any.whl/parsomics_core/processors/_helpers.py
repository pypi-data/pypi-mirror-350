import logging

from sqlalchemy import Engine
from sqlmodel import Session, select

from parsomics_core.entities.files.validated_file import ValidatedFileWithGenome
from parsomics_core.entities.files.drep.directory.models import DrepDirectory
from parsomics_core.entities.files.drep.entry.models import DrepEntry
from parsomics_core.entities.omics.genome.models import Genome, GenomePublic
from parsomics_core.entities.workflow.assembly.models import Assembly
from parsomics_core.entities.workflow.run.models import Run


def retrieve_genome_key(
    engine: Engine, file: ValidatedFileWithGenome, assembly_key: int
) -> int:
    with Session(engine) as session:
        statement = (
            select(Genome)
            .join(DrepEntry)
            .join(DrepDirectory)
            .join(Run)
            .join(Assembly)
            .where(DrepEntry.genome_name == file.genome_name)
            .where(Assembly.key == assembly_key)
        )
        results = session.exec(statement)
        genomes = results.all()

        if len(genomes) > 1:
            logging.warning(
                f"Expected only one Genome in the same Assembly (key = "
                f"{assembly_key}) to match name {file.genome_name}, but "
                f"matched: {genomes}"
            )

        if not genomes:
            raise Exception(
                f"No Genomes were matched to name {file.genome_name}, in "
                f"the same Assembly (key {assembly_key})"
            )

        genome_key: int = GenomePublic.model_validate(genomes[0]).key
        return genome_key
