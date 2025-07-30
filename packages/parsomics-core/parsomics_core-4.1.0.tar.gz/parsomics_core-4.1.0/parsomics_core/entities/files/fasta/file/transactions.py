from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.fasta.file.models import (
    FASTAFile,
    FASTAFileCreate,
    FASTAFileDemand,
    FASTAFilePublic,
)


class FASTAFileTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=FASTAFile,
            public_type=FASTAFilePublic,
            create_type=FASTAFileCreate,
            find_function=FASTAFileTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: FASTAFileDemand):
        return select(FASTAFile).where(
            FASTAFile.path == demand_model.path,
        )

    def create(
        self, session: Session, create_model: FASTAFileCreate
    ) -> FASTAFilePublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: FASTAFileDemand
    ) -> FASTAFilePublic:
        return super().demand(session, demand_model)
