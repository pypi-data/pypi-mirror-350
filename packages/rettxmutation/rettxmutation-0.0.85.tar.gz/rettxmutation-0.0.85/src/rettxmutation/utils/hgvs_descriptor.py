# File: rettxmutation/utils/hgvs_descriptor.py
from mutalyzer_hgvs_parser import to_model

class HgvsDescriptor:
    """
    Wraps mutalyzer-hgvs-parser.to_model to extract:
      - hgvs_string
      - variant_type (SNV, deletion, duplication, insertion, indel)
      - start, end (1-based)
      - size = end - start + 1
    """
    MUT_TYPE_MAP = {
        "substitution": "SNV",
        "deletion":     "deletion",
        "duplication":  "duplication",
        "insertion":    "insertion",
        "deletion_insertion":       "indel",
    }

    def __init__(self, hgvs_string: str):
        self.hgvs_string = hgvs_string
        try:
            parsed = to_model(hgvs_string)
        except Exception as e:
            raise ValueError(f"Invalid HGVS '{hgvs_string}': {e}") from e

        variant = parsed["variants"][0]
        raw_type = variant["type"]
        loc = variant["location"]

        if loc["type"] == "point":
            self.start = self.end = loc["position"]
        elif loc["type"] == "range":
            self.start = loc["start"]["position"]
            self.end   = loc["end"]["position"]
        else:
            raise ValueError(f"Unsupported location type '{loc['type']}' in '{hgvs_string}'")

        self.variant_type = self.MUT_TYPE_MAP.get(raw_type, "SNV")
        self.size = self.end - self.start + 1
