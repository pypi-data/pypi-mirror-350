from .document import Document
from .gene_models import GeneMutation


class AnalysisContext:
    """
    Object that holds the context of the analysis, including the input file, patient information, and other relevant data.
    It is used to pass data between different parts of the analysis pipeline.
    """
    genetic_document: Document
    patient_info: dict 
    gene_mutations: list[GeneMutation]
