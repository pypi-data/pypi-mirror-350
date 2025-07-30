from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.fragment.models import (
    Fragment,
    FragmentCreate,
    FragmentDemand,
    FragmentPublic,
)


class FragmentTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=Fragment,
            public_type=FragmentPublic,
            create_type=FragmentCreate,
            find_function=FragmentTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: FragmentDemand):
        return select(Fragment).where(
            Fragment.gff_entry_key == demand_model.gff_entry_key,
        )

    def create(self, session: Session, create_model: FragmentCreate) -> FragmentPublic:
        return super().create(session, create_model)

    def demand(self, session: Session, demand_model: FragmentDemand) -> FragmentPublic:
        return super().demand(session, demand_model)
