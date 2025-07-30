from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.workflow.metadata.models import (
    Metadata,
    MetadataCreate,
    MetadataDemand,
    MetadataPublic,
)


class MetadataTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Metadata,
            public_type=MetadataPublic,
            create_type=MetadataCreate,
            find_function=MetadataTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(_: MetadataDemand):
        return select(Metadata).where(
            Metadata.key == 1,
        )

    def create(self, session: Session, create_model: MetadataCreate) -> MetadataPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: MetadataDemand) -> MetadataPublic:
        return super().demand(session, demand_model)
