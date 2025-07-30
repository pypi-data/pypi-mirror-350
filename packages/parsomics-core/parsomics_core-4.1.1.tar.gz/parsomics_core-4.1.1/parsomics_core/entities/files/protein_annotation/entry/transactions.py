from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.protein_annotation.entry.models import (
    ProteinAnnotationEntry,
    ProteinAnnotationEntryCreate,
    ProteinAnnotationEntryDemand,
    ProteinAnnotationEntryPublic,
)


class ProteinAnnotationEntryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=ProteinAnnotationEntry,
            public_type=ProteinAnnotationEntryPublic,
            create_type=ProteinAnnotationEntryCreate,
            find_function=ProteinAnnotationEntryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: ProteinAnnotationEntryDemand):
        return select(ProteinAnnotationEntry).where(
            ProteinAnnotationEntry.protein_key == demand_model.protein_key,
            ProteinAnnotationEntry.coord_start == demand_model.coord_start,
            ProteinAnnotationEntry.coord_stop == demand_model.coord_stop,
            ProteinAnnotationEntry.description == demand_model.description,
            ProteinAnnotationEntry.file_key == demand_model.file_key,
            ProteinAnnotationEntry.source_key == demand_model.source_key,
        )

    def create(
        self, session: Session, create_model: ProteinAnnotationEntryCreate
    ) -> ProteinAnnotationEntryPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: ProteinAnnotationEntryDemand
    ) -> ProteinAnnotationEntryPublic:
        return super().demand(session, demand_model)
