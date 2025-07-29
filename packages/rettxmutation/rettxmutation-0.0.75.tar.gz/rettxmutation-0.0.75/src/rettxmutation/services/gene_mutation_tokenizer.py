import re
from rettxmutation.models.gene_models import GeneMutation

class HgvsMutationTokenizer:
    @staticmethod
    def tokenize(mutation: GeneMutation) -> str:
        tokens = set()

        # Primary transcript tokens
        if mutation.primary_transcript:
            tokens.update(HgvsMutationTokenizer.process_transcript(mutation.primary_transcript))

        # Secondary transcript tokens
        if mutation.secondary_transcript:
            tokens.update(HgvsMutationTokenizer.process_transcript(mutation.secondary_transcript))

        # Genomic coordinates tokens
        if mutation.genomic_coordinates:
            for coord in mutation.genomic_coordinates.values():
                tokens.update(HgvsMutationTokenizer.process_genomic_coordinate(coord.hgvs))

        return " ".join(sorted(tokens))

    @staticmethod
    def process_transcript(transcript) -> set:
        tokens = set()

        fields = [
            transcript.transcript_id,
            transcript.hgvs_transcript_variant,
            transcript.protein_consequence_slr,
            transcript.protein_consequence_tlr,
            transcript.gene_id,
        ]

        for val in fields:
            if val:
                tokens.add(val)

        # Extract numeric position from hgvs_transcript_variant
        if transcript.hgvs_transcript_variant:
            match = re.search(r"\.(\w\.\d+[ACGT]>[ACGT])", transcript.hgvs_transcript_variant)
            if match:
                mutation = match.group(1)
                tokens.add(mutation)
                pos_match = re.search(r"\d+", mutation)
                if pos_match:
                    tokens.add(pos_match.group(0))

        # Extract numeric positions from protein consequences
        for protein_str in [transcript.protein_consequence_slr, transcript.protein_consequence_tlr]:
            if protein_str:
                aa_match = re.search(r"p\.\((\w+)(\d+)(\w+)\)", protein_str)
                if aa_match:
                    tokens.add(aa_match.group(0))
                    tokens.add(aa_match.group(2))

        return tokens

    @staticmethod
    def process_genomic_coordinate(hgvs: str) -> set:
        tokens = {hgvs}
        match = re.match(r"(NC_\d+\.\d+):g\.(\d+)([ACGT]>[ACGT])?", hgvs)
        if match:
            chrom, position, base_change = match.groups()
            tokens.update([chrom, position])
            if base_change:
                tokens.add(base_change)
        return tokens
