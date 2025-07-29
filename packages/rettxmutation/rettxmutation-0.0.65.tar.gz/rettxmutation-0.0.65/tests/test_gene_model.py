import pytest
from pydantic import ValidationError
from rettxmutation.models.gene_models import (
    GeneMutation,
    GenomicCoordinate,
    TranscriptMutation
)

import logging
logger = logging.getLogger(__name__)

#
# 1. New “forward” path: supplying genomic_coordinates directly
#
def test_new_coordinates_parsing_and_dump():
    data = {
        "variant_type": "deletion",
        "genomic_coordinates": {
            "GRCh37": {
                "assembly": "GRCh37",
                "hgvs": "NC_000023.10:g.153338576_153421944del",
                "start": 153_338_576,
                "end":   153_421_944,
                "size":  83_369,
            },
            "GRCh38": {
                "assembly": "GRCh38",
                "hgvs": "NC_000023.11:g.154000000_154100000del",
                "start": 154_000_000,
                "end":   154_100_000,
                # size is omitted, should be computed from start/end
            },
        },
        "primary_transcript": {
            "hgvs_transcript_variant": "NM_004992.4:c.916C>T"
        }
    }
    gm = GeneMutation(**data)

    dumped = gm.model_dump(exclude_none=True)

    # legacy‐field names should not appear in the serialized output
    for legacy in ("affected_region", "deletion_size"):
        assert legacy not in dumped

    # the two assemblies round-trip correctly
    assert set(gm.genomic_coordinates) == {"GRCh37", "GRCh38"}
    grch38 = gm.genomic_coordinates["GRCh38"]
    assert isinstance(grch38, GenomicCoordinate)
    assert grch38.size == 100_001 # computed from start/end

    # default variant_type is preserved
    assert gm.variant_type == "deletion"


#
# 2. Legacy-only path: genome_assembly + genomic_coordinate
#    – start/end are parsed from the HGVS, not from affected_region,
#    – size is computed if deletion_size is None, otherwise preserved.
#
def test_migrate_legacy_fields():
    # Only legacy fields — no explicit deletion_size/affected_region any more
    legacy = {
        "genome_assembly": "GRCh37",
        "genomic_coordinate": "NC_000023.10:g.100_200del",
        "variant_type": "deletion",
        "primary_transcript": {"hgvs_transcript_variant": "NM_004992.4:c.1_2del"}
    }

    gm = GeneMutation(**legacy)
    out = gm.model_dump(exclude_none=True)

    # Legacy fields are still present for now
    assert out["genome_assembly"] == "GRCh37"
    assert out["genomic_coordinate"] == "NC_000023.10:g.100_200del"

    # No more deletion_size or affected_region keys
    assert "deletion_size" not in out
    assert "affected_region" not in out

    # We must have exactly one entry in the new dict
    assert list(out["genomic_coordinates"]) == ["GRCh37"]
    gc: GenomicCoordinate = gm.genomic_coordinates["GRCh37"]

    # start/end come from the HGVS g.100_200del
    assert gc.start == 100
    assert gc.end   == 200

    # size is auto‐computed = end-start+1 = 101
    assert gc.size == 200 - 100 + 1

    # variant_type remains 'deletion'
    assert gm.variant_type == "deletion"




#
# 3. Missing both new + legacy → error
#
def test_missing_coordinates_raises():
    with pytest.raises(ValidationError) as exc:
        GeneMutation(primary_transcript={"hgvs_transcript_variant": "NM_004992.4:c.10A>G"})
    assert "Missing genomic coordinates" in str(exc.value)


#
# 4. Literal validation & extras dropped
#
def test_invalid_assembly_literal_and_extra_flag_dropped():
    # extra fields should be ignored (not raise)
    valid = {
        "variant_type": "SNV",
        "genomic_coordinates": {
            "GRCh38": {
                "assembly": "GRCh38",
                "hgvs": "NC_000023.11:g.1A>C",
                "start": 1, "end": 1
            }
        },
        "primary_transcript": {"hgvs_transcript_variant": "NM_004992.4:c.1A>C"},
        "flag": "intergenic"
    }
    gm = GeneMutation(**valid)
    dumped = gm.model_dump(exclude_none=True)
    assert "flag" not in dumped

    # but an invalid assembly string should still raise
    invalid = valid.copy()
    invalid["genomic_coordinates"]["GRCh38"]["assembly"] = "hg19"
    with pytest.raises(ValidationError):
        GeneMutation(**invalid)


#
# 5. TranscriptMutation required fields
#
def test_transcript_mutation_required():
    with pytest.raises(ValidationError):
        TranscriptMutation()  # must at least supply hgvs_transcript_variant

#
# 7. Migration of legacy fields to new genomic_coordinates
#
def test_persist_and_migrate_specific_mutation():
    # simulate a stored document with the legacy shape
    legacy_payload = {
        "genome_assembly": "GRCh38",
        "genomic_coordinate": "NC_000023.11:g.154030793T>C",
        "primary_transcript": {
            "hgvs_transcript_variant": "NM_004992.4:c.1035A>G",
            "protein_consequence_tlr": "NP_004983.1:p.(Lys345=)",
            "protein_consequence_slr": "NP_004983.1:p.(K345=)"
        },
        "secondary_transcript": {
            "hgvs_transcript_variant": "NM_001110792.2:c.1071A>G",
            "protein_consequence_tlr": "NP_001104262.1:p.(Lys357=)",
            "protein_consequence_slr": "NP_001104262.1:p.(K357=)"
        }
    }

    # load into our GeneMutation model
    gm = GeneMutation(**legacy_payload)

    # serialize back to dict, dropping any None-valued fields
    out = gm.model_dump(exclude_none=True, mode="json")

    logger.debug(out)

    # 1) legacy fields must not appear
    for old in ("affected_region", "deletion_size"):
        assert old not in out

    # 2) we should now have exactly one assembly key
    assert list(out["genomic_coordinates"]) == ["GRCh38"]

    # 3) that record must carry the correct HGVS
    coords = out["genomic_coordinates"]["GRCh38"]
    assert coords["hgvs"] == "NC_000023.11:g.154030793T>C"

    # 4) since no affected_region was provided, start/end default to 0
    assert coords["start"] == 154030793
    assert coords["end"]   == 154030793

    # 6) transcripts are untouched
    assert out["primary_transcript"]["hgvs_transcript_variant"] == "NM_004992.4:c.1035A>G"
    assert out["primary_transcript"]["protein_consequence_slr"] == "NP_004983.1:p.(K345=)"
    assert out["secondary_transcript"]["hgvs_transcript_variant"] == "NM_001110792.2:c.1071A>G"
    assert out["secondary_transcript"]["protein_consequence_slr"] == "NP_001104262.1:p.(K357=)"
