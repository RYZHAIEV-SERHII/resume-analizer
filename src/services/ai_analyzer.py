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
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    # Configure the client to use OpenRouter's API
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def analyze_resume(resume_text, job_role=None):
    """
    Analyze a resume using AI and provide feedback.

    Args:
        resume_text (str): The text content of the resume
        job_role (str, optional): The job role the user is applying for

    Returns:
        str: AI-generated analysis and feedback
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

    client = get_openai_client()
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

    return response.choices[0].message.content
