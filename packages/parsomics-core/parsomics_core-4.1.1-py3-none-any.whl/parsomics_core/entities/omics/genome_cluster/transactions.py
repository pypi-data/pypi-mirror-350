from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.genome_cluster.models import (
    GenomeCluster,
    GenomeClusterCreate,
    GenomeClusterDemand,
    GenomeClusterPublic,
)


class GenomeClusterTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GenomeCluster,
            public_type=GenomeClusterPublic,
            create_type=GenomeClusterCreate,
            find_function=GenomeClusterTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GenomeClusterDemand):
        return select(GenomeCluster).where(
            GenomeCluster.name == demand_model.name,
            GenomeCluster.drep_directory_key == demand_model.drep_directory_key,
        )

    def create(
        self, session: Session, create_model: GenomeClusterCreate
    ) -> GenomeClusterPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: GenomeClusterDemand
    ) -> GenomeClusterPublic:
        return super().demand(session, demand_model)
