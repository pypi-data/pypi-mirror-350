import logging

from Bio import SeqIO
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from parsomics_core.entities.files.fasta.entry.models import FASTAEntry
from parsomics_core.entities.files.fasta.file.models import FASTAFile


class FASTAParser(BaseModel):
    file: FASTAFile

    def _remove_first_word(self, s: str) -> str | None:
        result = None
        if len(s.split()) > 1:
            result = s.split(maxsplit=1)[1]
        return result

    def parse(self, engine: Engine) -> None:
        mappings: list[dict] = []
        with open(self.file.path) as handle:
            for record in SeqIO.parse(handle, "fasta"):

                file_key = self.file.key
                sequence_name = (
                    record.id if record.id else record.description.split()[0]
                )
                description = self._remove_first_word(record.description)
                sequence = str(record.seq)

                mappings.append(
                    {
                        "file_key": file_key,
                        "sequence_name": sequence_name,
                        "description": description,
                        "sequence": sequence,
                    }
                )

        with Session(engine) as session:
            try:
                session.bulk_insert_mappings(FASTAEntry, mappings)
                session.commit()
                logging.info(
                    f"Added FASTA entries from {self.file.path} to the database."
                )
            except IntegrityError as e:
                logging.warning(
                    f"Failed to add FASTA entries from {self.file.path} to "
                    f"the database. Exception caught: {e}"
                )
