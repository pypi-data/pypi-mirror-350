from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.gtdbtk.file.models import (
    GTDBTkFile,
    GTDBTkFileCreate,
    GTDBTkFileDemand,
    GTDBTkFilePublic,
)


class GTDBTkFileTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GTDBTkFile,
            public_type=GTDBTkFilePublic,
            create_type=GTDBTkFileCreate,
            find_function=GTDBTkFileTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GTDBTkFileDemand):
        return select(GTDBTkFile).where(
            GTDBTkFile.path == demand_model.path,
        )

    def create(
        self, session: Session, create_model: GTDBTkFileCreate
    ) -> GTDBTkFilePublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: GTDBTkFileDemand
    ) -> GTDBTkFilePublic:
        return super().demand(session, demand_model)
