import logging
from typing import Optional, Tuple, List, Dict, Any

from rettxmutation.models.gene_models import TranscriptMutation, GeneMutation, GenomicCoordinate
from rettxmutation.models.gene_registry import registry
from rettxmutation.adapters.variant_validator_adapter import (
    VariantValidatorMutationAdapter,
    VariantValidatorNormalizationError
)
from rettxmutation.adapters.variant_validator_mapper import VariantValidatorMapper
from rettxmutation.utils.hgvs_descriptor import HgvsDescriptor
from rettxmutation.models.gene_assembly import GenomeAssembly

logger = logging.getLogger(__name__)


class MutationService:
    """
    Service for normalizing and mapping both simple (SNV/indel) and
    complex (large del/dup/ins) HGVS mutations into a unified GeneMutation model.
    """

    def __init__(
        self
    ):
        # Transcripts & genome build
        self.target_assembly = "grch38"
        self.legacy_assembly = "grch37"

        # VariantValidator pieces (for SNV / small indels)
        self.vv_adapter = VariantValidatorMutationAdapter()
        self.vv_mapper = VariantValidatorMapper()

    def close(self):
        """Clean up any open sessions or resources."""
        self.vv_adapter.close()

    def get_complex_gene_mutation(self, gene_assembly: GenomeAssembly, variant_description: str) -> GeneMutation:
        """
        Given a complex HGVS string, return a GeneMutation object.
        """
        # Step 1: obtain genomic coordinate
        try:
            loci = self.normalize_complex_variant(
                assembly=gene_assembly,
                hgvs_complex=variant_description
            )

        except VariantValidatorNormalizationError as e:
            logger.error(f"VariantValidator step1 error for {variant_description}: {e}")
            raise

        # Build GenomicCoordinate objects using HgvsDescriptor
        genomic_coords: Dict[str, GenomicCoordinate] = {}
        desc38 = HgvsDescriptor(loci[self.target_assembly][0])
        genomic_coords[self.target_assembly] = GenomicCoordinate(
            assembly=self.target_assembly,
            hgvs=desc38.hgvs_string,
            start=desc38.start,
            end=desc38.end,
            size=desc38.size,
        )
        if self.legacy_assembly and self.legacy_assembly != self.target_assembly:
            desc37 = HgvsDescriptor(loci[self.legacy_assembly][0])
            genomic_coords[self.legacy_assembly] = GenomicCoordinate(
                assembly=self.legacy_assembly,
                hgvs=desc37.hgvs_string,
                start=desc37.start,
                end=desc37.end,
                size=desc37.size,
            )

        return GeneMutation(
            genome_assembly=self.target_assembly, # legacy
            genomic_coordinate=genomic_coords[self.target_assembly].hgvs,
            genomic_coordinates=genomic_coords,
            variant_type=desc38.variant_type,
            primary_transcript=None,
            secondary_transcript=None,
        )


    def get_gene_mutation_model(
        self,
        hgvs_string: str,
        gene_symbol: str
    ) -> GeneMutation:
        """
        End-to-end: given an input HGVS on some transcript,
        produce a GeneMutation with multi-assembly genomic coordinates
        and per-transcript HGVS + protein consequences.
        """
        # Step 0: get the gene object from the registry
        gene = registry.get_gene(gene_symbol)
        if not gene:
            raise ValueError(f"Unknown gene symbol: {gene_symbol}")

        target_primary_transcript = gene.primary_transcript.mrna
        target_secondary_transcript = (
            gene.secondary_transcript.mrna if gene.secondary_transcript else None
        )

        # Step 1: Normalize to genomic on both assemblies
        loci = self._normalize_to_all_assemblies(hgvs_string)

        # Step 2: Formatter call for transcript/protein HGVS
        fmt_entry = self._call_formatter(
            genomic_hgvs=loci[self.target_assembly][0],
            primary_tx=target_primary_transcript,
            secondary_tx=target_secondary_transcript
        )

        # Step 3: Map formatter response to simple dicts
        mapped = self.vv_mapper.map_formatter_response(
            fmt_entry,
            primary_transcript=target_primary_transcript,
            secondary_transcript=target_secondary_transcript,
        )

        # Step 4: Build TranscriptMutation objects
        primary_tm = self._build_transcript_mutation(mapped[target_primary_transcript])
        secondary_tm = (
            self._build_transcript_mutation(mapped[target_secondary_transcript])
            if target_secondary_transcript else
            None
        )

        # 5) Build GenomicCoordinate objects using HgvsDescriptor
        genomic_coords: Dict[str, GenomicCoordinate] = {}
        # first, descriptor for the primary build
        desc38 = HgvsDescriptor(loci[self.target_assembly][0])
        genomic_coords[self.target_assembly] = GenomicCoordinate(
            assembly=self.target_assembly,
            hgvs=desc38.hgvs_string,
            start=desc38.start,
            end=desc38.end,
            size=desc38.size,
        )
        # then for legacy (if present)
        if self.legacy_assembly and self.legacy_assembly != self.target_assembly:
            desc37 = HgvsDescriptor(loci[self.legacy_assembly][0])
            genomic_coords[self.legacy_assembly] = GenomicCoordinate(
                assembly=self.legacy_assembly,
                hgvs=desc37.hgvs_string,
                start=desc37.start,
                end=desc37.end,
                size=desc37.size,
            )

        # Step 6: Return the final GeneMutation
        return GeneMutation(
            genomic_coordinate=genomic_coords[self.target_assembly].hgvs,
            genomic_coordinates=genomic_coords,
            genome_assembly=self.target_assembly, # legacy
            variant_type=desc38.variant_type,
            primary_transcript=primary_tm,
            secondary_transcript=secondary_tm,
        )


    def _normalize_to_all_assemblies(self, hgvs_string: str) -> Dict[str, Tuple[str,int]]:
        """
        Normalize transcript-level HGVS → genomic HGVS + POS under each assembly.
        Returns dict: { "GRCh38": (hgvs, pos), "GRCh37": (hgvs, pos), ... }
        """
        tx, detail = self._split_and_resolve(hgvs_string)

        def norm(build: str) -> Tuple[str,int]:
            try:
                resp = self.vv_adapter.normalize_mutation(
                    genome_build=build,
                    variant_description=f"{tx}:{detail}",
                    select_transcripts=tx
                )
            except VariantValidatorNormalizationError as e:
                logger.error(f"Normalization error on {build} for {hgvs_string}: {e}")
                raise

            if resp.get("messages"):
                raise Exception(f"Normalization warnings: {resp['messages']}")

            unwrapped = self.vv_mapper.unwrap_response(resp)
            # extract both the HGVS *and* position from primary_assembly_loci
            loci = unwrapped.get("primary_assembly_loci", {})
            details = loci.get(build.lower()) or loci.get(build)
            if not details:
                raise ValueError(f"No primary_assembly_loci for {build}")
            hgvs = details["hgvs_genomic_description"]
            pos = int(details["vcf"]["pos"])
            return hgvs, pos

        result = {self.target_assembly: norm(self.target_assembly)}
        if self.legacy_assembly and self.legacy_assembly != self.target_assembly:
            result[self.legacy_assembly] = norm(self.legacy_assembly)
        return result


    def _split_and_resolve(self, hgvs: str) -> Tuple[str, str]:
        """
        Split "TRANSCRIPT:detail" and resolve to a full versioned transcript
        using VariantValidator's transcript resolver.
        """
        parts = hgvs.split(":", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid HGVS format (expected TRANSCRIPT:detail): {hgvs}")
        transcript, detail = parts

        tv = self.vv_adapter.resolve_transcripts(transcript.split(".")[0])
        available: List[str] = [t["reference"] for t in tv.get("transcripts", [])]
        if not available:
            raise ValueError(f"No transcripts found for prefix: {transcript}")

        if "." in transcript:
            if transcript not in available:
                raise ValueError(f"Transcript {transcript} not available")
            chosen = transcript
        else:
            versions = [v for v in available if v.startswith(f"{transcript}.")]
            if not versions:
                raise ValueError(f"No versioned transcripts for {transcript}")
            chosen = max(versions, key=self._extract_version_number)

        return chosen, detail


    @staticmethod
    def _extract_version_number(transcript_ref: str) -> int:
        """
        Given a reference like "NM_004992.4", return the integer version (4).
        """
        try:
            return int(transcript_ref.split(".")[1])
        except Exception:
            return -1


    def _call_formatter(
        self,
        genomic_hgvs: str,
        primary_tx: str,
        secondary_tx: Optional[str],
    ) -> Dict[str, Any]:
        """
        Invokes VariantFormatter once to get transcript & protein HGVS info.
        """
        sel = primary_tx
        if secondary_tx:
            sel = f"{primary_tx}|{secondary_tx}"
        try:
            fmt = self.vv_adapter.format_variant(
                genomic_hgvs=genomic_hgvs,
                select_transcripts=sel,
                genome_build="GRCh38"
            )
        except VariantValidatorNormalizationError as e:
            logger.error(f"Formatter error for {genomic_hgvs}: {e}")
            raise
        return fmt


    def _build_transcript_mutation(self, data: Dict[str, Any]) -> TranscriptMutation:
        """
        Given one entry from map_formatter_response, build the Pydantic object.
        """
        return TranscriptMutation(
            gene_id=data["gene_id"],
            transcript_id=data["transcript_id"],
            hgvs_transcript_variant=data["hgvs_transcript_variant"],
            protein_consequence_tlr=data["predicted_protein_consequence_tlr"],
            protein_consequence_slr=data["predicted_protein_consequence_slr"],
        )


    def normalize_complex_variant(
        self,
        assembly: GenomeAssembly,
        hgvs_complex: str
    ) -> Dict[str, Tuple[str, int]]:
        """
        Call VariantValidator once for assembly.refseq:g.xxx, then
        return both GRCh37 and GRCh38 normalized HGVS + pos.
        """
        desc = f"{assembly.refseq}:{hgvs_complex}"

        try:
            resp = self.vv_adapter.normalize_mutation(
                genome_build=assembly.build,
                variant_description=desc,
                select_transcripts=assembly.refseq
            )
        except VariantValidatorNormalizationError as e:
            logger.error(f"Normalization error on {assembly.build} for {hgvs_complex}: {e}")
            raise

        if resp.get("messages"):
            raise Exception(f"Normalization warnings: {resp['messages']}")

        unwrapped = self.vv_mapper.unwrap_response(resp)
        loci = unwrapped.get("primary_assembly_loci", {})

        results: Dict[str, Tuple[str, int]] = {}
        for build_key, details in loci.items():
            hgvs = details["hgvs_genomic_description"]
            pos = int(details["vcf"]["pos"])
            results[build_key.lower()] = (hgvs, pos)

        return results
