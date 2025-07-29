import re
from typing import List
from collections import Counter
from semantic_kernel.functions import kernel_function
from rettxmutation.models.document import Keyword
from rettxmutation.models.gene_models import RawMutation


class RawMutationPlugin:

    PLUGIN_NAME = "RawMutationPlugin"
    DESCRIPTION = "A plugin that stores the raw mutation data."

    @kernel_function(
        name="store_raw_mutation",
        description="Store the raw mutation data.",
    )
    def store_raw_mutation(self, input: str) -> RawMutation:
        """
        Store the raw mutation data.

        Args:
            input (str): The raw mutation string (e.g., 'NM_004992.4:c.916C>T').

        Returns:
            RawMutation: The raw mutation data.
        """
        return RawMutation(mutation=input, confidence=1.0)


    @kernel_function(
        name="detect_mecp2_keywords",
        description="Detect MECP2 gene mentions and common variant patterns in the text.",
    )
    def detect_mecp2_keywords(self, text: str) -> List[Keyword]:
        """
        Looks for MECP2 gene mentions and common variant patterns within the cleaned text.
        Returns a single list of unique Keyword models, with counts for repeated occurrences.
        """
        detected_keywords = []

        # 1. Detect "MECP2" (case-insensitive)
        mecp2_mentions = re.findall(r"\bMECP2\b", text, flags=re.IGNORECASE)
        mecp2_count = len(mecp2_mentions)
        if mecp2_count > 0:
            detected_keywords.append(Keyword(value="MECP2", type="gene_name", count=mecp2_count))

        # 2. Detect c. variants: e.g., "c.1035A>G" or "c.[473C>T]"
        variants_c = re.findall(r"(c\.\[?\d+[ACGTacgt>]+\]?)", text)
        variants_c_counter = Counter(variants_c)
        detected_keywords.extend(
            [Keyword(value=variant, type="variant_c", count=count) for variant, count in variants_c_counter.items()]
        )

        # 2a. Detect c. variants with deletion: e.g., "c.1040_1047del"
        variants_c_del = re.findall(r"(c\.\d+_\d+del)", text)
        variants_c_del_counter = Counter(variants_c_del)
        detected_keywords.extend(
            [Keyword(value=variant, type="variant_c", count=count) for variant, count in variants_c_del_counter.items()]
        )

        # 3. Detect p. variants: e.g., "p.Arg306Cys" or "p.[Thr158Met]"
        variants_p = re.findall(r"(p\.\[?[A-Za-z]{1,3}\d+[A-Za-z]{1,3}\]?)", text)
        variants_p_counter = Counter(variants_p)
        detected_keywords.extend(
            [Keyword(value=variant, type="variant_p", count=count) for variant, count in variants_p_counter.items()]
        )

        # 4. Detect reference sequences like NM_####.# or NP_####.#
        refs = re.findall(r"(N[M|P]_\d+\.\d+)", text)
        refs_counter = Counter(refs)
        detected_keywords.extend(
            [Keyword(value=ref, type="reference_sequence", count=count) for ref, count in refs_counter.items()]
        )

        # 4a. Detect reference sequences like NM_######
        refs_no_version = re.findall(r"(N[M|P]_\d+)", text)
        refs_no_version_counter = Counter(refs_no_version)
        detected_keywords.extend(
            [Keyword(value=ref, type="reference_sequence", count=count) for ref, count in refs_no_version_counter.items()]
        )

        return detected_keywords
