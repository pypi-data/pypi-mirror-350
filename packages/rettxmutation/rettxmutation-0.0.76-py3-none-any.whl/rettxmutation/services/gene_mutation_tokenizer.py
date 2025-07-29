import re
from rettxmutation.models.gene_models import GeneMutation

class HgvsMutationTokenizer:
    # Amino acid mapping for normalization
    AA_MAP = {
        'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 'Cys': 'C',
        'Gln': 'Q', 'Glu': 'E', 'Gly': 'G', 'His': 'H', 'Ile': 'I',
        'Leu': 'L', 'Lys': 'K', 'Met': 'M', 'Phe': 'F', 'Pro': 'P',
        'Ser': 'S', 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V',
        'Ter': '*', 'X': 'X'
    }
    
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

        # Add variant type tokens
        if mutation.variant_type:
            tokens.add(mutation.variant_type.lower())

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

        # Enhanced transcript variant parsing
        if transcript.hgvs_transcript_variant:
            tokens.update(HgvsMutationTokenizer.parse_transcript_variant(transcript.hgvs_transcript_variant))

        # Enhanced protein consequence parsing
        for protein_str in [transcript.protein_consequence_slr, transcript.protein_consequence_tlr]:
            if protein_str:
                tokens.update(HgvsMutationTokenizer.parse_protein_consequence(protein_str))

        return tokens

    @staticmethod
    def parse_transcript_variant(variant: str) -> set:
        """Parse transcript variants like c.916C>T, c.1157_1188del, c.1115_1189delinsCCTC"""
        tokens = set()
        
        # Extract positions and changes
        patterns = [
            r'c\.(\d+)([ACGT])>([ACGT])',  # c.916C>T
            r'c\.(\d+)_(\d+)del',          # c.1157_1188del
            r'c\.(\d+)_(\d+)delins([ACGT]+)'  # c.1115_1189delinsCCTC
        ]
        
        for pattern in patterns:
            match = re.search(pattern, variant)
            if match:
                groups = match.groups()
                # Add all numeric positions
                for group in groups:
                    if group and group.isdigit():
                        tokens.add(group)
                # Add change notation if present
                if len(groups) >= 3 and not groups[2].isdigit():
                    tokens.add(f"{groups[1]}>{groups[2]}" if '>' in variant else groups[2])
                break
        
        return tokens

    @staticmethod
    def parse_protein_consequence(protein_str: str) -> set:
        """Parse protein consequences like p.(R306C), p.(Arg306Cys), p.(H372Pfs*9)"""
        tokens = set()
        
        # Remove prefix and parentheses: NP_004983.1:p.(R306C) -> R306C
        clean_str = re.sub(r'^.*?p\.\(?([^)]+)\)?', r'\1', protein_str)
        tokens.add(clean_str)
        
        # Pattern for substitutions: R306C or Arg306Cys
        subst_match = re.match(r'([A-Za-z]{1,3})(\d+)([A-Za-z]{1,3})', clean_str)
        if subst_match:
            from_aa, position, to_aa = subst_match.groups()
            tokens.add(position)
            tokens.add(f"{from_aa}{position}")
            tokens.add(f"{from_aa}{position}{to_aa}")
            
            # Add both 1-letter and 3-letter codes, but only add 3-letter codes as standalone tokens
            from_1 = HgvsMutationTokenizer.AA_MAP.get(from_aa, from_aa)
            to_1 = HgvsMutationTokenizer.AA_MAP.get(to_aa, to_aa)
            if len(from_aa) == 3:  # 3-letter to 1-letter
                tokens.add(f"{from_1}{position}{to_1}")
                tokens.add(f"{from_1}{position}")
                # Add 3-letter codes as they're more informative
                tokens.update([from_aa, to_aa])
            elif len(from_aa) == 1:  # 1-letter, add 3-letter equivalent
                from_3 = next((k for k, v in HgvsMutationTokenizer.AA_MAP.items() if v == from_aa), from_aa)
                to_3 = next((k for k, v in HgvsMutationTokenizer.AA_MAP.items() if v == to_aa), to_aa)
                if from_3 != from_aa:
                    tokens.add(f"{from_3}{position}{to_3}")
                    tokens.add(f"{from_3}{position}")
                    # Add 3-letter codes as they're more informative
                    tokens.update([from_3, to_3])
            
            return tokens
        
        # Pattern for frameshift: H372Pfs*9 or His372ProfsTer9
        fs_match = re.match(r'([A-Za-z]{1,3})(\d+).*?([Pp]fs|\*|Ter).*?(\d+)?', clean_str)
        if fs_match:
            aa, position, fs_type, stop_pos = fs_match.groups()
            tokens.add(position)
            tokens.add(f"{aa}{position}")
            tokens.add("frameshift")
            if stop_pos:
                tokens.add(stop_pos)
            
            # Add 1-letter code combinations but only 3-letter as standalone
            if len(aa) == 3:
                aa_1 = HgvsMutationTokenizer.AA_MAP.get(aa, aa)
                tokens.add(f"{aa_1}{position}")
                tokens.add(aa)  # 3-letter code is informative
            elif len(aa) == 1:
                # Convert to 3-letter for standalone token
                aa_3 = next((k for k, v in HgvsMutationTokenizer.AA_MAP.items() if v == aa), aa)
                if aa_3 != aa:
                    tokens.add(aa_3)
            return tokens
        
        # Pattern for deletions: Pro386_Leu396del or P386_L396del
        del_match = re.match(r'([A-Za-z]{1,3})(\d+)_([A-Za-z]{1,3})(\d+)del', clean_str)
        if del_match:
            from_aa, start_pos, to_aa, end_pos = del_match.groups()
            tokens.update([start_pos, end_pos, f"{from_aa}{start_pos}", f"{to_aa}{end_pos}", "deletion"])
            
            # Add 1-letter code combinations but only 3-letter as standalone
            if len(from_aa) == 3:
                from_1 = HgvsMutationTokenizer.AA_MAP.get(from_aa, from_aa)
                to_1 = HgvsMutationTokenizer.AA_MAP.get(to_aa, to_aa)
                tokens.update([f"{from_1}{start_pos}", f"{to_1}{end_pos}"])
                # Add 3-letter codes as they're more informative
                tokens.update([from_aa, to_aa])
            elif len(from_aa) == 1:
                # Convert to 3-letter for standalone tokens
                from_3 = next((k for k, v in HgvsMutationTokenizer.AA_MAP.items() if v == from_aa), from_aa)
                to_3 = next((k for k, v in HgvsMutationTokenizer.AA_MAP.items() if v == to_aa), to_aa)
                if from_3 != from_aa:
                    tokens.update([from_3, to_3])
            return tokens
        
        # Extract any standalone positions
        positions = re.findall(r'\d+', clean_str)
        tokens.update(positions)
        
        return tokens

    @staticmethod
    def process_genomic_coordinate(hgvs: str) -> set:
        tokens = {hgvs}
        
        # Handle different genomic coordinate patterns
        patterns = [
            r'(NC_\d+\.\d+):g\.(\d+)([ACGT])>([ACGT])',        # g.154030912G>A
            r'(NC_\d+\.\d+):g\.(\d+)_(\d+)del',                # g.154027620_154027651del
            r'(NC_\d+\.\d+):g\.(\d+)_(\d+)delins([ACGT]+)'     # g.154030639_154030713delinsGAGG
        ]
        
        for pattern in patterns:
            match = re.match(pattern, hgvs)
            if match:
                groups = match.groups()
                tokens.add(groups[0])  # chromosome
                # Add all numeric positions
                for group in groups[1:]:
                    if group and group.isdigit():
                        tokens.add(group)
                # Add change notation if present
                if len(groups) >= 4 and not groups[3].isdigit():
                    if '>' in groups[3]:
                        tokens.add(f"{groups[2]}>{groups[3]}")
                    else:
                        tokens.add(groups[3])
                break
        
        return tokens
