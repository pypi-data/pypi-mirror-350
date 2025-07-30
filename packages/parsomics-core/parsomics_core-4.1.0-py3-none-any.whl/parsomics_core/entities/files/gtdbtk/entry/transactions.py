from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.gtdbtk.entry.models import (
    GTDBTkEntry,
    GTDBTkEntryCreate,
    GTDBTkEntryDemand,
    GTDBTkEntryPublic,
)


class GTDBTkEntryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GTDBTkEntry,
            public_type=GTDBTkEntryPublic,
            create_type=GTDBTkEntryCreate,
            find_function=GTDBTkEntryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GTDBTkEntryDemand):
        return select(GTDBTkEntry).where(
            GTDBTkEntry.file_key == demand_model.file_key,
            GTDBTkEntry.genome_key == demand_model.genome_key,
        )

    def create(
        self, session: Session, create_model: GTDBTkEntryCreate
    ) -> GTDBTkEntryPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: GTDBTkEntryDemand
    ) -> GTDBTkEntryPublic:
        return super().demand(session, demand_model)
