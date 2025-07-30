from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.gene_annotation.entry.models import (
    GeneAnnotationEntry,
    GeneAnnotationEntryCreate,
    GeneAnnotationEntryDemand,
    GeneAnnotationEntryPublic,
)


class GeneAnnotationEntryTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GeneAnnotationEntry,
            public_type=GeneAnnotationEntryPublic,
            create_type=GeneAnnotationEntryCreate,
            find_function=GeneAnnotationEntryTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GeneAnnotationEntryDemand):
        return select(GeneAnnotationEntry).where(
            GeneAnnotationEntry.gene_key == demand_model.gene_key,
            GeneAnnotationEntry.coord_start == demand_model.coord_start,
            GeneAnnotationEntry.coord_stop == demand_model.coord_stop,
            GeneAnnotationEntry.description == demand_model.description,
            GeneAnnotationEntry.file_key == demand_model.file_key,
            GeneAnnotationEntry.source_key == demand_model.source_key,
        )

    def create(
        self, session: Session, create_model: GeneAnnotationEntryCreate
    ) -> GeneAnnotationEntryPublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: GeneAnnotationEntryDemand
    ) -> GeneAnnotationEntryPublic:
        return super().demand(session, demand_model)
