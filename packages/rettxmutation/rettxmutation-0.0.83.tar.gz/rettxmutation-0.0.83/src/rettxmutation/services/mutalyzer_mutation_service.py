# File: services/mutalyzer_mutation_service.py
import logging
from rettxmutation.services.mutation_service_interface import IStandardMutationService
from rettxmutation.adapters.mutalyzer_mutation_adapter import MutalyzerMutationAdapter, MutationMappingError, MutationNormalizationError
from rettxmutation.models.gene_models import CoreGeneMutation

logger = logging.getLogger(__name__)

class MutalyzerStandardMutationService(IStandardMutationService):
    """
    Concrete implementation of IStandardMutationService using the Mutalyzer API.

    This service:
      - Maps an input mutation string (e.g., "NM_001110792.2:c.952C>T") to the canonical transcript
        (default "NM_004992.4") and the alternate transcript (default "NM_001110792.2").
      - Normalizes the canonical representation to extract the genomic coordinate, protein consequence,
        and other fields.
      - Returns a standardized CoreGeneMutation domain model.
    """
    def __init__(self,
                 canonical_transcript: str = "NM_004992.4",
                 alternate_transcript: str = "NM_001110792.2",
                 target_assembly: str = "GRCH38",
                 map_base_url: str = "https://mutalyzer.nl/api/map/",
                 norm_base_url: str = "https://mutalyzer.nl/api/normalize/"):
        self.canonical_transcript = canonical_transcript
        self.alternate_transcript = alternate_transcript
        self.target_assembly = target_assembly
        # Create an instance of our low-level Mutalyzer API client.
        self.service = MutalyzerMutationAdapter(
            target_assembly=target_assembly,
            map_base_url=map_base_url,
            norm_base_url=norm_base_url
        )

    def get_core_mutation(self, input_hgvs: str) -> CoreGeneMutation:
        """
        Convert an input HGVS string into a standardized CoreGeneMutation.

        Parameters:
            input_hgvs (str): A mutation string in HGVS format (e.g., "NM_001110792.2:c.952C>T")

        Returns:
            CoreGeneMutation: The standardized mutation object.

        Raises:
            Exception: If any mapping or normalization step fails.
        """
        try:
            # Map to canonical transcript if necessary.
            if not input_hgvs.startswith(self.canonical_transcript):
                canonical_hgvs = self.service.map_mutation(input_hgvs, self.canonical_transcript)
            else:
                canonical_hgvs = input_hgvs

            # Map to alternate transcript if necessary.
            if not input_hgvs.startswith(self.alternate_transcript):
                alternate_hgvs = self.service.map_mutation(input_hgvs, self.alternate_transcript)
            else:
                alternate_hgvs = input_hgvs

            # Normalize the canonical representation to obtain additional details.
            norm_response = self.service.normalize_mutation(canonical_hgvs)
            chrom_desc = norm_response.get("chromosomal_descriptions", [])
            genomic_coordinate = next(
                (entry.get("g") for entry in chrom_desc if entry.get("assembly") == self.target_assembly),
                None
            )
            if not genomic_coordinate:
                raise Exception("Genomic coordinate not found in normalization response.")

            protein_info = norm_response.get("protein", {})
            protein_consequence = protein_info.get("description")
            mane_tag = next(
                (entry.get("tag", {}).get("details") for entry in chrom_desc if entry.get("tag")),
                None
            )

            return CoreGeneMutation(
                genomic_coordinate=genomic_coordinate,
                canonical_hgvs=canonical_hgvs,
                alternate_hgvs=alternate_hgvs,
                protein_consequence=protein_consequence,
                mane_tag=mane_tag,
                source="Mutalyzer",
                confidence_score=1.0 if mane_tag == "MANE Plus Clinical" else 0.8
            )
        except (MutationMappingError, MutationNormalizationError) as e:
            logger.error(f"Error in get_core_mutation for {input_hgvs}: {e}")
            raise Exception("Failed to build CoreGeneMutation from input") from e
        except Exception as e:
            logger.error(f"Unexpected error in get_core_mutation for {input_hgvs}: {e}")
            raise

    def close(self):
        """Clean up any resources."""
        self.service.close()
