from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.workflow.source.models import (
    Source,
    SourceCreate,
    SourceDemand,
    SourcePublic,
)


class SourceTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Source,
            public_type=SourcePublic,
            create_type=SourceCreate,
            find_function=SourceTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: SourceDemand):
        return select(Source).where(
            Source.name == demand_model.name,
            Source.version == demand_model.version,
        )

    def create(self, session: Session, create_model: SourceCreate) -> SourcePublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: SourceDemand) -> SourcePublic:
        return super().demand(session, demand_model)
