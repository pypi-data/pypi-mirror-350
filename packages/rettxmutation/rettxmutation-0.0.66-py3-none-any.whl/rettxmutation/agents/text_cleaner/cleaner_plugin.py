import re
import ftfy
import logging
from semantic_kernel.functions import kernel_function


logger = logging.getLogger(__name__)


class TextCleanerPlugin:
    """
    Responsible for cleaning and normalizing text extracted from OCR or other sources.
    """

    PLUGIN_NAME = "text_cleaner_plugin"
    DESCRIPTION = "A plugin that cleans and normalizes text extracted from OCR or other sources."


    @kernel_function(
        name="clean_ocr_text",
        description="Clean and normalize text extracted from OCR or other sources.",
    )
    def clean_ocr_text(self, raw_text: str) -> str:
        """
        Takes raw text (e.g. from OCR) and normalizes / cleans it up:
        1. Fix common Unicode issues (ftfy).
        2. Collapse whitespace.
        3. Fix typical HGVS-like patterns.
        4. Additional checks for missing '.' after 'c', etc.
        """
        # 1) Fix garbled Unicode with ftfy
        text = ftfy.fix_text(raw_text)

        # 2) Collapse all whitespace into a single space
        text = re.sub(r"\s+", " ", text).strip()

        # 3) Remove line breaks
        text = text.replace("\n", " ")

        # 3a) Normalizing c. patterns (e.g., c. 123A > G -> c.123A>G)
        # For strings like:
        #   "c.  123 G>A" -> "c.123G>A"
        #   "c. 1234T > C" -> "c.1234T>C"
        # Match:
        #  1) literal 'c.'
        #  2) some spaces
        #  3) one or more digits
        #  4) possible spaces
        #  5) one DNA base
        #  6) possible spaces
        #  7) literal '>'
        #  8) possible spaces
        #  9) one DNA base
        text = re.sub(
            r"(c\.)\s*(\d+)\s*([ACGTacgt])\s*>\s*([ACGTacgt])",
            r"\1\2\3>\4",
            text
        )

        # 3b) Normalizing p. patterns (e.g., p. Arg306 Cys -> p.Arg306Cys)
        text = re.sub(
            r"(p\.)\s*([A-Za-z]+)\s*(\d+)\s*([A-Za-z]+)",
            r"\1\2\3\4",
            text
        )

        # 3c) Collapsing single-letter amino-acid changes (e.g., R 306 C -> R306C)
        text = re.sub(
            r"\b([A-Za-z])\s*(\d+)\s*([A-Za-z])\b",
            r"\1\2\3",
            text
        )

        # 3d) Normalize reference sequences like NM_ or NP_ (e.g., N M_ 123. 4 -> NM_123.4)
        text = re.sub(
            r"(N[M|P]_)\s*([0-9]+)\s*\.\s*([0-9]+)",
            r"\1\2.\3",
            text
        )

        # 3e) Add a missing dot if we see "c" directly followed by
        # digits and a variant pattern (e.g., "c1234A>G" -> "c.1234A>G")
        text = re.sub(
            r"\bc(\d+[ACGTacgt]\s*>\s*[ACGTacgt])",
            r"c.\1",
            text
        )

        # 3f) If there's "c." anywhere, we might want to remove extraneous
        # spaces after "c." (e.g., "c.  123A>G" -> "c.123A>G")
        text = re.sub(
            r"(c\.)\s+(\d)",
            r"\1\2",
            text
        )

        # 3g) Convert "->" to ">" if flanked by nucleotides (e.g., "A -> T" -> "A>T")
        text = re.sub(
            r"([ACGTacgt])\s*->\s*([ACGTacgt])",
            r"\1>\2",
            text
        )

        # 5) Convert "473C-T" -> "c.473C>T"
        text = re.sub(
            r"\b(\d+)([ACGTacgt])\s*-\s*([ACGTacgt])\b",
            r"c.\1\2>\3",
            text
        )

        # 1) Looks for 3-4 digits: (\d{3,4})
        # 2) Then optional spaces, then a nucleotide letter: ([ACGTacgt])
        # 3) Then optional spaces, then a literal '>'
        # 4) Then optional spaces, then another nucleotide letter: ([ACGTacgt])
        text = re.sub(
            r"\b(\d{3,4})\s*([ACGTacgt])\s*>\s*([ACGTacgt])\b",
            r"\1\2>\3",
            text
        )

        # Looks for a single letter, then 3 digits, then a single letter
        text = re.sub(
            r"(?<!c\.)\b(\d{3,4})([ACGTacgt])>([ACGTacgt])\b",
            r"c.\1\2>\3",
            text
        )

        return text
