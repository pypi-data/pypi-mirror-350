from typing import Sequence

from parsomics_core.entities.files.file_factory import FileFactory
from parsomics_core.entities.files.gff.validated_file import GFFValidatedFile


class GFFFileFactory(FileFactory):
    def __init__(self, path: str, dereplicated_genomes: Sequence[str] | None = None):
        return super().__init__(
            validation_class=GFFValidatedFile,
            path=path,
            dereplicated_genomes=dereplicated_genomes,
        )
