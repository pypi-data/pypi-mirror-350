from pathlib import Path
from typing import ClassVar

from pydantic import field_validator
from sqlmodel import SQLModel


class ValidatedDirectory(SQLModel):
    path: str

    _MUST_CONTAIN_FILES: ClassVar[list[str]]

    @field_validator("path")
    @classmethod
    def path_must_exist(cls, v: str) -> str:
        path_obj = Path(v)
        if not path_obj.exists():
            message: str = "Path must exist"
            reason: str = f"'{path_obj.resolve()}' does not exist"
            raise ValueError(f"{message}. {reason}")
        return v

    @field_validator("path")
    @classmethod
    def path_must_a_directory(cls, v: str) -> str:
        path_obj = Path(v)
        if not path_obj.is_dir():
            message: str = "Path must be a directory"
            reason: str = f"'{path_obj.resolve()}' is not a directory"
            raise ValueError(f"{message}. {reason}")
        return v

    @field_validator("path")
    @classmethod
    def path_must_contain_files(cls, v: str) -> str:
        path_obj = Path(v)
        missing_files = [
            file for file in cls._MUST_CONTAIN_FILES if not (path_obj / file).exists()
        ]

        if missing_files:
            message: str = "Path must have all files in _MUST_CONTAIN_FILES"
            reason: str = f"Files {missing_files} are missing"
            raise ValueError(f"{message}. {reason}")

        return v


class ValidatedDirectoryWithGenome(ValidatedDirectory):
    @property
    def genome_name(self) -> str:
        raise NotImplementedError("Please implement this method in a subclass")
