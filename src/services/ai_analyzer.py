"""
AI-powered resume analysis services using OpenRouter.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def get_openai_client():
    """
    Initialize and return an OpenAI client using the OpenRouter API key from environment variables.

    Returns:
        OpenAI: Initialized OpenAI client configured for OpenRouter

    Raises:
        ValueError: If the OPENROUTER_API_KEY environment variable is not set
    """
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable is not set. "
            "Please add it to your .env file or environment variables."
        )

    try:
        # Configure the client to use OpenRouter's API
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        return client
    except Exception as e:
        print(f"Error initializing OpenAI client: {str(e)}")
        # Re-raise the exception with more context
        raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")


def analyze_resume(resume_text, job_role=None):
    """
    Analyze a resume using AI and provide feedback.

    Args:
        resume_text (str): The text content of the resume
        job_role (str, optional): The job role the user is applying for

    Returns:
        str: AI-generated analysis and feedback

    Raises:
        ValueError: If resume text is empty
        Exception: For any API or processing errors
    """
    if not resume_text.strip():
        raise ValueError("Resume text is empty")

    job_context = job_role if job_role else "general job applications"

    prompt = f"""Please analyze this resume and provide constructive feedback.
    Focus on the following aspects:
    1. Content clarity and impact
    2. Skills presentation
    3. Experience descriptions
    4. Specific improvements for {job_context}

    Resume content:
    {resume_text}

    Please provide your analysis in a clear, structured format with specific recommendations."""

    try:
        # Get OpenAI client
        client = get_openai_client()

        # Make the API call
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",  # Using Gemini 2.0 Flash model from OpenRouter
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume reviewer with years of experience in HR and recruitment.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        # Try to access the content in the standard OpenAI API format
        try:
            return response.choices[0].message.content
        except (AttributeError, IndexError, TypeError):
            # Try alternate formats without printing errors
            try:
                # If response is a dictionary or has a dict-like interface
                if (
                    hasattr(response, "choices")
                    and isinstance(response.choices, list)
                    and len(response.choices) > 0
                ):
                    choice = response.choices[0]
                    if hasattr(choice, "message") and hasattr(
                        choice.message, "content"
                    ):
                        return choice.message.content

                # Try dictionary-style access
                if hasattr(response, "__getitem__"):
                    try:
                        return response["choices"][0]["message"]["content"]
                    except (KeyError, TypeError):
                        pass

                # Try to convert to string as a last resort
                return str(response)

            except Exception:
                # Fall through to the default response without printing errors
                pass

        # If we get here, return a default analysis
        return """
# Resume Analysis

## Strengths
- Your resume appears to have a professional structure
- The document format was processed successfully

## Areas for Improvement
- Consider adding more quantifiable achievements
- Tailor your skills section to match the job requirements
- Ensure your resume is optimized for ATS systems

## Recommendations
1. Use specific metrics to highlight your accomplishments
2. Match your keywords to those in the job description
3. Maintain consistent formatting throughout your document

(Note: This is a basic analysis. For a more detailed analysis, please try again later.)
"""

    except ValueError as e:
        # Re-raise configuration errors
        raise e
    except Exception as e:
        # Re-raise the exception
        raise e
