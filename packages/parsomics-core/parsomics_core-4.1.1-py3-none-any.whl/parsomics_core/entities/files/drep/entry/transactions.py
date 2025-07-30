from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.drep.entry.models import (
    DrepEntry,
    DrepEntryCreate,
    DrepEntryDemand,
    DrepEntryPublic,
)


class DrepEntryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=DrepEntry,
            public_type=DrepEntryPublic,
            create_type=DrepEntryCreate,
            find_function=DrepEntryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: DrepEntryDemand):
        return select(DrepEntry).where(
            DrepEntry.genome_name == demand_model.genome_name,
            DrepEntry.directory_key == demand_model.directory_key,
        )

    def create(
        self, session: Session, create_model: DrepEntryCreate
    ) -> DrepEntryPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: DrepEntryDemand
    ) -> DrepEntryPublic:
        return super().demand(session, demand_model)
