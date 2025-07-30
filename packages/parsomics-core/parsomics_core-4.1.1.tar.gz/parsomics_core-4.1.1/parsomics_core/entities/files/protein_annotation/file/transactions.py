from sqlmodel import Session, select

from parsomics_core.entities.transactions import Transactions
from parsomics_core.entities.files.protein_annotation.file.models import (
    ProteinAnnotationFile,
    ProteinAnnotationFileCreate,
    ProteinAnnotationFileDemand,
    ProteinAnnotationFilePublic,
)


class ProteinAnnotationFileTransactions(Transactions):
    def __init__(self):
        return super().__init__(
            table_type=ProteinAnnotationFile,
            public_type=ProteinAnnotationFilePublic,
            create_type=ProteinAnnotationFileCreate,
            find_function=ProteinAnnotationFileTransactions._find_statement,
        )

    @staticmethod
    def _find_statement(demand_model: ProteinAnnotationFileDemand):
        return select(ProteinAnnotationFile).where(
            ProteinAnnotationFile.path == demand_model.path,
        )

    def create(
        self, session: Session, create_model: ProteinAnnotationFileCreate
    ) -> ProteinAnnotationFilePublic:
        return super().create(session, create_model)

    def demand(
        self, session: Session, demand_model: ProteinAnnotationFileDemand
    ) -> ProteinAnnotationFilePublic:
        return super().demand(session, demand_model)
