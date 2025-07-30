import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def translate_mutalyzer_response(raw_response: Dict[str, Any], target_assembly: str) -> Dict[str, Optional[str]]:
    """
    Translate the raw Mutalyzer API response into a standardized dictionary format.
    
    Expected standardized keys:
      - genomic_coordinate: The canonical genomic coordinate (e.g., "NC_000023.11:g.154030912G>A")
      - protein_consequence: Protein-level consequence (e.g., "NP_004983.1:p.Arg306Cys")
      - mane_tag: Tag indicating MANE status (e.g., "MANE Plus Clinical")
    
    Parameters:
      raw_response: The raw dictionary returned by the API.
      target_assembly: The assembly to filter on (e.g., "GRCH38").
    
    Returns:
      A dictionary with standardized keys.
    """
    chrom_desc = raw_response.get("chromosomal_descriptions", [])
    genomic_coordinate = next(
        (entry.get("g") for entry in chrom_desc if entry.get("assembly") == target_assembly),
        None
    )
    protein_info = raw_response.get("protein", {})
    protein_consequence = protein_info.get("description")
    mane_tag = next(
        (entry.get("tag", {}).get("details") for entry in chrom_desc if entry.get("tag")),
        None
    )
    
    standardized_data = {
        "genomic_coordinate": genomic_coordinate,
        "protein_consequence": protein_consequence,
        "mane_tag": mane_tag,
    }
    
    logger.debug(f"Translated API response into standardized data: {standardized_data}")
    return standardized_data
