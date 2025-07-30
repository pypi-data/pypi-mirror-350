import logging
from typing import Optional, List
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# Word data model, extracted from a document by OCR tool
class WordData(BaseModel):
    word: str = Field(..., description="The word extracted from the document")
    confidence: float = Field(..., description="Confidence score of the extracted word")
    page_number: int = Field(..., description="Page number where the word was found")
    offset: int = Field(None, description="Offset of the word in the page")
    length: int = Field(None, description="Length of the word")

# Line data model, extracted from a document by OCR tool
class LineData(BaseModel):
    line: str = Field(..., description="The line extracted from the document")
    page_number: int = Field(..., description="Page number where the line was found")
    length: int = Field(None, description="Length of the line")

# Mecp2 keyword model
class Keyword(BaseModel):
    value: str = Field(..., description="The value of the detected keyword")
    type: str = Field(..., description="The type of the keyword (e.g., 'gene_name', 'variant_c', etc.)")
    count: int = Field(1, description="Number of occurrences of the keyword")
    confidence: Optional[float] = Field("", description="Confidence score of the detected keyword")


# Document model
class Document(BaseModel):
    raw_text: str = Field(..., description="The extracted text from the document")
    cleaned_text: Optional[str] = Field("", description="The cleaned version of the extracted text")
    summary: Optional[str] = Field("", description="Summary of the document content")
    language: str = Field(..., description="Language of the extracted text")
    words: List[WordData] = Field(..., description="List of extracted words with confidence scores")
    lines: List[LineData] = Field(..., description="List of extracted lines")
    keywords: Optional[List[Keyword]] = Field(None, description="List of detected mecp2 keywords")
    text_analytics_result: Optional[List[Keyword]] = Field(None, description="List of detected keywords from text analytics")

    def find_word_confidence(self, word_to_find: str) -> Optional[float]:
        """
        Finds a word in the word data and returns its confidence value.

        :param word_to_find: The word to search for in the words data.
        :return: The confidence score of the word if found, else None.
        """
        for word_data in self.words:
            if word_to_find in word_data.word:
                return word_data.confidence
        return None

    def dump_keywords(self, separator: str = "\n") -> str:
        """
        Dump the instance's keywords into a single string for serialization.
        Each keyword's value is separated by a space.
        """
        if not self.keywords:
            return ""
        return separator.join(keyword.value for keyword in self.keywords)

    def dump_text_analytics_keywords(self, separator: str = "\n") -> str:
        """
        Dump the instance's text analytics keywords into a single string for serialization.
        Each keyword's value is separated by a space.
        """
        if not self.text_analytics_result:
            return ""
        return separator.join(keyword.value for keyword in self.text_analytics_result)

    def dump_all_content(self) -> dict:
        """
        Dump the document content into a dictionary for serialization.
        """
        return {
            "cleaned_text": self.cleaned_text,
            "language": self.language,
            "keywords": self.dump_keywords()
        }

    def dump_plain_text(self) -> str:
        """
        Generates a plain text output concatenating cleaned_text with keywords (only keywords.value).
        """
        keywords_text = " ".join(keyword.value for keyword in self.keywords) if self.keywords else ""
        return f"{self.cleaned_text.strip()} {keywords_text}".strip()
