from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.workflow.assembly.models import (
    Assembly,
    AssemblyCreate,
    AssemblyDemand,
    AssemblyPublic,
)


class AssemblyTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Assembly,
            public_type=AssemblyPublic,
            create_type=AssemblyCreate,
            find_function=AssemblyTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: AssemblyDemand):
        return select(Assembly).where(
            Assembly.name == demand_model.name,
        )

    def create(self, session: Session, create_model: AssemblyCreate) -> AssemblyPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: AssemblyDemand) -> AssemblyPublic:
        return super().demand(session, demand_model)
