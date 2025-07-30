from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.workflow.tool.models import (
    Tool,
    ToolCreate,
    ToolDemand,
    ToolPublic,
)


class ToolTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Tool,
            public_type=ToolPublic,
            create_type=ToolCreate,
            find_function=ToolTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: ToolDemand):
        return select(Tool).where(
            Tool.name == demand_model.name,
        )

    def create(self, session: Session, create_model: ToolCreate) -> ToolPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: ToolDemand) -> ToolPublic:
        return super().demand(session, demand_model)
