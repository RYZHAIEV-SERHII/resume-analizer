"""
Tests for the UI utilities.
"""

import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.utils.ui_utils import (
    set_gradient_background,
    load_css_file,
    setup_custom_spinner,
    setup_page_config,
    setup_ui,
    setup_sidebar,
)


class TestUIUtils:
    def test_set_gradient_background(self):
        """Test setting gradient background."""
        with patch("streamlit.markdown") as mock_markdown:
            set_gradient_background()
            mock_markdown.assert_called_once()
            style_content = mock_markdown.call_args[0][0]
            assert "background: linear-gradient" in style_content
            assert mock_markdown.call_args[1]["unsafe_allow_html"] is True

    def test_load_css_file(self):
        """Test loading CSS file."""
        css_content = "body { background: blue; }"
        with (
            patch("builtins.open", mock_open(read_data=css_content)) as mock_file,
            patch("streamlit.markdown") as mock_markdown,
        ):
            load_css_file("test.css")
            mock_file.assert_called_once_with("test.css")
            mock_markdown.assert_called_once()
            assert css_content in mock_markdown.call_args[0][0]
            assert mock_markdown.call_args[1]["unsafe_allow_html"] is True

    def test_setup_custom_spinner(self):
        """Test setting up custom spinner."""
        with patch("streamlit.markdown") as mock_markdown:
            setup_custom_spinner()
            mock_markdown.assert_called_once()
            style_content = mock_markdown.call_args[0][0]
            assert ".stSpinner" in style_content
            assert mock_markdown.call_args[1]["unsafe_allow_html"] is True

    def test_setup_page_config(self):
        """Test setting up page configuration."""
        with patch("streamlit.set_page_config") as mock_config:
            setup_page_config()
            mock_config.assert_called_once()
            config = mock_config.call_args[1]
            assert config["page_title"] == "AI Resume Analyzer"
            assert config["page_icon"] == "📃"
            assert config["layout"] == "centered"
            assert config["initial_sidebar_state"] == "collapsed"
            assert "Get Help" in config["menu_items"]
            assert "Report a bug" in config["menu_items"]
            assert "About" in config["menu_items"]

    def test_setup_sidebar(self):
        """Test setting up sidebar."""
        with patch("src.utils.ui_utils.st") as mock_st:
            # Create sidebar mock
            mock_sidebar = MagicMock()
            mock_st.sidebar = mock_sidebar

            # Call the function under test
            setup_sidebar()

            # Verify sidebar content was added correctly
            mock_sidebar.image.assert_called_once_with(
                "https://img.icons8.com/fluency/96/resume.png", width=80
            )
            mock_sidebar.title.assert_called_once_with("Resume Analyzer")

            # Verify markdown calls
            markdown_calls = mock_sidebar.markdown.call_args_list
            markdown_texts = [args[0][0] for args in markdown_calls]

            assert "---" in markdown_texts
            assert "### About" in markdown_texts
            assert "### Features" in markdown_texts
            assert "### Need Help?" in markdown_texts

    @patch("os.path.exists")
    def test_setup_ui_with_css(self, mock_exists):
        """Test UI setup with existing CSS file."""
        mock_exists.return_value = True

        with (
            patch("src.utils.ui_utils.setup_page_config") as mock_page_config,
            patch("src.utils.ui_utils.set_gradient_background") as mock_gradient,
            patch("src.utils.ui_utils.setup_custom_spinner") as mock_spinner,
            patch("src.utils.ui_utils.load_css_file") as mock_css,
            patch("src.utils.ui_utils.setup_sidebar") as mock_sidebar,
        ):
            setup_ui()

            mock_page_config.assert_called_once()
            mock_gradient.assert_called_once()
            mock_spinner.assert_called_once()
            mock_css.assert_called_once_with("src/static/styles.css")
            mock_sidebar.assert_called_once()

    @patch("os.path.exists")
    def test_setup_ui_without_css(self, mock_exists):
        """Test UI setup without CSS file."""
        mock_exists.return_value = False

        with (
            patch("src.utils.ui_utils.setup_page_config") as mock_page_config,
            patch("src.utils.ui_utils.set_gradient_background") as mock_gradient,
            patch("src.utils.ui_utils.setup_custom_spinner") as mock_spinner,
            patch("src.utils.ui_utils.load_css_file") as mock_css,
            patch("src.utils.ui_utils.setup_sidebar") as mock_sidebar,
        ):
            setup_ui()

            mock_page_config.assert_called_once()
            mock_gradient.assert_called_once()
            mock_spinner.assert_called_once()
            mock_css.assert_not_called()
            mock_sidebar.assert_called_once()

    def test_load_css_file_not_found(self):
        """Test handling of missing CSS file."""
        with (
            pytest.raises(FileNotFoundError),
            patch("builtins.open", mock_open()) as mock_file,
        ):
            mock_file.side_effect = FileNotFoundError()
            load_css_file("nonexistent.css")
