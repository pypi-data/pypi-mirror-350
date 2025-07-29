from typing import Literal, Dict, Tuple, Any
from pydantic import BaseModel, Field, model_validator, field_validator


# Hard-coded map: (build, chromosome) → refseq accession
# “legacy” vs “current” versions encoded explicitly
REFSEQ_MAP: Dict[Tuple[str, str], str] = {
    # Chromosome 1
    ("GRCh37", "1"):  "NC_000001.10",  # example: legacy 
    ("GRCh38", "1"):  "NC_000001.11",  # example: current

    # Chromosome 3
    ("GRCh37", "3"):  "NC_000003.11",  # legacy for chr3
    ("GRCh38", "3"):  "NC_000003.12",  # current for chr3

    # Chromosome X (23)
    ("GRCh37", "X"):  "NC_000023.10",  # legacy for chrX
    ("GRCh38", "X"):  "NC_000023.11",  # current for chrX
}


class GenomeAssembly(BaseModel):
    build: Literal["GRCh37", "GRCh38"] = Field(..., description="Genome build")
    chromosome: str = Field(..., description="Chromosome (1-22, X or Y)")
    refseq: str = Field(
        ..., 
        description="RefSeq accession for this build+chromosome"
    )

    @field_validator("build", mode="before")
    @classmethod
    def _normalize_build(cls, v: str) -> str:
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
    def _set_refseq(cls, values):
        build = values.get("build")
        chrom = values.get("chromosome")
        if not build or not chrom:
            raise ValueError("Both 'build' and 'chromosome' are required")

        # Normalize input: allow "chr1"/"CHR1" or "1"
        chrom_norm = chrom.upper().removeprefix("CHR")
        if chrom_norm not in {c for (_, c) in REFSEQ_MAP.keys()}:
            raise ValueError(f"Unsupported chromosome: {chrom}")

        key = (build, chrom_norm)
        if key not in REFSEQ_MAP:
            raise ValueError(f"No RefSeq defined for build={build}, chr={chrom_norm}")

        values["chromosome"] = chrom_norm
        values["refseq"] = REFSEQ_MAP[key]
        return values
