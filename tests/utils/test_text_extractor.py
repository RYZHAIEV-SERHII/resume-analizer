"""
Tests for the text extraction utilities.
"""

import io
import pytest
from unittest.mock import MagicMock, patch
from src.utils.text_extractor import (
    extract_text_from_file,
    extract_text_from_pdf,
    extract_text_from_docx,
)


class TestTextExtractor:
    def test_extract_text_from_valid_file(self, mock_uploaded_file):
        """Test text extraction from a valid text file."""
        result = extract_text_from_file(mock_uploaded_file)
        assert result == "This is a sample resume content."

    def test_extract_text_from_empty_file(self, mock_empty_file):
        """Test text extraction from an empty file."""
        result = extract_text_from_file(mock_empty_file)
        assert result.strip() == ""

    @pytest.fixture
    def mock_pdf_file(self):
        """Fixture for mocking a PDF file."""
        file = MagicMock()
        file.type = "application/pdf"
        file.read.return_value = b"PDF content"
        return file

    @pytest.fixture
    def mock_docx_file(self):
        """Fixture for mocking a DOCX file."""
        file = MagicMock()
        file.type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        file.read.return_value = b"DOCX content"
        return file

    def test_extract_text_from_pdf(self, mock_pdf_file):
        """Test PDF text extraction."""
        with patch("PyPDF2.PdfReader") as mock_pdf_reader:
            # Mock PDF page extraction
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Page 1 content"
            mock_pdf_reader.return_value.pages = [mock_page]

            result = extract_text_from_file(mock_pdf_file)
            assert "Page 1 content" in result

    @patch("src.utils.text_extractor.Document")
    def test_extract_text_from_docx(self, mock_document_class, mock_docx_file):
        """Test DOCX text extraction."""
        # Set up mock document
        mock_doc = MagicMock()
        mock_paragraph = MagicMock()
        mock_paragraph.text = "Paragraph 1 content"
        mock_doc.paragraphs = [mock_paragraph]
        mock_document_class.return_value = mock_doc

        result = extract_text_from_file(mock_docx_file)

        # Verify Document was created with BytesIO
        mock_document_class.assert_called_once()
        assert isinstance(mock_document_class.call_args[0][0], io.BytesIO)
        assert "Paragraph 1 content" in result

    def test_invalid_text_file_encoding(self):
        """Test handling of invalid text file encoding."""
        file = MagicMock()
        file.type = "text/plain"
        file.read.return_value = b"\x80\x81\x82"  # Invalid UTF-8 bytes

        result = extract_text_from_file(file)
        assert "Could not decode the file" in result

    def test_pdf_extraction_error(self):
        """Test handling of PDF extraction errors."""
        file = MagicMock()
        file.type = "application/pdf"
        file.read.return_value = b"Invalid PDF content"

        with pytest.raises(Exception):
            extract_text_from_pdf(io.BytesIO(file.read()))

    def test_docx_extraction_error(self):
        """Test handling of DOCX extraction errors."""
        file = MagicMock()
        file.type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        file.read.return_value = b"Invalid DOCX content"

        with pytest.raises(Exception):
            extract_text_from_docx(io.BytesIO(file.read()))
