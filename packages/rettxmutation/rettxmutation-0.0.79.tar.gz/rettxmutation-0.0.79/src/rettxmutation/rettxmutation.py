import logging
from typing import BinaryIO, List, Dict, Any
from rettxmutation.analysis.text_cleaner import TextCleaner
from rettxmutation.analysis.ocr_extractor import OcrExtractor
from rettxmutation.analysis.models import Document
from rettxmutation.analysis.text_analytics import HealthcareTextAnalyzer
from rettxmutation.analysis.openai_rettx_agents import OpenAIRettXAgents
from rettxmutation.analysis.gene_variant_detector import GeneVariantDetector
from rettxmutation.analysis.document_processing import DynamicDocumentPreprocessor
from rettxmutation.services.mutation_service import MutationService
from rettxmutation.services.embedding_service import EmbeddingService
from rettxmutation.services.gene_mutation_tokenizer import HgvsMutationTokenizer
from rettxmutation.models.gene_models import GeneMutation
from rettxmutation.models.mutation_model import Mutation

import numpy as np

logger = logging.getLogger(__name__)


class RettXDocumentAnalysis:
    """
    High-level orchestrator that uses the various sub-components
    for a full end-to-end document analysis workflow.
    """
    def __init__(
        self,
        doc_analysis_endpoint: str,
        doc_analysis_key: str,
        cognitive_services_endpoint: str,
        cognitive_services_key: str,
        openai_key: str,
        openai_model_version: str,
        openai_endpoint: str,
        openai_model_name: str,
        embedding_deployment: str,
        binarize: bool = False,
        sharpen: bool = False,
        contrast_threshold: float = 25.0,
        audit_logger = None,
    ):
        # Initialize sub-components
        self.ocr_extractor = OcrExtractor(doc_analysis_endpoint, doc_analysis_key)
        self.text_cleaner = TextCleaner()
        self.gene_variant_detector = GeneVariantDetector()
        self.health_analyzer = HealthcareTextAnalyzer(cognitive_services_endpoint,
                                                      cognitive_services_key)
        self.openai_mutation_extractor = OpenAIRettXAgents(
            api_key=openai_key,
            api_version=openai_model_version,
            azure_endpoint=openai_endpoint,
            model_name=openai_model_name,
            embedding_deployment=embedding_deployment,
            audit_logger=audit_logger
        )
        self.mutation_service = MutationService()        # Initialize the embedding service
        self.embedding_service = EmbeddingService(embedding_model=embedding_deployment)

        # Initialize the image preprocessor
        self.file_preprocessor = DynamicDocumentPreprocessor(
            binarize=binarize,
            sharpen=sharpen,
            contrast_threshold=contrast_threshold)

        # Audit logger
        self._audit_logger = audit_logger

    def preprocess_image(self,
                         audit_context,
                         file_stream: BinaryIO,
                         binarize: bool,
                         sharpen: bool,
                         contrast_threshold: float) -> BinaryIO:
        """
        Preprocess image files to improve OCR accuracy.
        The input is a file stream, the output is a preprocessed image.
        """
        if file_stream is None:
            logger.error("File stream is None, cannot preprocess image.")
            return None
        return self.file_preprocessor.preprocess_image(file_stream, binarize, sharpen, contrast_threshold)

    def extract_text(self,
                     audit_context,
                     file_stream: BinaryIO) -> Document:
        """
        Extract text from the document using OCR, clean it, and detect gene variants.
        """
        document = self.ocr_extractor.extract_text(file_stream)
        document.cleaned_text = self.text_cleaner.clean_ocr_text(document.raw_text)
        document.keywords = self.gene_variant_detector.detect_mecp2_keywords(document.cleaned_text)

        # Validate what was the OCR confidence score of the detected keywords
        for keyword in document.keywords:
            confidence_value = document.find_word_confidence(keyword.value)
            if confidence_value is not None:
                logger.debug(f"Found {keyword} with confidence {confidence_value}")
                keyword.confidence = confidence_value
            else:
                logger.warning(f"{keyword} was not found")
                keyword.confidence = 0.0
        logger.debug(f"Mecp2 keyword confidence {document.keywords}")

        return document

    def summarize_and_correct(self,
                              audit_context,
                              document: Document) -> Document:
        """
        Summarize the text and correct it based on additional insights.
        Gets additional insights from Azure Healthcare Text Analytics.
        """
        # Summarize the text using OpenAI powered agent
        document.summary = self.openai_mutation_extractor.summarize_report(
            audit_context=audit_context,
            document_text=document.cleaned_text,
            keywords=document.dump_keywords())
        logger.debug(f"OpenAI summary: {document.summary}")

        # Analyze with Azure healthcare text analytics
        doc_analysis_result = self.health_analyzer.analyze_text(document.summary)
        document.text_analytics_result = self.health_analyzer.extract_variant_information(
            doc_analysis_result,
            confidence_threshold=0.0)
        logger.debug(f"TA4H: {document.text_analytics_result}")

        # Correct the summary with additional inputs from TA4H
        corrected_summary = self.openai_mutation_extractor.correct_summary_mistakes(
            audit_context=audit_context,
            document_text=document.summary,
            keywords=document.dump_keywords(),
            text_analytics=document.dump_text_analytics_keywords())
        logger.debug(f"Corrected summary: {corrected_summary}")
        return corrected_summary

    def mutation_to_embedding_string(self, mutation: GeneMutation) -> str:
        """
        Convert a GeneMutation object to a string representation suitable for embedding.
        
        Args:
            mutation (GeneMutation): The mutation object to convert
            
        Returns:
            str: String representation of the mutation
        """
        return self.embedding_service.mutation_to_embedding_string(mutation)

    def create_mutation_embedding(self, mutation: GeneMutation) -> np.ndarray:
        """
        Create an embedding vector for a single GeneMutation object.

        Args:
            mutation (GeneMutation): The mutation to convert to an embedding
            
        Returns:
            np.ndarray: Embedding vector
        """
        return self.embedding_service.create_embedding(mutation)

    def create_mutation_embeddings(self, mutations: List[GeneMutation]) -> List[np.ndarray]:
        """
        Create embedding vectors for multiple GeneMutation objects.
        
        Args:
            mutations (List[GeneMutation]): List of mutations to convert to embeddings
            
        Returns:
            List[np.ndarray]: List of embedding vectors
        """
        return self.embedding_service.create_embeddings(mutations)

    def parse_hgvs_string(self, hgvs_string: str) -> Mutation:
        """
        Parse an HGVS string and create a Mutation object.
        
        Args:
            hgvs_string (str): The HGVS string to parse
            
        Returns:
            Mutation: Parsed mutation object
        """
        return self.embedding_service.parse_hgvs_string(hgvs_string)

    def find_similar_mutations(
        self, 
        query_mutation: GeneMutation,
        mutation_library: List[GeneMutation],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find mutations similar to the query mutation in the provided library.
        
        Args:
            query_mutation (GeneMutation): The mutation to find similar mutations for
            mutation_library (List[GeneMutation]): The library of mutations to search
            top_k (int, optional): The number of similar mutations to return. Defaults to 5.
            
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing mutations and similarity scores        """
        return self.embedding_service.find_similar_mutations(
            query_mutation=query_mutation,
            mutation_library=mutation_library,
            top_k=top_k
        )

    def tokenize(self, gene_mutation: GeneMutation) -> str:
        """
        Tokenize a GeneMutation object for free text search.
        
        Args:
            gene_mutation (GeneMutation): The mutation to tokenize
            
        Returns:
            str: Space-separated tokens suitable for free text search
        """
        return HgvsMutationTokenizer.tokenize(gene_mutation)
