from pathlib import Path
from typing import ClassVar

from pydantic import field_validator

from parsomics_core.entities.files.validated_file import ValidatedFileWithGenome
from parsomics_core.entities.files.fasta.sequence_type import SequenceType


class FASTAValidatedFile(ValidatedFileWithGenome):
    _VALID_FILE_TERMINATIONS: ClassVar[list[str]] = [
        ".fasta",
        ".fas",
        ".fna",
        ".ffn",
        ".faa",
        ".fa",
        ".mpfa",
        ".frn",
    ]

    _VALID_UNAMBIGUOUS_FILE_TERMINATIONS: ClassVar[list[str]] = [
        ".fna",
        ".ffn",
        ".faa",
    ]

    @field_validator("path")
    @classmethod
    def path_must_have_an_unambiguous_extension(cls, v: str) -> str:
        path_obj = Path(v)
        if not any(
            path_obj.name.endswith(s) for s in cls._VALID_UNAMBIGUOUS_FILE_TERMINATIONS
        ):
            message: str = "Value has ambiguous extension."
            reason: str = (
                f"Please rename the file such that its extension is either \
                '.fna', '.ffn', or '.faa'"
            )
            raise ValueError(f"{message}. {reason}")
        return v

    @property
    def genome_name(self) -> str:
        path_obj = Path(self.path)
        return path_obj.stem

    @property
    def _sequence_type(self) -> SequenceType:
        extension: str = Path(self.path).suffix
        extension_to_sequence_type: dict[str, SequenceType] = {
            ".ffn": SequenceType.GENE,
            ".fna": SequenceType.CONTIG,
            ".faa": SequenceType.PROTEIN,
        }
        return extension_to_sequence_type[extension]
