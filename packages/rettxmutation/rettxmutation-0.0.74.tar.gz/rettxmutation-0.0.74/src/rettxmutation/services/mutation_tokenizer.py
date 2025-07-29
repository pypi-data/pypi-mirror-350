import logging
import re
from typing import Optional, List
from rettxmutation.models.gene_models import GeneMutation, TranscriptMutation
from rettxmutation.models.mutation_model import Mutation

logger = logging.getLogger(__name__)


class MutationTokenizer:
    """
    Service for tokenizing mutation information to support free text search.
    
    This class provides methods to extract searchable tokens from various    mutation formats including cDNA, protein, and embedding input strings.
    """
    
    def __init__(self):
        """
        Initialize the MutationTokenizer.
        """
        pass
    
    def tokenize_gene_mutation(self, gene_mutation: GeneMutation) -> str:
        """
        Tokenize a complete GeneMutation object for free text search.
        
        Args:
            gene_mutation: GeneMutation object to tokenize
            
        Returns:
            str: Space-separated tokens for searching
        """
        if not gene_mutation:
            return ""
        
        all_tokens = []
        
        # Tokenize primary transcript
        if gene_mutation.primary_transcript:
            cdna_tokens = self._tokenize_cdna_mutation(gene_mutation.primary_transcript.hgvs_transcript_variant)
            if cdna_tokens:
                all_tokens.append(cdna_tokens)
            
            protein_consequence = gene_mutation.primary_transcript.protein_consequence_slr or gene_mutation.primary_transcript.protein_consequence_tlr
            if protein_consequence:
                protein_tokens = self._tokenize_protein_mutation(protein_consequence)
                if protein_tokens:
                    all_tokens.append(protein_tokens)
        
        # Tokenize secondary transcript
        if gene_mutation.secondary_transcript:
            cdna_tokens = self._tokenize_cdna_mutation(gene_mutation.secondary_transcript.hgvs_transcript_variant)
            if cdna_tokens:
                all_tokens.append(cdna_tokens)
            
            protein_consequence = gene_mutation.secondary_transcript.protein_consequence_slr or gene_mutation.secondary_transcript.protein_consequence_tlr
            if protein_consequence:
                protein_tokens = self._tokenize_protein_mutation(protein_consequence)
                if protein_tokens:
                    all_tokens.append(protein_tokens)
        
        # Add gene-level information
        if gene_mutation.variant_type:
            all_tokens.append(gene_mutation.variant_type)
        
        # Extract gene_id from transcripts if available
        gene_id = None
        if gene_mutation.primary_transcript and gene_mutation.primary_transcript.gene_id:
            gene_id = gene_mutation.primary_transcript.gene_id
            all_tokens.append(gene_id)
        elif gene_mutation.secondary_transcript and gene_mutation.secondary_transcript.gene_id:
            gene_id = gene_mutation.secondary_transcript.gene_id
            all_tokens.append(gene_id)
        
        # Combine all tokens and remove duplicates
        combined_tokens = ' '.join(all_tokens)
        unique_tokens = list(dict.fromkeys(combined_tokens.split()))
        return ' '.join(filter(None, unique_tokens))
        
    def _tokenize_cdna_mutation(self, hgvs_string: str) -> Optional[str]:
        """
        Tokenize cDNA mutation information for free text search.
        
        Args:
            hgvs_string: HGVS string to tokenize (e.g., "NM_004992.4:c.916C>T")
            
        Returns:
            str: Space-separated tokens for searching, or None if invalid
        """
        if not hgvs_string:
            return None
            
        try:
            tokens = []
            # Add the full HGVS string
            tokens.append(hgvs_string)
            
            # Extract and tokenize components using Mutation class
            mutation = Mutation.from_hgvs_string(hgvs_string)
            
            # Add transcript ID
            tokens.append(mutation.transcript)
            # Also add without version number
            if '.' in mutation.transcript:
                tokens.append(mutation.transcript.split('.')[0])
            
            # Add mutation part
            tokens.append(mutation.mutation)
            
            # Add position information
            tokens.append(str(mutation.cdna_start_position))
            if mutation.cdna_end_position != mutation.cdna_start_position:
                tokens.append(str(mutation.cdna_end_position))
            
            # Add base change information
            tokens.append(mutation.cdna_base_change)
            # Split compound changes like "C>T" into individual bases
            if '>' in mutation.cdna_base_change:
                parts = mutation.cdna_base_change.split('>')
                tokens.extend(parts)
            
            return ' '.join(filter(None, tokens))
            
        except Exception as e:
            logger.warning(f"Failed to tokenize cDNA mutation: {e}")
            return hgvs_string

    def _tokenize_protein_mutation(self, protein_hgvs: str) -> Optional[str]:
        """
        Tokenize protein mutation information for free text search.

        Args:
            protein_hgvs: Protein HGVS string (e.g., "p.Arg106His")

        Returns:
            str: Space-separated tokens for searching, or None if no protein consequence
        """
        if not protein_hgvs:
            return None

        try:
            tokens = []
            # Add the full protein HGVS string
            tokens.append(protein_hgvs)

            # Extract amino acid changes (e.g., "p.Arg106His" -> "Arg", "106", "His")
            aa_pattern = r'p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2}|\*|=)'
            aa_match = re.search(aa_pattern, protein_hgvs)
            if aa_match:
                tokens.extend([aa_match.group(1), aa_match.group(2), aa_match.group(3)])

            # Also check for single letter amino acid codes
            aa_single_pattern = r'p\.([A-Z])(\d+)([A-Z]|\*|=)'
            aa_single_match = re.search(aa_single_pattern, protein_hgvs)
            if aa_single_match:
                tokens.extend([aa_single_match.group(1), aa_single_match.group(2), aa_single_match.group(3)])

            return ' '.join(filter(None, tokens))

        except Exception as e:
            logger.warning(f"Failed to tokenize protein mutation: {e}")
            return protein_hgvs

    def _tokenize_embedding_input(self, embedding_input: str, gene_id: Optional[str], variant_type: Optional[str]) -> Optional[str]:
        """
        Tokenize the embedding input string for free text search.

        Args:
            embedding_input: The full embedding input string
            gene_id: Gene identifier
            variant_type: Type of variant

        Returns:
            str: Space-separated tokens for searching
        """
        if not embedding_input:
            return None
        try:
            tokens = []

            # Split on common delimiters and extract meaningful tokens
            # Remove common prefixes and split on delimiters
            clean_input = embedding_input.replace('Gene:', '').replace('Primary transcript:', '').replace('Secondary transcript:', '').replace('Primary protein:', '').replace('Secondary protein:', '').replace('Variant type:', '').replace('Rett Syndrome', '')

            # Split on pipes, colons, spaces, and other delimiters
            raw_tokens = re.split(r'[|\s:,;()]+', clean_input)

            # Filter and process tokens
            for token in raw_tokens:
                token = token.strip()
                if len(token) > 1:  # Skip single characters and empty strings
                    tokens.append(token)

                    # For HGVS-like strings, extract components
                    if '.' in token and ('c.' in token or 'p.' in token or 'g.' in token):
                        # Extract positions and changes
                        pos_match = re.search(r'(\d+)', token)
                        if pos_match:
                            tokens.append(pos_match.group(1))

                    # For base changes like "C>T"
                    if '>' in token and len(token) <= 5:
                        tokens.extend(token.split('>'))

            # Add structured metadata
            if gene_id:
                tokens.append(gene_id)
            if variant_type:
                tokens.append(variant_type)

            # Add common search terms
            tokens.extend(['mutation', 'variant', 'rett', 'syndrome'])

            # Remove duplicates and return
            unique_tokens = list(dict.fromkeys(tokens))  # Preserves order
            return ' '.join(filter(None, unique_tokens))

        except Exception as e:
            logger.warning(f"Failed to tokenize embedding input: {e}")
            return embedding_input
            # Remove duplicates and return
            unique_tokens = list(dict.fromkeys(tokens))  # Preserves order
            return ' '.join(filter(None, unique_tokens))

        except Exception as e:
            logger.warning(f"Failed to tokenize embedding input: {e}")
            return embedding_input
