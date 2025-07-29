import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from rettxmutation.analysis.models import Document, WordData
from rettxmutation.analysis.ocr_extractor import OcrExtractor
from azure.ai.documentintelligence.models import (
    DocumentPage,
    DocumentWord,
    DocumentSpan,
    DocumentLine,
    DocumentLanguage,
    AnalyzeResult,
    DocumentAnalysisFeature
)


@pytest.fixture
def mock_analyze_result():
    """
    Builds a mock AnalyzeResult object with fake data to simulate a typical Azure response.
    """
    word1 = DocumentWord(
        content="Hello",
        confidence=0.95,
        span=DocumentSpan(offset=0, length=5)
    )
    word2 = DocumentWord(
        content="World",
        confidence=0.90,
        span=DocumentSpan(offset=6, length=5)
    )
    line1 = DocumentLine(
        content="Hello World!",
        spans=[DocumentSpan(offset=0, length=12)]
    )
    line2 = DocumentLine(
        content="Another line",
        spans=[DocumentSpan(offset=0, length=12)]
    )
    page = DocumentPage(
        page_number=1,
        words=[word1, word2],
        lines=[line1, line2]
    )
    lang_obj = DocumentLanguage(
        locale="en",
        confidence=0.99
    )
    result = AnalyzeResult(
        content="Hello World!",
        pages=[page],
        languages=[lang_obj],
        styles=None,
        documents=[],
        tables=[],
        key_value_pairs=[]
    )
    return result


@patch("rettxmutation.analysis.ocr_extractor.DocumentAnalysisClient")
def test_extract_text_success(mock_client_class, mock_analyze_result):
    """
    Test a successful call to extract_text, ensuring it returns
    a Document object with the expected fields.
    """
    # 1) Create a mock poller that returns our fake AnalyzeResult
    mock_poller = MagicMock()
    mock_poller.result.return_value = mock_analyze_result

    # 2) The client's begin_analyze_document returns mock_poller
    mock_client_instance = MagicMock()
    mock_client_instance.begin_analyze_document.return_value = mock_poller
    # The mock_client_class is the *class*, so returning our instance
    mock_client_class.return_value = mock_client_instance

    # 3) Instantiate OcrExtractor with dummy endpoint/key
    extractor = OcrExtractor(endpoint="https://dummy_endpoint",
                             key="dummy_key")

    # 4) Provide a dummy BytesIO stream (or real file stream) to extract_text
    fake_file = BytesIO(b"fake-pdf-or-image-bytes")
    document_result = extractor.extract_text(fake_file)

    # 5) Validate the returned Document object
    assert isinstance(document_result, Document)
    # The raw_text we expect from mock_analyze_result
    assert document_result.raw_text == "Hello World!"
    assert document_result.language == "en"  # from _infer_language

    # Check the words
    assert len(document_result.words) == 2
    assert isinstance(document_result.words[0], WordData)
    assert document_result.words[0].word == "Hello"
    assert document_result.words[0].confidence == 0.95

    # 6) Verify the correct client methods were called
    # Using 'prebuilt-read' model
    mock_client_instance.begin_analyze_document.assert_called_once_with(
        "prebuilt-read",
        document=fake_file,
        features=[DocumentAnalysisFeature.LANGUAGES],
    )
    # Check the 'features' argument in detail:
    call_args = mock_client_instance.begin_analyze_document.call_args[1]
    assert "prebuilt-read" in mock_client_instance.begin_analyze_document.call_args[0]
    assert "document" in call_args
    assert "features" in call_args


@patch("rettxmutation.analysis.ocr_extractor.DocumentAnalysisClient")
def test_extract_text_no_result(mock_client_class):
    mock_poller = MagicMock()
    mock_poller.result.return_value = None  # simulate no result
    mock_client_instance = MagicMock()
    mock_client_instance.begin_analyze_document.return_value = mock_poller

    mock_client_class.return_value = mock_client_instance
    extractor = OcrExtractor(endpoint="test_endpoint", key="test_key")

    fake_file = BytesIO(b"fake")
    result = extractor.extract_text(fake_file)

    # The code logs "No valid document..." and returns something like ("", None).
    assert result == ("", None), "Expected empty data if no result"
