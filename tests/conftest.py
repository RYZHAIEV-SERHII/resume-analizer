"""
Pytest configuration and shared fixtures.
"""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_uploaded_file():
    """Fixture to mock an uploaded file (e.g., resume)."""
    file = MagicMock()
    file.name = "sample_resume.txt"
    file.read.return_value = b"This is a sample resume content."
    return file


@pytest.fixture
def mock_empty_file():
    """Fixture to mock an empty uploaded file."""
    file = MagicMock()
    file.name = "empty_resume.txt"
    file.read.return_value = b""
    return file


@pytest.fixture
def mock_ai_analysis_result():
    """Fixture to mock AI analysis results."""
    return "Mocked AI Analysis Result"


@pytest.fixture
def mock_streamlit_components():
    """Fixture to mock essential Streamlit components for testing."""
    with (
        patch("streamlit.file_uploader") as mock_file_uploader,
        patch("streamlit.text_input") as mock_text_input,
        patch("streamlit.button") as mock_button,
    ):
        yield mock_file_uploader, mock_text_input, mock_button


@pytest.fixture
def mock_analyze_resume():
    """Fixture to mock the analyze_resume function."""
    with patch("src.services.ai_analyzer.analyze_resume") as mock_function:
        mock_function.return_value = "Mocked AI Analysis Result"
        yield mock_function
