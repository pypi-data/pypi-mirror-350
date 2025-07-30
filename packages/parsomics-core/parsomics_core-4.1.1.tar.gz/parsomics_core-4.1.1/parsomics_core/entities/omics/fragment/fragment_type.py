from enum import Enum


class FragmentType(str, Enum):

    # Common types
    CDS = "CDS"
    GENE = "GENE"

    # Prokka-only types
    # Source: https://github.com/tseemann/prokka?tab=readme-ov-file#output-files
    RRNA = "RRNA"
    TRNA = "TRNA"
    TMRNA = "TMRNA"
    MISC_RNA = "MISC_RNA"
    REPEAT_REGION = "REPEAT_REGION"

    # Funannotate-only types
    MRNA = "MRNA"
    EXON = "EXON"

    def is_coding(self):
        return self.value == self.CDS or self.value == self.EXON
