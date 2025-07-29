import logging
from typing import BinaryIO
from rettxmutation.analysis.text_cleaner import TextCleaner
from rettxmutation.analysis.ocr_extractor import OcrExtractor
from rettxmutation.analysis.models import Document
from rettxmutation.analysis.text_analytics import HealthcareTextAnalyzer
from rettxmutation.analysis.openai_rettx_agents import OpenAIRettXAgents
from rettxmutation.analysis.gene_variant_detector import GeneVariantDetector
from rettxmutation.analysis.document_processing import DynamicDocumentPreprocessor
from rettxmutation.services.mutation_service import MutationService

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
            audit_logger=audit_logger
        )
        self.mutation_service = MutationService()

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
