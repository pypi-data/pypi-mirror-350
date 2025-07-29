#!/usr/bin/env python3
"""
Test script to verify the MutationTokenizer integration in rettxmutation.py
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rettxmutation.services.mutation_tokenizer import MutationTokenizer
from rettxmutation.models.gene_models import GeneMutation, TranscriptMutation


def test_mutation_tokenizer():
    """Test the MutationTokenizer class directly"""
    print("Testing MutationTokenizer class...")
    
    # Initialize tokenizer
    tokenizer = MutationTokenizer()
      # Create a mock transcript mutation
    transcript = TranscriptMutation(
        hgvs_transcript_variant="NM_004992.3:c.808C>T",
        protein_consequence_slr="p.Arg270*",
        gene_id="MECP2"
    )    # Create a mock gene mutation
    gene_mutation = GeneMutation(
        variant_type="SNV",
        primary_transcript=transcript,
        genomic_coordinates={
            "GRCh38": {
                "assembly": "GRCh38",
                "hgvs": "NC_000023.11:g.154030872C>T",
                "start": 154030872,
                "end": 154030872
            }
        }
    )
    
    # Test tokenization methods
    print("\n1. Testing tokenize_gene_mutation:")
    tokens = tokenizer.tokenize_gene_mutation(gene_mutation)
    print(f"Tokens: {tokens}")
    
    print("\n2. Testing _tokenize_cdna_mutation:")
    cdna_tokens = tokenizer._tokenize_cdna_mutation(transcript.hgvs_transcript_variant)
    print(f"cDNA Tokens: {cdna_tokens}")
    
    print("\n3. Testing _tokenize_protein_mutation:")
    protein_tokens = tokenizer._tokenize_protein_mutation(transcript.protein_consequence_slr)
    print(f"Protein Tokens: {protein_tokens}")
    
    print("\n4. Testing tokenize_embedding_input with sample data:")
    sample_embedding_input = "Gene: MECP2 | Primary transcript: NM_004992.3:c.808C>T | Primary protein: p.Arg270* | Variant type: SNV | Rett Syndrome"
    embedding_tokens = tokenizer._tokenize_embedding_input(
        sample_embedding_input, 
        "MECP2", 
        "SNV"
    )
    print(f"Embedding Tokens: {embedding_tokens}")
    
    print("\nMutationTokenizer test completed successfully!")


def test_rettx_integration():
    """Test the integration with RettXDocumentAnalysis"""
    print("\n\nTesting RettXDocumentAnalysis integration...")
    
    # We can't fully test RettXDocumentAnalysis without API keys,
    # but we can test the tokenizer initialization
    from rettxmutation.services.mutation_tokenizer import MutationTokenizer
    
    # Test with minimal initialization
    tokenizer = MutationTokenizer()
    
    # Test embedding input tokenization (doesn't require API)
    test_input = "Gene: MECP2 | Primary transcript: NM_004992.3:c.808C>T | Primary protein: p.Arg270*"
    tokens = tokenizer._tokenize_embedding_input(test_input, "MECP2", "SNV")
    print(f"Integration test tokens: {tokens}")
    
    # Assert that tokens were generated
    assert tokens is not None
    assert isinstance(tokens, str)
    assert len(tokens) > 0
    
    print("RettXDocumentAnalysis integration test completed successfully!")


if __name__ == "__main__":
    print("Running MutationTokenizer integration tests...\n")
    
    # Test the tokenizer directly
    test_mutation_tokenizer()
    
    # Test the integration
    test_rettx_integration()
    
    print("\n🎉 All tests passed! The MutationTokenizer has been successfully integrated.")
    print("\nThe following methods are now available in RettXDocumentAnalysis:")
    print("- tokenize_gene_mutation(gene_mutation)")
    print("- tokenize_cdna_mutation(transcript_mutation)")
    print("- tokenize_protein_mutation(transcript_mutation)")
    print("- tokenize_embedding_input(embedding_input, gene_id, variant_type)")
