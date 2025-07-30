from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.gff.file.models import (
    GFFFile,
    GFFFileCreate,
    GFFFileDemand,
    GFFFilePublic,
)


class GFFFileTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GFFFile,
            public_type=GFFFilePublic,
            create_type=GFFFileCreate,
            find_function=GFFFileTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GFFFileDemand):
        return select(GFFFile).where(
            GFFFile.path == demand_model.path,
        )

    def create(self, session: Session, create_model: GFFFileCreate) -> GFFFilePublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: GFFFileDemand) -> GFFFilePublic:
        return super().demand(session, demand_model)
