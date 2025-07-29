import logging
from typing import Optional, Tuple
from rettxmutation.models.gene_models import TranscriptMutation, GeneMutation
from .variant_validator_adapter import (
    VariantValidatorMutationAdapter,
    VariantValidatorNormalizationError
)
from .variant_validator_mapper import VariantValidatorMapper
from rettxmutation.models.gene_models import RawMutation

logger = logging.getLogger(__name__)


class MutationService:
    """
    Service layer that implements the new workflow using only the VariantValidator API.

    Workflow:
      1. Initial call: Use the input HGVS string (as variant_description and select_transcripts)
         to obtain the genomic coordinate.
      2. If errors occur, stop and raise an exception.
      3. Second call: Use the genomic coordinate as variant_description and select_transcripts
         set to "NM_004992.4,NM_001110792.2".
      4. Again, if errors occur, raise an exception.
      5. Use the mapping layer to extract the needed fields and populate a GeneMutation instance.

    Note: genome_build is fixed to "GRCh38".
    """
    def __init__(
        self,
        primary_transcript: str = "NM_004992.4",
        secondary_transcript: Optional[str] = "NM_001110792.2",
        target_assembly: str = "GRCh38"
    ):
        # Initialize the primary and secondary transcripts.
        self.primary_transcript = primary_transcript
        self.secondary_transcript = secondary_transcript
        # Initialize the target assembly (genome build).
        self.target_assembly = target_assembly
        # Initialize the adapter for VariantValidator API calls.
        self.variantvalidator_adapter = VariantValidatorMutationAdapter(target_assembly=target_assembly)
        # Initialize the mapping layer.
        self.mapper = VariantValidatorMapper()

    # Extract and validate the transcript from the input HGVS string.
    def extract_and_validate_transcript(self, input_hgvs: str) -> Tuple[str, str]:
        transcript, mutation_detail = self._split_input_hgvs(input_hgvs)
        validated_transcript = self._resolve_transcript_version(transcript)
        return validated_transcript, mutation_detail

    def _split_input_hgvs(self, input_hgvs: str) -> Tuple[str, str]:
        parts = input_hgvs.split(":", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid HGVS format: {input_hgvs}")
        return parts[0], parts[1]

    def _resolve_transcript_version(self, transcript: str) -> str:
        transcript_data = self.variantvalidator_adapter.resolve_transcripts(
            transcript.split(".")[0]
        )
        transcripts = [t["reference"] for t in transcript_data.get("transcripts", [])]

        if not transcripts:
            raise ValueError(f"No transcripts found for input transcript id: {transcript}")

        if "." in transcript:
            # Verify transcript exists
            if transcript in transcripts:
                return transcript
            raise ValueError(f"Transcript '{transcript}' is not available.")

        # Select highest version if no version specified
        versioned_transcripts = [
            t for t in transcripts if t.startswith(f"{transcript}.")
        ]
        if not versioned_transcripts:
            raise ValueError(f"No versioned transcripts found for '{transcript}'")

        return max(versioned_transcripts, key=self._extract_version_number)

    def _extract_version_number(self, transcript_ref: str) -> int:
        try:
            return int(transcript_ref.split(".")[1])
        except (IndexError, ValueError):
            return -1

    def get_gene_mutation(self, input_hgvs: RawMutation) -> GeneMutation:
        """
        Given an input HGVS mutation, obtain a mapped and normalized GeneMutation.
        
        Steps:
          1. Call VariantValidator with the input HGVS as both the variant_description and select_transcripts
             (using the transcript extracted from the input) to obtain the genomic coordinate.
          2. If errors are present, raise an exception.
          3. Call VariantValidator a second time using the genomic coordinate as variant_description and
             select_transcripts = "NM_004992.4,NM_001110792.2".
          4. If errors are present, raise an exception.
          5. Map the final API response to domain objects using the mapping layer and build a GeneMutation.
        """
        try:
            # Step 1: Initial API call
            logger.info(f"Processing mutation: {input_hgvs}")
            transcript, mutation_detail = self.extract_and_validate_transcript(input_hgvs.mutation)
            logger.info(f"Extracted info: {transcript} and {mutation_detail}")
            initial_response = self.variantvalidator_adapter.normalize_mutation(
                variant_description=f"{transcript}:{mutation_detail}",
                select_transcripts=transcript
            )
            if initial_response.get("messages"):
                raise Exception(f"Initial VariantValidator error: {initial_response['messages']}")

            # Unwrap the response to get the mutation-specific data.
            unwrapped_initial = self.mapper.unwrap_response(initial_response)

            # Extract genomic coordinate.
            genomic_coordinate = self.mapper.extract_genomic_coordinate(unwrapped_initial, self.target_assembly)
            if not genomic_coordinate:
                validation_warnings = unwrapped_initial.get("validation_warnings", [])
                raise Exception(f"Genomic coordinate not found in the initial response. Validation warnings: {validation_warnings}")

            # Step 2: Second API call with genomic coordinate and both transcripts.
            transcripts_param = f"{self.primary_transcript}|{self.secondary_transcript}"
            final_response = self.variantvalidator_adapter.normalize_mutation(
                variant_description=genomic_coordinate,
                select_transcripts=transcripts_param
            )
            if final_response.get("messages"):
                raise Exception(f"Second VariantValidator error: {final_response['messages']}")

            # Map the final response into a list of gene variant dictionaries.
            variants = self.mapper.map_gene_variants(final_response, self.primary_transcript, self.secondary_transcript)
            if not variants:
                raise Exception("No gene variant data found in the final VariantValidator response.")

            # Use the mapper to get a dictionary keyed by transcript.
            variants = self.mapper.map_gene_variants(final_response, self.primary_transcript, self.secondary_transcript)

            primary_data = variants.get(self.primary_transcript)
            secondary_data = variants.get(self.secondary_transcript)
            # We need to ensure we have the primary and secondary variants.
            if not primary_data or not secondary_data:
                raise Exception("Required gene variants not found in the final response.")

            # Extract the primary and secondary variants.
            primary_transcript_obj = TranscriptMutation(
                hgvs_transcript_variant=primary_data["hgvs_transcript_variant"],
                protein_consequence_tlr=primary_data["predicted_protein_consequence_tlr"],
                protein_consequence_slr=primary_data["predicted_protein_consequence_slr"]
            )
            secondary_transcript_obj = TranscriptMutation(
                hgvs_transcript_variant=secondary_data["hgvs_transcript_variant"],
                protein_consequence_tlr=secondary_data["predicted_protein_consequence_tlr"],
                protein_consequence_slr=secondary_data["predicted_protein_consequence_slr"]
            )

            # Create and return the GeneMutation object.
            return GeneMutation(
                genome_assembly=self.target_assembly,
                genomic_coordinate=genomic_coordinate,
                primary_transcript=primary_transcript_obj,
                secondary_transcript=secondary_transcript_obj
            )
        except VariantValidatorNormalizationError as e:
            logger.exception(f"Error processing mutation {input_hgvs}: {e}")
            raise Exception("Failed to process mutation input") from e
        except Exception as e:
            logger.exception(f"Unexpected error processing mutation {input_hgvs}: {e}")
            raise
