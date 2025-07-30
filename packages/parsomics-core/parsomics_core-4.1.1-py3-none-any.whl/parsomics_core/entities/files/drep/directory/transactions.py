from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.drep.directory.models import (
    DrepDirectory,
    DrepDirectoryCreate,
    DrepDirectoryDemand,
    DrepDirectoryPublic,
)


class DrepDirectoryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=DrepDirectory,
            public_type=DrepDirectoryPublic,
            create_type=DrepDirectoryCreate,
            find_function=DrepDirectoryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: DrepDirectoryDemand):
        return select(DrepDirectory).where(
            DrepDirectory.path == demand_model.path,
        )

    def create(
        self, session: Session, create_model: DrepDirectoryCreate
    ) -> DrepDirectoryPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: DrepDirectoryDemand
    ) -> DrepDirectoryPublic:
        return super().demand(session, demand_model)
