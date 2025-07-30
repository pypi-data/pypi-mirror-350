from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.sample.models import (
    Sample,
    SampleCreate,
    SampleDemand,
    SamplePublic,
)


class SampleTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Sample,
            public_type=SamplePublic,
            create_type=SampleCreate,
            find_function=SampleTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: SampleDemand):
        return select(Sample).where(
            Sample.name == demand_model.name,
        )

    def create(self, session: Session, create_model: SampleCreate) -> SamplePublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: SampleDemand) -> SamplePublic:
        return super().demand(session, demand_model)
