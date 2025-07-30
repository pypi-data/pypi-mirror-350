import logging

from sqlmodel import Session, select

from parsomics_core.entities.files.fasta.entry.models import FASTAEntry
from parsomics_core.entities.files.fasta.file.models import FASTAFile
from parsomics_core.entities.files.fasta.sequence_type import SequenceType
from parsomics_core.entities.omics.gene.models import Gene
from parsomics_core.entities.workflow.assembly.models import Assembly
from parsomics_core.entities.workflow.run.models import Run
from parsomics_core.globals.database import engine


def search_gene_by_name(gene_name: str, assembly_key: int):
    statement = (
        select(Gene)
        .join(FASTAEntry)
        .join(FASTAFile)
        .join(Run)
        .join(Assembly)
        .where(FASTAFile.sequence_type == SequenceType.GENE)
        .where(FASTAEntry.sequence_name == gene_name)
        .where(Assembly.key == assembly_key)
    )

    with Session(engine) as session:
        genes = session.exec(statement).all()
        if len(genes) > 1:
            logging.warning(
                f"Expected only one Gene to match name {gene_name}, "
                f"but matched: {genes}"
            )

        if not genes:
            raise Exception(f"No Genes were matched to name {gene_name} ")

        gene_key = genes[0].key
        return gene_key
