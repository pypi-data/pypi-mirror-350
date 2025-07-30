from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.workflow.run.models import (
    Run,
    RunCreate,
    RunDemand,
    RunPublic,
)


class RunTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Run,
            public_type=RunPublic,
            create_type=RunCreate,
            find_function=RunTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: RunDemand):
        return select(Run).where(
            Run.output_directory == demand_model.output_directory,
        )

    def create(self, session: Session, create_model: RunCreate) -> RunPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: RunDemand) -> RunPublic:
        return super().demand(session, demand_model)
