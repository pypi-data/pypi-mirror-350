import logging
from typing import Dict, Any, List
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from rettxmutation.analysis.models import Keyword


logger = logging.getLogger(__name__)


class HealthcareTextAnalyzer:
    """
    Uses Azure Text Analytics for Health to analyze and extract medical entities,
    focusing on genetic variants, genes, and mutation types.
    """

    def __init__(self, endpoint: str, key: str):
        self._client = TextAnalyticsClient(endpoint=endpoint,
                                           credential=AzureKeyCredential(key))

    def analyze_text(self, text: str) -> Any:
        """
        Analyze text using Azure Healthcare Entities.
        """
        try:
            logger.debug("Analyzing text with Healthcare Entities")

            documents = [text]
            poller = self._client.begin_analyze_healthcare_entities(documents)
            result = poller.result()

            # Filter out errored documents
            docs = [doc for doc in result if not doc.is_error]
            if not docs:
                logger.error("No valid documents found for analysis")
                return None

            # We only submitted one document, so docs[0] is the result
            return docs[0]

        except Exception as e:
            logger.error(f"Error during healthcare text analysis: {e}")
            raise

    def extract_variant_information(
        self, doc: Any, confidence_threshold: float = 0.5
    ) -> List[Keyword]:
        """
        Extract unique genetic variants from the document based on a confidence threshold.
        Return a list of `Keyword` objects.
        """
        if not doc:
            return []

        seen_variants = set()
        variants = []

        for entity in doc.entities:
            if entity.category == "Variant" and entity.confidence_score >= confidence_threshold:
                if entity.text not in seen_variants:
                    seen_variants.add(entity.text)
                    variants.append(
                        Keyword(
                            value=entity.text,
                            type="variant",
                            count=1,
                            confidence=entity.confidence_score
                        )
                    )

        return variants

    def extract_genetic_information(self, doc: Any) -> Dict[str, Any]:
        """
        Extract relevant genetic information from the healthcare entities.
        """
        if not doc:
            return {
                "variants": [],
                "genes": [],
                "mutation_types": [],
                "relations": []
            }

        relevant_data = {
            "variants": [],
            "genes": [],
            "mutation_types": [],
            "relations": []
        }

        relevant_categories = {"Variant", "GeneOrProtein", "MutationType"}

        # Gather relevant entities
        for entity in doc.entities:
            if entity.category == "Variant":
                relevant_data["variants"].append({
                    "text": entity.text,
                    "normalized_text": entity.normalized_text,
                    "confidence_score": entity.confidence_score
                })
            elif entity.category == "GeneOrProtein":
                relevant_data["genes"].append({
                    "text": entity.text,
                    "normalized_text": entity.normalized_text,
                    "confidence_score": entity.confidence_score
                })
            elif entity.category == "MutationType":
                relevant_data["mutation_types"].append({
                    "text": entity.text,
                    "normalized_text": entity.normalized_text,
                    "confidence_score": entity.confidence_score
                })

        # Process relations
        for relation in doc.entity_relations:
            if any(role.entity.category in relevant_categories for role in relation.roles):
                rel_info = {
                    "relation_type": relation.relation_type,
                    "roles": []
                }
                for role in relation.roles:
                    rel_info["roles"].append({
                        "role_name": role.name,
                        "entity_text": role.entity.text,
                        "entity_category": role.entity.category
                    })
                relevant_data["relations"].append(rel_info)

        return relevant_data
