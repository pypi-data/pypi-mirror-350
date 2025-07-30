from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.repeated_region.models import (
    RepeatedRegion,
    RepeatedRegionCreate,
    RepeatedRegionDemand,
    RepeatedRegionPublic,
)


class RepeatedRegionTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=RepeatedRegion,
            public_type=RepeatedRegionPublic,
            create_type=RepeatedRegionCreate,
            find_function=RepeatedRegionTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: RepeatedRegionDemand):
        return select(RepeatedRegion).where(
            RepeatedRegion.gff_entry_key == demand_model.gff_entry_key,
        )

    def create(
        self, session: Session, create_model: RepeatedRegionCreate
    ) -> RepeatedRegionPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: RepeatedRegionDemand
    ) -> RepeatedRegionPublic:
        return super().demand(session, demand_model)
