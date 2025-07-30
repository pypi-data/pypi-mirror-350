from pathlib import Path
from typing import ClassVar

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class ValidatedFile(SQLModel):
    path: str = Field(index=True)

    _VALID_FILE_TERMINATIONS: ClassVar[list[str]]

    @field_validator("path")
    @classmethod
    def path_must_exist(cls, v: str) -> str:
        path_obj = Path(v)
        if not path_obj.exists():
            message: str = "Value must be a file that exists"
            reason: str = f"'{path_obj.resolve()}' does not exist"
            raise ValueError(f"{message}. {reason}")
        return v

    @field_validator("path")
    @classmethod
    def path_must_be_a_file(cls, v: str) -> str:
        path_obj = Path(v)
        if not path_obj.is_file():
            message: str = "Value must be a file"
            reason: str = f"Given value '{v}' is a directory"
            raise ValueError(f"{message}. {reason}")
        return v

    @field_validator("path")
    @classmethod
    def path_must_have_a_valid_extension(cls, v: str) -> str:
        path_obj = Path(v)
        if not any(path_obj.name.endswith(s) for s in cls._VALID_FILE_TERMINATIONS):
            message: str = "Value must have a valid file termination."
            reason: str = (
                f"Given file name '{path_obj.name}' ends with none of {cls._VALID_FILE_TERMINATIONS}"
            )
            raise ValueError(f"{message}. {reason}")
        return v


class ValidatedFileWithGenome(ValidatedFile):
    @property
    def genome_name(self) -> str:
        raise NotImplementedError("Please implement this method in a subclass")
