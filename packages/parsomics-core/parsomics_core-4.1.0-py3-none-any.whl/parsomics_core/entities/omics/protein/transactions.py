from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.protein.models import (
    Protein,
    ProteinCreate,
    ProteinDemand,
    ProteinPublic,
)


class ProteinTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Protein,
            public_type=ProteinPublic,
            create_type=ProteinCreate,
            find_function=ProteinTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: ProteinDemand):
        return select(Protein).where(
            Protein.fasta_entry_key == demand_model.fasta_entry_key,
        )

    def create(self, session: Session, create_model: ProteinCreate) -> ProteinPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: ProteinDemand) -> ProteinPublic:
        return super().demand(session, demand_model)
