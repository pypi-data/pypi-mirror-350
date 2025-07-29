import jmespath
from typing import Dict, List

class VariantValidatorMapper:
    """
    Mapper to extract only the fields of interest from the VariantValidator API response.

    Fields of interest:
      - hgvs_transcript_variant: The transcript-level mutation description (e.g., "NM_004992.4:c.916C>T")
      - genomic_coordinate: The genomic coordinate, extracted via the path 
          primary_assembly_loci.grch38.hgvs_genomic_description (e.g., "NC_000023.11:g.154030912G>A")
      - predicted_protein_consequence_tlr: Detailed protein consequence (e.g., "NP_004983.1:p.(Arg306Cys)")
      - predicted_protein_consequence_slr: Short protein consequence (e.g., "NP_004983.1:p.(R306C)")
    """
    RESERVED_KEYS = {"flag", "metadata", "messages"}

    def map_gene_variant(self, gene_variant: Dict) -> Dict:
        """
        Extracts the required fields from a single gene_variant object.
        """
        try:
            transcript_variant = gene_variant["hgvs_transcript_variant"]

            # Extract genomic coordinate using JMESPath.
            genomic_coordinate = gene_variant.get("genomic_coordinate")
            if not genomic_coordinate:
                genomic_coordinate = jmespath.search(
                    "primary_assembly_loci.grch38.hgvs_genomic_description", gene_variant
                )
            if not genomic_coordinate:
                raise ValueError("Genomic coordinate not found.")

            protein_info = gene_variant.get("hgvs_predicted_protein_consequence", {})
            tlr = protein_info.get("tlr")
            slr = protein_info.get("slr")

            return {
                "hgvs_transcript_variant": transcript_variant,
                "genomic_coordinate": genomic_coordinate,
                "predicted_protein_consequence_tlr": tlr,
                "predicted_protein_consequence_slr": slr
            }
        except Exception as e:
            raise ValueError(f"Error mapping gene variant: {e}")

    def map_gene_variants(self, raw_response: Dict, primary_transcript: str, secondary_transcript: str) -> Dict[str, Dict]:
        """
        Extracts gene variants from the raw API response and returns a dictionary keyed by transcript.
        
        Only variants corresponding to primary_transcript and secondary_transcript are returned.
        """
        variants = {}
        for key, value in raw_response.items():
            if key in self.RESERVED_KEYS:
                continue
            # We assume the key is in the format "Transcript:c.XXX" and we extract the transcript part.
            transcript = key.split(":")[0]
            if transcript in (primary_transcript, secondary_transcript):
                variants[transcript] = self.map_gene_variant(value)
        return variants


    def unwrap_response(self, raw_response: Dict) -> Dict:
        """
        Unwraps the raw API response to extract the mutation-specific data.

        The API response contains extra keys (like "flag", "metadata", or "messages").
        This method returns the first key that isn't one of those.

        Parameters:
            raw_response (Dict): The full JSON response from VariantValidator.

        Returns:
            Dict: The unwrapped mutation data.

        Raises:
            ValueError: If no mutation data is found.
        """
        for key, value in raw_response.items():
            if key not in self.RESERVED_KEYS:
                return value
        raise ValueError("unwrap_response::No mutation data found in response.")


    def extract_genomic_coordinate(self, unwrapped: Dict, target_assembly: str) -> str:
        """
        Extracts the genomic coordinate from the unwrapped mutation data.

        It looks for the key "primary_assembly_loci" and then for the assembly matching 
        target_assembly (trying both lower-case and original case) to obtain the value under
        "hgvs_genomic_description".

        Parameters:
            unwrapped (Dict): The mutation-specific data (after unwrapping the raw response).
            target_assembly (str): The genome build, e.g., "GRCh38".

        Returns:
            str: The genomic coordinate (e.g., "NC_000023.11:g.154030912G>A").

        Raises:
            ValueError: If the genomic coordinate cannot be found.
        """
        # Try lower-case target_assembly first.
        query = f"primary_assembly_loci.{target_assembly.lower()}.hgvs_genomic_description"
        genomic_coordinate = jmespath.search(query, unwrapped)
        if not genomic_coordinate:
            # Fall back to target_assembly as provided.
            query = f"primary_assembly_loci.{target_assembly}.hgvs_genomic_description"
            genomic_coordinate = jmespath.search(query, unwrapped)
        if not genomic_coordinate:
            raise ValueError("extract_genomic_coordinate::Genomic coordinate not found in response.")
        return genomic_coordinate
