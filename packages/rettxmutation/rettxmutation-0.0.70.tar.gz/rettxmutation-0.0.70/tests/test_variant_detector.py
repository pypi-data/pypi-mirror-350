import pytest
from rettxmutation.analysis.gene_variant_detector import GeneVariantDetector


@pytest.fixture
def detector():
    return GeneVariantDetector()


def test_detect_mecp2_mentions(detector):
    text = "MECP2 is commonly mentioned. MECP2 mutations can cause issues."
    result = detector.detect_mecp2_keywords(text)

    assert len(result) == 1
    assert result[0].value == "MECP2"
    assert result[0].type == "gene_name"
    assert result[0].count == 2


def test_detect_c_variants(detector):
    text = "Variants like c.1035A>G and c.[473C>T] are known."
    result = detector.detect_mecp2_keywords(text)

    assert len(result) == 2
    assert result[0].value == "c.1035A>G"
    assert result[0].type == "variant_c"
    assert result[0].count == 1
    assert result[1].value == "c.[473C>T]"
    assert result[1].type == "variant_c"
    assert result[1].count == 1


def test_detect_c_deletion_variants(detector):
    text = "Deletion variants include c.1040_1047del and c.1035_1040del."
    result = detector.detect_mecp2_keywords(text)

    assert len(result) == 2
    assert result[0].value == "c.1040_1047del"
    assert result[0].type == "variant_c"
    assert result[0].count == 1
    assert result[1].value == "c.1035_1040del"
    assert result[1].type == "variant_c"
    assert result[1].count == 1


def test_detect_p_variants(detector):
    text = "Protein variants include p.Arg306Cys and p.[Thr158Met]."
    result = detector.detect_mecp2_keywords(text)

    assert len(result) == 2
    assert result[0].value == "p.Arg306Cys"
    assert result[0].type == "variant_p"
    assert result[0].count == 1
    assert result[1].value == "p.[Thr158Met]"
    assert result[1].type == "variant_p"
    assert result[1].count == 1


def test_detect_reference_sequences(detector):
    text = "Reference sequences are NM_004992.3, NP_001029.1, and NM_004992."
    result = detector.detect_mecp2_keywords(text)

    assert len(result) == 4  # Adjust to match the actual result
    assert any(k.value == "NM_004992.3" and k.type == "reference_sequence" for k in result)
    assert any(k.value == "NM_004992" and k.type == "reference_sequence" for k in result)
    assert any(k.value == "NP_001029.1" and k.type == "reference_sequence" for k in result)
    assert any(k.value == "NP_001029" and k.type == "reference_sequence" for k in result)


def test_combined_detection(detector):
    text = (
        "MECP2 mutations such as c.1035A>G, c.[473C>T], p.Arg306Cys, "
        "and references like NM_004992.3 and NM_004992 are important to track."
    )
    result = detector.detect_mecp2_keywords(text)

    assert len(result) == 6  # Both versioned and non-versioned transcripts are included
    # Check each detected keyword
    assert any(k.value == "MECP2" and k.type == "gene_name" for k in result)
    assert any(k.value == "c.1035A>G" and k.type == "variant_c" for k in result)
    assert any(k.value == "c.[473C>T]" and k.type == "variant_c" for k in result)
    assert any(k.value == "p.Arg306Cys" and k.type == "variant_p" for k in result)
    assert any(k.value == "NM_004992.3" and k.type == "reference_sequence" for k in result)
    assert any(k.value == "NM_004992" and k.type == "reference_sequence" for k in result)


def test_no_matches(detector):
    text = "No relevant genetic information is provided in this text."
    result = detector.detect_mecp2_keywords(text)

    assert len(result) == 0
