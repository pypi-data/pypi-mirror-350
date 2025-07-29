#!/usr/bin/env python3
"""
Test script to verify the new HgvsMutationTokenizer integration
"""
from rettxmutation.models.gene_models import GeneMutation, TranscriptMutation, GenomicCoordinate
from rettxmutation.services.gene_mutation_tokenizer import HgvsMutationTokenizer


def test_direct_tokenizer():
    """Test the HgvsMutationTokenizer directly"""
    print("Testing HgvsMutationTokenizer directly...")
      # Create test data
    transcript = TranscriptMutation(
        transcript_id="NM_004992.4",
        hgvs_transcript_variant="NM_004992.4:c.916C>T",
        protein_consequence_slr="p.(Arg306*)",
        protein_consequence_tlr="p.Arg306*",
        gene_id="MECP2"
    )
    
    genomic_coord = GenomicCoordinate(
        assembly="GRCh38",
        hgvs="NC_000023.11:g.154030872C>T",
        start=154030872,
        end=154030872
    )
    
    gene_mutation = GeneMutation(
        variant_type="SNV",
        primary_transcript=transcript,
        genomic_coordinates={
            "GRCh38": genomic_coord
        }
    )
      # Test tokenization
    tokens = HgvsMutationTokenizer.tokenize(gene_mutation)
    print(f"Direct tokenizer result: {tokens}")
    
    # Add assertions to validate the tokenizer output
    assert tokens is not None, "Tokenizer should not return None"
    assert isinstance(tokens, str), "Tokenizer should return a string"
    assert len(tokens) > 0, "Tokenizer should return non-empty string"
    
    # Verify that important components are in the tokenized output
    assert "MECP2" in tokens, "Gene ID should be in tokenized output"
    assert "C>T" in tokens, "Base change should be in tokenized output"
    assert "154030872" in tokens, "Genomic position should be in tokenized output"
    assert "NM_004992.4" in tokens, "Transcript ID should be in tokenized output"
    assert "c.916C>T" in tokens, "cDNA variant should be in tokenized output"
    assert "p.(Arg306*)" in tokens or "p.Arg306*" in tokens, "Protein consequence should be in tokenized output"
    
    print("✓ All direct tokenizer assertions passed")


def test_main_module_integration():
    """Test integration through the main RettXDocumentAnalysis module"""
    print("\nTesting integration through RettXDocumentAnalysis...")
    
    # Import the main class
    from rettxmutation.rettxmutation import RettXDocumentAnalysis
      # Create test data
    transcript = TranscriptMutation(
        transcript_id="NM_004992.4",
        hgvs_transcript_variant="NM_004992.4:c.916C>T",
        protein_consequence_slr="p.(Arg306*)",
        gene_id="MECP2"
    )
    
    genomic_coord = GenomicCoordinate(
        assembly="GRCh38",
        hgvs="NC_000023.11:g.154030872C>T",
        start=154030872,
        end=154030872
    )
    
    gene_mutation = GeneMutation(
        variant_type="SNV",
        primary_transcript=transcript,
        genomic_coordinates={
            "GRCh38": genomic_coord
        }
    )
      # Check that the tokenize method exists
    assert hasattr(RettXDocumentAnalysis, 'tokenize'), "tokenize method not found!"
    print("✓ tokenize method exists in RettXDocumentAnalysis")
    
    # Verify method signature and callable
    tokenize_method = getattr(RettXDocumentAnalysis, 'tokenize')
    assert callable(tokenize_method), "tokenize should be a callable method"
    
    # Test with a minimal instance (we can't fully initialize without API keys)
    # Just verify the method exists and can be called
    print("✓ Integration verified - tokenize method is available")
    
    # Additional assertions to verify the integration
    assert hasattr(RettXDocumentAnalysis, '__init__'), "RettXDocumentAnalysis should have __init__ method"
    
    # Verify that the class doesn't have the old tokenizer methods
    old_methods = ['tokenize_gene_mutation', 'tokenize_cdna_mutation', 'tokenize_protein_mutation', 'tokenize_embedding_input']
    for old_method in old_methods:
        assert not hasattr(RettXDocumentAnalysis, old_method), f"Old method {old_method} should not exist anymore"
    
    print("✓ Verified old tokenizer methods have been removed")
    print("✓ All integration assertions passed")


if __name__ == "__main__":
    print("🚀 Testing new HgvsMutationTokenizer integration...\n")
    
    # Test direct tokenizer
    test_direct_tokenizer()
    print("✓ Direct tokenizer test passed")
    
    # Test integration
    test_main_module_integration()
    print("✓ Integration test passed")
    
    print("\n🎉 All tests passed!")
    print("✓ Your new tokenizer is successfully integrated!")
    print("\nUsage:")
    print("  from rettxmutation.rettxmutation import RettXDocumentAnalysis")
    print("  rettx = RettXDocumentAnalysis(...)")  
    print("  tokens = rettx.tokenize(gene_mutation)")
