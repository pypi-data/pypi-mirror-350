from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.gene.models import (
    Gene,
    GeneCreate,
    GeneDemand,
    GenePublic,
)


class GeneTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Gene,
            public_type=GenePublic,
            create_type=GeneCreate,
            find_function=GeneTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GeneDemand):
        return select(Gene).where(
            Gene.fasta_entry_key == demand_model.fasta_entry_key,
        )

    def create(self, session: Session, create_model: GeneCreate) -> GenePublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: GeneDemand) -> GenePublic:
        return super().demand(session, demand_model)
