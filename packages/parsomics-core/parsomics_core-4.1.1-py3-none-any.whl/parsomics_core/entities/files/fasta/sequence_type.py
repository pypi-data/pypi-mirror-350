from enum import Enum


class SequenceType(str, Enum):
    GENE = "GENE"
    CONTIG = "CONTIG"
    PROTEIN = "PROTEIN"
