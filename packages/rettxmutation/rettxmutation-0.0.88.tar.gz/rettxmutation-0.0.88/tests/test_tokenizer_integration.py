#!/usr/bin/env python3
"""
Test script to verify the new HgvsMutationTokenizer integration in rettxmutation.py
"""
from rettxmutation.rettxmutation import RettXDocumentAnalysis
from rettxmutation.services.gene_mutation_tokenizer import HgvsMutationTokenizer
from rettxmutation.models.gene_models import GeneMutation, TranscriptMutation


def test_hgvs_tokenizer_directly():
    """Test the HgvsMutationTokenizer class directly"""
    print("Testing HgvsMutationTokenizer class directly...")
    
    # Create a mock transcript mutation
    transcript = TranscriptMutation(
        transcript_id="NM_004992.3",
        hgvs_transcript_variant="NM_004992.3:c.808C>T",
        protein_consequence_slr="p.Arg270*",
        protein_consequence_tlr="p.(Arg270*)",
        gene_id="MECP2"
    )
      # Create a mock gene mutation with proper genomic coordinates
    from rettxmutation.models.gene_models import GenomicCoordinate
    
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
    # Test tokenization directly
    print("\n1. Testing HgvsMutationTokenizer.tokenize:")
    tokens = HgvsMutationTokenizer.tokenize(gene_mutation)
    print(f"Tokens: {tokens}")
    
    print("\nHgvsMutationTokenizer test completed successfully!")


def test_rettx_integration():
    """Test the integration with RettXDocumentAnalysis"""
    print("\n\nTesting RettXDocumentAnalysis integration...")
    
    try:
        # Test that the tokenize method is available without needing full initialization
        # We can't fully test RettXDocumentAnalysis without API keys,
        # but we can test that the method exists
          # Create test data with proper structure
        from rettxmutation.models.gene_models import GenomicCoordinate
        
        transcript = TranscriptMutation(
            transcript_id="NM_004992.3",
            hgvs_transcript_variant="NM_004992.3:c.808C>T",
            protein_consequence_slr="p.Arg270*",
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
        
        # Test the tokenizer directly (since we can't initialize RettXDocumentAnalysis without API keys)
        tokens = HgvsMutationTokenizer.tokenize(gene_mutation)
        print(f"Integration test tokens: {tokens}")
        
        # Verify the method exists in RettXDocumentAnalysis
        assert hasattr(RettXDocumentAnalysis, 'tokenize'), "tokenize method not found in RettXDocumentAnalysis"
        print("✓ tokenize method found in RettXDocumentAnalysis")
        print("RettXDocumentAnalysis integration test completed successfully!")
        
    except Exception as e:
        print(f"Integration test failed: {e}")
        assert False, f"Integration test failed: {e}"


if __name__ == "__main__":
    print("Running new HgvsMutationTokenizer integration tests...\n")
    
    # Test the tokenizer directly
    test_hgvs_tokenizer_directly()
    
    # Test the integration
    test_rettx_integration()
    
    print("\n🎉 All tests passed! The HgvsMutationTokenizer has been successfully integrated.")
    print("\nThe following method is now available in RettXDocumentAnalysis:")
    print("- tokenize(gene_mutation)")
    print("\nYou can now simply call: rettx_instance.tokenize(gene_mutation)")
