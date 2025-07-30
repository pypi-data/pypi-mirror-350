import pytest
from rettxmutation.analysis.text_cleaner import TextCleaner


def test_clean_ocr_text():
    # Test case for normalizing c. patterns
    assert TextCleaner.clean_ocr_text("NM_004992.3:c.378-3C>G") == "NM_004992.3:c.378-3C>G"

    # Test case for normalizing c. patterns
    assert TextCleaner.clean_ocr_text("c. 1234A>G") == "c.1234A>G"
    assert TextCleaner.clean_ocr_text("c.1234 A>G") == "c.1234A>G"
    assert TextCleaner.clean_ocr_text("c. 1234 A>G") == "c.1234A>G"
    assert TextCleaner.clean_ocr_text("c. 1234 A> G") == "c.1234A>G"
    assert TextCleaner.clean_ocr_text("c. 1234 A > G") == "c.1234A>G"

    # Test case for normalizing p. patterns
    assert TextCleaner.clean_ocr_text("p. Arg306 Cys") == "p.Arg306Cys"

    # Test case for collapsing single-letter amino-acid changes
    assert TextCleaner.clean_ocr_text("R 306 C") == "R306C"

    # Test case for normalizing reference sequences like NM_ or NP_
    assert TextCleaner.clean_ocr_text("NM_ 123. 4") == "NM_123.4"

    # Additional test cases
    assert TextCleaner.clean_ocr_text("p. Gly12 Ser") == "p.Gly12Ser"
    assert TextCleaner.clean_ocr_text("NM_001110792.2:c.123A > G") == "NM_001110792.2:c.123A>G"
    assert TextCleaner.clean_ocr_text("NP_001110792.1:p. Arg306 Cys") == "NP_001110792.1:p.Arg306Cys"


if __name__ == "__main__":
    pytest.main()
