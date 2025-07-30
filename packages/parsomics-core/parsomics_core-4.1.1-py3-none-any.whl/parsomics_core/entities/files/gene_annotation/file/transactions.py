from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.gene_annotation.file.models import (
    GeneAnnotationFile,
    GeneAnnotationFileCreate,
    GeneAnnotationFileDemand,
    GeneAnnotationFilePublic,
)


class GeneAnnotationFileTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=GeneAnnotationFile,
            public_type=GeneAnnotationFilePublic,
            create_type=GeneAnnotationFileCreate,
            find_function=GeneAnnotationFileTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: GeneAnnotationFileDemand):
        return select(GeneAnnotationFile).where(
            GeneAnnotationFile.path == demand_model.path,
        )

    def create(
        self, session: Session, create_model: GeneAnnotationFileCreate
    ) -> GeneAnnotationFilePublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: GeneAnnotationFileDemand
    ) -> GeneAnnotationFilePublic:
        return super().demand(session, demand_model)
