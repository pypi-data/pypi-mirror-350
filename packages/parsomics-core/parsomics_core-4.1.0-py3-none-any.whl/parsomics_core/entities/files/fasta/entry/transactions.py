from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.fasta.entry.models import (
    FASTAEntry,
    FASTAEntryCreate,
    FASTAEntryDemand,
    FASTAEntryPublic,
)


class FASTAEntryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=FASTAEntry,
            public_type=FASTAEntryPublic,
            create_type=FASTAEntryCreate,
            find_function=FASTAEntryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: FASTAEntryDemand):
        return select(FASTAEntry).where(
            FASTAEntry.sequence_name == demand_model.sequence_name,
            FASTAEntry.file_key == demand_model.file_key,
        )

    def create(
        self, session: Session, create_model: FASTAEntryCreate
    ) -> FASTAEntryPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: FASTAEntryDemand
    ) -> FASTAEntryPublic:
        return super().demand(session, demand_model)
