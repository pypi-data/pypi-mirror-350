from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.workflow.project.models import (
    Project,
    ProjectCreate,
    ProjectDemand,
    ProjectPublic,
)


class ProjectTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Project,
            public_type=ProjectPublic,
            create_type=ProjectCreate,
            find_function=ProjectTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: ProjectDemand):
        return select(Project).where(
            Project.name == demand_model.name,
        )

    def create(self, session: Session, create_model: ProjectCreate) -> ProjectPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: ProjectDemand) -> ProjectPublic:
        return super().demand(session, demand_model)
