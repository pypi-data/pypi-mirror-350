import logging

from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session

from parsomics_core.entities.files.drep.directory.models import (
    DrepDirectory,
    DrepDirectoryDemand,
)
from parsomics_core.entities.files.drep.directory.transactions import (
    DrepDirectoryTransactions,
)
from parsomics_core.entities.files.drep.parser import DrepDirectoryParser


class DrepOutputProcessor(BaseModel):
    output_directory: str
    run_key: int

    def process_drep_directory(self, engine: Engine):
        run_key = self.run_key

        drep_directory_demand_model = DrepDirectoryDemand(
            path=self.output_directory,
            run_key=run_key,
        )

        with Session(engine) as session:
            drep_directory: DrepDirectory = DrepDirectory.model_validate(
                DrepDirectoryTransactions().demand(
                    session,
                    drep_directory_demand_model,
                )
            )

        drep_directory_parser = DrepDirectoryParser(directory=drep_directory)
        drep_directory_parser.parse(engine)

        logging.info(
            f"Finished adding all dRep files on {self.output_directory} to the database."
        )
