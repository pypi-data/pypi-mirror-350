import re
from typing import Optional
from pydantic import BaseModel, Field
from mutalyzer_hgvs_parser import to_model


class Mutation(BaseModel):
    """
    Represents a parsed HGVS mutation with specific components extracted using mutalyzer.
    Example: NM_004992.4:c.916C>T
    """
    transcript: str = Field(..., description="Transcript identifier (e.g., NM_004992.4)")
    mutation: str = Field(..., description="Mutation part (e.g., c.916C>T)")
    cdna_start_position: int = Field(..., description="Starting position in cDNA (e.g., 916)")
    cdna_end_position: int = Field(..., description="Ending position in cDNA (e.g., 916)")
    cdna_base_change: str = Field(..., description="Base change notation (e.g., C>T)")

    @classmethod
    def from_hgvs_string(cls, hgvs_string: str) -> "Mutation":
        """
        Parse an HGVS string using mutalyzer and create a Mutation object.
        
        Args:
            hgvs_string: HGVS notation string (e.g., "NM_004992.4:c.916C>T")
            
        Returns:
            Mutation: Parsed mutation object
            
        Raises:
            ValueError: If the HGVS string cannot be parsed or is invalid
        """
        try:
            # Parse using mutalyzer
            parsed_model = to_model(hgvs_string)
        except Exception as e:
            raise ValueError(f"Failed to parse HGVS string '{hgvs_string}' with mutalyzer: {e}")

        # Extract transcript reference
        transcript = parsed_model.get("reference", {}).get("id", "")
        if not transcript:
            raise ValueError(f"No transcript reference found in HGVS string: {hgvs_string}")

        # Extract coordinate system and mutation part
        coordinate_system = parsed_model.get("coordinate_system", "")
        if not coordinate_system:
            raise ValueError(f"No coordinate system found in HGVS string: {hgvs_string}")

        # Extract variant information
        variants = parsed_model.get("variants", [])
        if not variants:
            raise ValueError(f"No variants found in HGVS string: {hgvs_string}")

        variant = variants[0]  # Take the first variant

        # Extract location information
        location = variant.get("location", {})
        location_type = location.get("type")

        if location_type == "point":
            cdna_start_position = location.get("position")
            cdna_end_position = location.get("position")
        elif location_type == "range":
            cdna_start_position = location.get("start", {}).get("position")
            cdna_end_position = location.get("end", {}).get("position")
        else:
            raise ValueError(f"Unsupported location type '{location_type}' in HGVS string: {hgvs_string}")

        if cdna_start_position is None or cdna_end_position is None:
            raise ValueError(f"Could not extract positions from HGVS string: {hgvs_string}")

        # Extract base change information
        cdna_base_change = cls._extract_base_change(variant)

        # Construct the mutation part (everything after the colon)
        mutation_part = hgvs_string.split(":")[-1] if ":" in hgvs_string else hgvs_string        # Create the mutation object
        mutation_obj = cls(
            transcript=transcript,
            mutation=mutation_part,
            cdna_start_position=cdna_start_position,
            cdna_end_position=cdna_end_position,
            cdna_base_change=cdna_base_change
        )
        
        # Validate by reconstructing the original string
        reconstructed = f"{transcript}:{mutation_part}"
        if reconstructed != hgvs_string:
            raise ValueError(
                f"Reconstruction validation failed. "
                f"Original: '{hgvs_string}', "
                f"Reconstructed: '{reconstructed}'"
            )
        
        return mutation_obj
    
    @staticmethod
    def _extract_base_change(variant: dict) -> str:
        """
        Extract the base change notation from a mutalyzer variant.
        
        Args:
            variant: Variant dictionary from mutalyzer
            
        Returns:
            str: Base change notation (e.g., "C>T", "del", "dup")
        """
        variant_type = variant.get("type", "")
        
        if variant_type == "substitution":
            deleted = variant.get("deleted", [])
            inserted = variant.get("inserted", [])
            
            if deleted and inserted:
                deleted_seq = "".join(d.get("sequence", "") for d in deleted)
                inserted_seq = "".join(i.get("sequence", "") for i in inserted)
                return f"{deleted_seq}>{inserted_seq}"
            
        elif variant_type == "deletion":
            return "del"
            
        elif variant_type == "duplication":
            return "dup"
            
        elif variant_type == "insertion":
            inserted = variant.get("inserted", [])
            if inserted:
                inserted_seq = "".join(i.get("sequence", "") for i in inserted)
                return f"ins{inserted_seq}"
            return "ins"
            
        elif variant_type == "deletion_insertion":
            deleted = variant.get("deleted", [])
            inserted = variant.get("inserted", [])
            
            deleted_seq = "".join(d.get("sequence", "") for d in deleted) if deleted else ""
            inserted_seq = "".join(i.get("sequence", "") for i in inserted) if inserted else ""
            
            if deleted_seq and inserted_seq:
                return f"delins{inserted_seq}"
            elif deleted_seq:
                return "del"
            elif inserted_seq:
                return f"ins{inserted_seq}"
        
        # Fallback - try to extract from the original sequence
        return "unknown"