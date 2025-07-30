import logging
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session

from parsomics_core.entities.files.gtdbtk.file.models import (
    GTDBTkFile,
    GTDBTkFileDemand,
)
from parsomics_core.entities.files.gtdbtk.file.transactions import (
    GTDBTkFileTransactions,
)
from parsomics_core.entities.files.gtdbtk.file_factory import GTDBTkFileFactory
from parsomics_core.entities.files.gtdbtk.parser import GTDBTkParser
from parsomics_core.entities.files.gtdbtk.validated_file import GTDBTkValidatedFile


class GTDBTkOutputProcessor(BaseModel):
    output_directory: str
    dereplicated_genomes: Sequence[str]
    assembly_key: int
    run_key: int
    tool_key: int

    def process_gtdbtk_files(self, engine: Engine):
        gtdbtk_file_factory: GTDBTkFileFactory = GTDBTkFileFactory(
            self.output_directory,
            self.dereplicated_genomes,
        )

        gtdbtk_files: list[GTDBTkValidatedFile] = gtdbtk_file_factory.assemble()
        for f in gtdbtk_files:
            run_key = self.run_key

            gtdbtk_file_demand_model = GTDBTkFileDemand(
                path=f.path,
                run_key=run_key,
            )

            with Session(engine) as session:
                gtdbtk_file: GTDBTkFile = GTDBTkFile.model_validate(
                    GTDBTkFileTransactions().demand(
                        session,
                        gtdbtk_file_demand_model,
                    )
                )

            gtdbtk_parser = GTDBTkParser(
                file=gtdbtk_file,
                assembly_key=self.assembly_key,
                tool_key=self.tool_key,
            )
            gtdbtk_parser.parse(engine)

        logging.info(
            f"Finished adding all GTDBTk files on {self.output_directory} to the database."
        )
