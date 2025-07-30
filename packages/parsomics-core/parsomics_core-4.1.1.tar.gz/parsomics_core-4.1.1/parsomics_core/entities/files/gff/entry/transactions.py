from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.gff.entry.models import (
    GFFEntry,
    GFFEntryCreate,
    GFFEntryDemand,
    GFFEntryPublic,
)


class GFFEntryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GFFEntry,
            public_type=GFFEntryPublic,
            create_type=GFFEntryCreate,
            find_function=GFFEntryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GFFEntryDemand):
        return select(GFFEntry).where(
            GFFEntry.file_key == demand_model.file_key,
            GFFEntry.identifier == demand_model.identifier,
        )

    def create(self, session: Session, create_model: GFFEntryCreate) -> GFFEntryPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: GFFEntryDemand) -> GFFEntryPublic:
        return super().demand(session, demand_model)
