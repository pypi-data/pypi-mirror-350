import logging
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session

from parsomics_core.entities.files.fasta.file.models import FASTAFile, FASTAFileDemand
from parsomics_core.entities.files.fasta.file.transactions import FASTAFileTransactions
from parsomics_core.entities.files.fasta.file_factory import FASTAFileFactory
from parsomics_core.entities.files.fasta.parser import FASTAParser
from parsomics_core.entities.files.fasta.validated_file import FASTAValidatedFile
from parsomics_core.entities.files.gff.file.models import GFFFile, GFFFileDemand
from parsomics_core.entities.files.gff.file.transactions import GFFFileTransactions
from parsomics_core.entities.files.gff.file_factory import GFFFileFactory
from parsomics_core.entities.files.gff.parser import GFFParser
from parsomics_core.entities.files.gff.validated_file import GFFValidatedFile
from parsomics_core.processors._helpers import retrieve_genome_key


class ProkkaOutputProcessor(BaseModel):
    output_directory: str
    dereplicated_genomes: Sequence[str]
    assembly_key: int
    run_key: int
    tool_key: int

    def process_fasta_files(self, engine: Engine):
        fasta_file_factory: FASTAFileFactory = FASTAFileFactory(
            self.output_directory,
            self.dereplicated_genomes,
        )

        fasta_files: list[FASTAValidatedFile] = fasta_file_factory.assemble()
        for f in fasta_files:
            genome_key = retrieve_genome_key(engine, f, self.assembly_key)
            run_key = self.run_key

            fasta_file_demand_model = FASTAFileDemand(
                path=f.path,
                run_key=run_key,
                genome_key=genome_key,
                sequence_type=f._sequence_type,
            )

            with Session(engine) as session:
                fasta_file: FASTAFile = FASTAFile.model_validate(
                    FASTAFileTransactions().demand(
                        session,
                        fasta_file_demand_model,
                    )
                )

            fasta_parser = FASTAParser(file=fasta_file)
            fasta_parser.parse(engine)

        logging.info(
            f"Finished adding all prokka FASTA files on {self.output_directory} to the database."
        )

    def process_gff_files(self, engine: Engine):
        gff_file_factory: GFFFileFactory = GFFFileFactory(
            self.output_directory,
            self.dereplicated_genomes,
        )

        gff_files: list[GFFValidatedFile] = gff_file_factory.assemble()
        for f in gff_files:
            genome_key = retrieve_genome_key(engine, f, self.assembly_key)
            gff_file_demand_model = GFFFileDemand(
                path=f.path,
                run_key=self.run_key,
                genome_key=genome_key,
            )
            with Session(engine) as session:
                gff_file_key = (
                    GFFFileTransactions()
                    .demand(
                        session,
                        gff_file_demand_model,
                    )
                    .key
                )
            if gff_file_key is not None:
                logging.info(f"Added GFF file {f.path} to the database.")
            else:
                logging.warning(f"Failed to add GFF file {f.path} to the database.")

            with Session(engine) as session:
                file = session.get(GFFFile, gff_file_key)
                if file is None:
                    raise Exception(
                        f"Unexpectedly unable to find GFFFile with key {gff_file_key}"
                    )

            gff_parser = GFFParser(file=file, tool_key=self.tool_key)
            gff_parser.parse(engine)

        logging.info(
            f"Finished adding all prokka GFF files on {self.output_directory} to the database."
        )
