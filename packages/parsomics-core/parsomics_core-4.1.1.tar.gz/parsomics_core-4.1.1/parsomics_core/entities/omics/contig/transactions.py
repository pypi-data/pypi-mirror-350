from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.contig.models import (
    Contig,
    ContigCreate,
    ContigDemand,
    ContigPublic,
)


class ContigTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Contig,
            public_type=ContigPublic,
            create_type=ContigCreate,
            find_function=ContigTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: ContigDemand):
        return select(Contig).where(
            Contig.fasta_entry_key == demand_model.fasta_entry_key,
        )

    def create(self, session: Session, create_model: ContigCreate) -> ContigPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: ContigDemand) -> ContigPublic:
        return super().demand(session, demand_model)
