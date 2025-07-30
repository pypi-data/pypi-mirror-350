from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.genome.models import (
    Genome,
    GenomeCreate,
    GenomeDemand,
    GenomePublic,
)


class GenomeTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Genome,
            public_type=GenomePublic,
            create_type=GenomeCreate,
            find_function=GenomeTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GenomeDemand):
        return select(Genome).where(
            Genome.drep_entry_key == demand_model.drep_entry_key,
        )

    def create(self, session: Session, create_model: GenomeCreate) -> GenomePublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: GenomeDemand) -> GenomePublic:
        return super().demand(session, demand_model)
