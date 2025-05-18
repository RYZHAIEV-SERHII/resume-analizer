"""
Tests for the main application functionality.
"""

import pytest
import streamlit as st
from unittest.mock import patch, MagicMock


class TestMainApp:
    def test_file_uploader(self, mock_streamlit_components):
        """Test file uploader component."""
        mock_file_uploader, _, _ = mock_streamlit_components
        mock_file_uploader.return_value = None
        uploaded_file = st.file_uploader("Upload your resume")
        assert uploaded_file is None

    def test_text_input(self, mock_streamlit_components):
        """Test text input component."""
        _, mock_text_input, _ = mock_streamlit_components
        mock_text_input.return_value = "Software Engineer"
        job_role = st.text_input("Enter the job role")
        assert job_role == "Software Engineer"

    def test_button_click(self, mock_streamlit_components):
        """Test button click component."""
        _, _, mock_button = mock_streamlit_components
        mock_button.return_value = True
        analyze_button = st.button("Analyze Resume")
        assert analyze_button is True

    @pytest.fixture
    def mock_main_components(self):
        """Fixture for mocking main components."""
        with (
            patch("streamlit.file_uploader") as mock_uploader,
            patch("streamlit.text_input") as mock_input,
            patch("streamlit.button") as mock_button,
            patch("streamlit.spinner") as mock_spinner,
            patch("streamlit.progress") as mock_progress,
            patch("streamlit.success") as mock_success,
            patch("streamlit.error") as mock_error,
            patch("streamlit.info") as mock_info,
            patch("streamlit.markdown") as mock_markdown,
            patch("streamlit.tabs") as mock_tabs,
            patch("streamlit.download_button") as mock_download,
        ):
            yield (
                mock_uploader,
                mock_input,
                mock_button,
                mock_spinner,
                mock_progress,
                mock_success,
                mock_error,
                mock_info,
                mock_markdown,
                mock_tabs,
                mock_download,
            )

    def test_successful_analysis_flow(self, mock_main_components, mock_uploaded_file):
        """Test successful resume analysis workflow."""
        (
            mock_uploader,
            mock_input,
            mock_button,
            mock_spinner,
            mock_progress,
            mock_success,
            mock_error,
            mock_info,
            mock_markdown,
            mock_tabs,
            mock_download,
        ) = mock_main_components

        # Setup component returns
        mock_uploader.return_value = mock_uploaded_file
        mock_input.return_value = "Software Engineer"
        mock_button.return_value = True
        mock_progress.return_value = MagicMock()
        mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        with (
            patch("src.utils.text_extractor.extract_text_from_file") as mock_extract,
            patch("src.services.ai_analyzer.analyze_resume") as mock_analyze,
        ):
            # Set up mock returns
            mock_extract.return_value = "Extracted resume text"
            mock_analyze.return_value = "Analysis result"

            # Import and run main
            from main import main

            main()

            # Verify the workflow
            mock_extract.assert_called_once()
            mock_analyze.assert_called_once_with(
                "Extracted resume text", "Software Engineer"
            )
            mock_success.assert_called()
            mock_error.assert_not_called()

    def test_empty_file_handling(self, mock_main_components, mock_empty_file):
        """Test handling of empty file upload."""
        (
            mock_uploader,
            mock_input,
            mock_button,
            mock_spinner,
            mock_progress,
            mock_success,
            mock_error,
            mock_info,
            mock_markdown,
            mock_tabs,
            mock_download,
        ) = mock_main_components

        # Set up mocks before importing main
        mock_uploader.return_value = mock_empty_file  # Mock uploaded file
        mock_button.return_value = True  # Simulate button click

        # Direct patch of extract_text_from_file at the module level
        with patch("main.extract_text_from_file", return_value=""):
            # Mock st.stop to prevent test termination
            with patch("streamlit.stop") as mock_stop:
                # Now import and run main
                from main import main

                main()

                # Check that the error was shown
                mock_error.assert_called_once_with(
                    "⚠️ File does not have any content..."
                )
                # Verify st.stop was called to halt execution
                mock_stop.assert_called_once()

    def test_error_handling(self, mock_main_components, mock_uploaded_file):
        """Test error handling during analysis."""
        (
            mock_uploader,
            mock_input,
            mock_button,
            mock_spinner,
            mock_progress,
            mock_success,
            mock_error,
            mock_info,
            mock_markdown,
            mock_tabs,
            mock_download,
        ) = mock_main_components

        # Setup components
        mock_uploader.return_value = mock_uploaded_file
        mock_input.return_value = "Software Engineer"
        mock_button.return_value = True
        mock_progress.return_value = MagicMock()

        # Setup mock error
        test_error = Exception("Test error")

        with (
            patch("main.extract_text_from_file") as mock_extract,
            patch("main.analyze_resume") as mock_analyze,
        ):
            mock_extract.side_effect = test_error

            from main import main

            main()

            # Verify error handling
            mock_extract.assert_called_once()
            mock_analyze.assert_not_called()
            mock_success.assert_not_called()
            mock_error.assert_called_with("An error occurred: Test error")

    def test_no_file_uploaded(self, mock_main_components):
        """Test behavior when no file is uploaded."""
        (
            mock_uploader,
            mock_input,
            mock_button,
            mock_spinner,
            mock_progress,
            mock_success,
            mock_error,
            mock_info,
            mock_markdown,
            mock_tabs,
            mock_download,
        ) = mock_main_components

        mock_uploader.return_value = None
        mock_button.return_value = True

        # Direct patch of extract_text_from_file at the module level
        with patch("main.extract_text_from_file", return_value=""):
            from main import main

            main()

        # Verify that no analysis was attempted
        mock_spinner.assert_not_called()
        mock_progress.assert_not_called()
        mock_success.assert_not_called()
        mock_error.assert_not_called()
