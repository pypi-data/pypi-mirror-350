from pathlib import Path
from typing import ClassVar

from parsomics_core.entities.files.validated_file import ValidatedFileWithGenome


class GFFValidatedFile(ValidatedFileWithGenome):
    # Source: https://en.wikipedia.org/wiki/General_feature_format
    _VALID_FILE_TERMINATIONS: ClassVar[list[str]] = [
        ".gff",
        ".gff3",
    ]

    @property
    def genome_name(self) -> str:
        path_obj = Path(self.path)
        return path_obj.stem
