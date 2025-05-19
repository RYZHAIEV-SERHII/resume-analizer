"""
Tests for the AI-powered resume analysis services.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.services.ai_analyzer import analyze_resume, get_openai_client


class TestAIAnalyzer:
    def test_get_openai_client_configuration(self):
        """Test OpenAI client configuration with OpenRouter settings."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            client = get_openai_client()
            assert client.api_key == "test-key"
            assert str(client.base_url) == "https://openrouter.ai/api/v1/"

    def test_analyze_resume_with_job_role(self):
        """Test resume analysis with a specified job role."""
        with patch("src.services.ai_analyzer.get_openai_client") as mock_get_client:
            mock_client = MagicMock()
            mock_get_client.return_value = mock_client

            mock_response = MagicMock()
            mock_message = MagicMock()
            mock_message.content = "Mocked AI Analysis Result"
            mock_choice = MagicMock()
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_response

            result = analyze_resume("Sample resume text", "Data Scientist")
            assert result == "Mocked AI Analysis Result"
            mock_client.chat.completions.create.assert_called_once()

    def test_analyze_resume_without_job_role(self):
        """Test resume analysis without a job role."""
        with patch("src.services.ai_analyzer.get_openai_client") as mock_get_client:
            mock_client = MagicMock()
            mock_get_client.return_value = mock_client

            mock_response = MagicMock()
            mock_message = MagicMock()
            mock_message.content = "Mocked AI Analysis Result"
            mock_choice = MagicMock()
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_response

            result = analyze_resume("Sample resume text")
            assert result == "Mocked AI Analysis Result"
            mock_client.chat.completions.create.assert_called_once()

    def test_analyze_resume_empty_text(self):
        """Test handling of empty resume text."""
        with pytest.raises(ValueError, match="Resume text is empty"):
            analyze_resume("")

    def test_analyze_resume_whitespace_only(self):
        """Test handling of whitespace-only resume text."""
        with pytest.raises(ValueError, match="Resume text is empty"):
            analyze_resume("   \n   \t   ")

    @patch("src.services.ai_analyzer.get_openai_client")
    def test_analyze_resume_api_integration(self, mock_get_client):
        """Test the complete API integration flow."""
        # Mock the OpenAI client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="AI Analysis Result"))
        ]
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = analyze_resume("Valid resume text", "Software Engineer")

        # Verify the API call
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]

        # Verify correct model and parameters
        assert call_kwargs["model"] == "google/gemini-2.0-flash-exp:free"
        assert call_kwargs["temperature"] == 0.7
        assert call_kwargs["max_tokens"] == 1000

        # Verify system and user messages
        messages = call_kwargs["messages"]
        assert messages[0]["role"] == "system"
        assert "expert resume reviewer" in messages[0]["content"].lower()
        assert messages[1]["role"] == "user"
        assert "Software Engineer" in messages[1]["content"]

        # Verify result
        assert result == "AI Analysis Result"

    @patch("src.services.ai_analyzer.get_openai_client")
    def test_analyze_resume_api_error(self, mock_get_client):
        """Test handling of API errors."""
        # Mock the client to raise an exception
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client

        with pytest.raises(Exception, match="API Error"):
            analyze_resume("Valid resume text")
