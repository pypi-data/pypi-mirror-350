from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.omics.fragment_protein_link.models import (
    FragmentProteinLink,
    FragmentProteinLinkCreate,
    FragmentProteinLinkDemand,
    FragmentProteinLinkPublic,
)


class FragmentProteinLinkTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=FragmentProteinLink,
            public_type=FragmentProteinLinkPublic,
            create_type=FragmentProteinLinkCreate,
            find_function=FragmentProteinLinkTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: FragmentProteinLinkDemand):
        return select(FragmentProteinLink).where(
            FragmentProteinLink.fragment_key == demand_model.fragment_key,
            FragmentProteinLink.protein_key == demand_model.protein_key,
        )

    def create(
        self, session: Session, create_model: FragmentProteinLinkCreate
    ) -> FragmentProteinLinkPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: FragmentProteinLinkDemand
    ) -> FragmentProteinLinkPublic:
        return super().demand(session, demand_model)
