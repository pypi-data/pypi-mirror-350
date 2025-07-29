import re
from enum import Enum
from typing import Optional, Literal, Dict, Any
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
    model_validator,
    ConfigDict,
)

class GenomicCoordinate(BaseModel):
    """
    Represents a normalization of a variant on a specific reference assembly.
    """
    assembly: Literal["GRCh37", "GRCh38"] = Field(..., description="Genome assembly version for this coordinate")
    hgvs: str = Field(..., description="HGVS genomic description, e.g. 'NC_000023.10:g.153338576_153421944del'")
    start: int = Field(..., description="Genomic start position (1-based)")
    end: int = Field(..., description="Genomic end position (1-based, inclusive)")
    size: Optional[int] = Field(None, description="Computed size = end - start + 1 (for del/dup)")

    @model_validator(mode="after")
    def ensure_size(cls, model: "GenomicCoordinate") -> "GenomicCoordinate":
        if model.size is None:
            model.size = model.end - model.start + 1
        return model

    @field_validator("assembly", mode="before")
    @classmethod
    def _upper_assembly(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        vv = v.strip().lower()
        if vv == "grch37":
            return "GRCh37"
        if vv == "grch38":
            return "GRCh38"
        return v

class TranscriptMutation(BaseModel):
    """
    Represents detailed mutation descriptions for transcript and protein levels.
    """
    gene_id: Optional[str] = Field(None, description="Gene ID (e.g., MECP2)")
    transcript_id: Optional[str] = Field(None, description="Transcript ID (e.g., NM_004992.4)")
    hgvs_transcript_variant: str = Field(..., description="Full transcript mutation description (e.g., NM_004992.3:c.916C>T)")
    protein_consequence_tlr: Optional[str] = Field(None, description="Full protein consequence description (e.g., NP_004983.2:p.Ser306Cys)")
    protein_consequence_slr: Optional[str] = Field(None, description="Short protein consequence description in SLR format (e.g., NP_004983.1:p.(R306C))")


class GeneMutation(BaseModel):
    """
    Comprehensive mutation data model for Rett Syndrome (MECP2) mutations.
    """
    model_config = ConfigDict(
        extra="ignore", # drop any unknown fields
        exclude_none=True, # omit fields with None from model_dump()
    )
    genomic_coordinates: Optional[Dict[Literal["GRCh37", "GRCh38"], GenomicCoordinate]] = Field(None, description="New: per-assembly normalized coords")
    variant_type: Literal['SNV', 'deletion', 'duplication', 'insertion', 'indel'] = Field('SNV', description="Type of variant")
    primary_transcript: Optional[TranscriptMutation] = Field(None, description="Primary transcript mutation details NM_004992.4")
    secondary_transcript: Optional[TranscriptMutation] = Field(None, description="Secondary transcript mutation details NM_001110792.2")
    # Legacy, TODO: remove in future
    genome_assembly: Optional[str] = Field(None, description="Genome assembly version (e.g., GRCh37 or GRCh38)")
    genomic_coordinate: Optional[str] = Field(None, description="Canonical genomic coordinate (e.g., NC_000023.11:g.154030912G>A or NC_000023.11:g.154010939_154058566del)")

    @staticmethod
    def _infer_variant_type(hgvs: str, default: str) -> str:
        if "delins" in hgvs:
            return "indel"
        if hgvs.endswith("del"):
            return "deletion"
        if "dup" in hgvs:
            return "duplication"
        if "ins" in hgvs:
            return "insertion"
        return default

    @field_validator("genome_assembly", mode="before")
    @classmethod
    def _normalize_legacy_asm(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        vv = v.strip().lower()
        if vv == "grch37":
            return "GRCh37"
        if vv == "grch38":
            return "GRCh38"
        return v

    @model_validator(mode="before")
    @classmethod
    def _normalize_assemblies_and_keys(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        # 1) Canonicalize the legacy field
        if asm := values.get("genome_assembly"):
            a = asm.strip().lower()
            if a == "grch37":
                values["genome_assembly"] = "GRCh37"
            elif a == "grch38":
                values["genome_assembly"] = "GRCh38"

        # 2) Canonicalize the keys of genomic_coordinates
        if coords := values.get("genomic_coordinates"):
            new_coords: Dict[str, Any] = {}
            for k, v in coords.items():
                kl = k.strip().lower()
                if kl == "grch37":
                    key = "GRCh37"
                elif kl == "grch38":
                    key = "GRCh38"
                else:
                    # if somehow you have a weird key, pass it through
                    key = k
                new_coords[key] = v
            values["genomic_coordinates"] = new_coords

        return values


    @model_validator(mode="before")
    def migrate_legacy_fields(cls, values: Any) -> Any:
        """
        If only the old fields (genome_assembly+genomic_coordinate) are provided,
        build a genomic_coordinates dict *in addition to* leaving the old fields intact.
        """
        # if new coords already present, nothing to do
        if values.get("genomic_coordinates"):
            return values

        legacy_hgvs = values.get("genomic_coordinate")
        if not legacy_hgvs:
            return values

        # pick assembly (default to GRCh38)
        asm = values.get("genome_assembly", "GRCh38")

        # parse start/end from legacy HGVS
        m = re.search(r"g\.(\d+)(?:_(\d+))?", legacy_hgvs)
        if m:
            start = int(m.group(1))
            end   = int(m.group(2)) if m.group(2) else start
        else:
            start = end = 0

        # infer variant_type
        vt = cls._infer_variant_type(legacy_hgvs, values.get("variant_type", "SNV"))

        # set both fields
        values["variant_type"] = vt
        values["genomic_coordinates"] = {
            asm: {
                "assembly": asm,
                "hgvs": legacy_hgvs,
                "start": start,
                "end": end,
                # omit size → GenomicCoordinate.ensure_size will fill size=end-start+1
            }
        }

        return values

    @model_validator(mode="after")
    def ensure_some_coordinates(cls, model: "GeneMutation") -> "GeneMutation":
        """
        Make sure *at least* one of:
          - genomic_coordinates is present, or
          - legacy genome_assembly+genomic_coordinate was present
        (we already migrated the legacy into genomic_coordinates above)
        """
        if not model.genomic_coordinates:
            raise ValueError(
                "Missing genomic coordinates: either "
                "`genomic_coordinates` or legacy "
                "`genome_assembly`+`genomic_coordinate` must be provided."
            )
        return model

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


# Raw mutation data model (returned by the OpenAI model)
class RawMutation(BaseModel):
    """
    Represents the raw mutation data returned by the OpenAI model.
    """
    mutation: str = Field(..., description="Raw mutation string (e.g., 'NM_004992.4:c.916C>T')")
    confidence: float = Field(..., description="Confidence score for the mutation (0.0 to 1.0)")
