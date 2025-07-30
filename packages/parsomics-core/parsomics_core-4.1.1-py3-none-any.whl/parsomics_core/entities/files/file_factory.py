import logging
import os
from pathlib import Path
from typing import Sequence

from pydantic import BaseModel

from parsomics_core.entities.files.validated_file import ValidatedFileWithGenome


class FileFactory(BaseModel):
    path: str
    validation_class: type
    dereplicated_genomes: Sequence[str]

    def _needs_validation(self, file_path_obj):
        return (
            not issubclass(self.validation_class, ValidatedFileWithGenome)
            or any(
                file_path_obj.name.startswith(genome + ".")
                for genome in self.dereplicated_genomes
            )
            or any(
                file_path_obj.name.startswith(genome + "_")
                for genome in self.dereplicated_genomes
            )
        )

    def assemble(self) -> list:
        directory_path_obj = Path(self.path).resolve()
        relevant_files: list = []

        for root, _, files in os.walk(directory_path_obj):
            for file in files:
                file_path_obj = Path(os.path.join(root, file)).resolve()

                if self._needs_validation(file_path_obj):

                    # NOTE: we rely on the field validators of the file classes to
                    #       make sure we only create objects for valid files

                    try:
                        relevant_file = self.validation_class(path=str(file_path_obj))
                        relevant_files.append(relevant_file)
                        logging.debug(f"Listed file {file_path_obj}")
                    except ValueError:
                        logging.debug(f"Ignored file {file_path_obj}")

        return relevant_files
