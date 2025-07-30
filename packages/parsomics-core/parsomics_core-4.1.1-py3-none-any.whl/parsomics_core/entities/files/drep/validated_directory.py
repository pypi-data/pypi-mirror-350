from typing import ClassVar

from parsomics_core.entities.files.validated_directory import ValidatedDirectory


class DrepValidatedDirectory(ValidatedDirectory):
    _MUST_CONTAIN_FILES: ClassVar[list[str]] = [
        "Wdb.csv",
        "Cdb.csv",
    ]
