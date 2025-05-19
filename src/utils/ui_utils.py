"""
UI utilities for the Resume Analyzer application.
Contains functions for styling and UI setup.
"""

import os
import streamlit as st


def set_gradient_background():
    """
    Set a gradient background for the Streamlit app.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #4361ee, #3a0ca3, #4cc9f0);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_css_file(file_name):
    """
    Load and apply a CSS file.

    Args:
        file_name (str): Path to the CSS file
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def setup_custom_spinner():
    """
    Set up a custom spinner animation.
    """
    st.markdown(
        """
        <style>
        .stSpinner > div {
            border-top-color: #4361ee !important;
            border-right-color: #4cc9f0 !important;
            border-bottom-color: #3a0ca3 !important;
            border-left-color: rgba(255, 255, 255, 0.2) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def setup_page_config():
    """
    Set up the page configuration for the Streamlit app.
    """
    st.set_page_config(
        page_title="AI Resume Analyzer",
        page_icon="📃",
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items={
            "Get Help": "https://github.com/RYZHAIEV-SERHII/resume-analyzer/issues",
            "Report a bug": "https://github.com/RYZHAIEV-SERHII/resume-analyzer/issues/new",
            "About": """
            # AI Resume Analyzer

            An innovative AI-powered tool crafted to evaluate resumes and provide tailored, actionable insights,
            empowering job seekers to refine their applications.

            Version: 0.1.0
            """,
        },
    )


def setup_ui():
    """
    Set up the UI for the Streamlit app.
    This function handles all UI elements initialization.
    """
    # Set up page config
    setup_page_config()

    # Set gradient background
    set_gradient_background()

    # Set up custom spinner
    setup_custom_spinner()

    # Load custom CSS
    if os.path.exists("src/static/styles.css"):
        load_css_file("src/static/styles.css")

    # Setup sidebar
    setup_sidebar()


def setup_sidebar():
    """
    Set up the sidebar for the Streamlit app.
    """
    # Safe direct access to sidebar - works in both real app and tests
    sidebar = st.sidebar

    # Add logo and title
    sidebar.image("https://img.icons8.com/fluency/96/resume.png", width=80)
    sidebar.title("Resume Analyzer")

    sidebar.markdown("---")
    sidebar.markdown("### About")
    sidebar.markdown("""
    This tool uses AI to analyze your resume and provide actionable feedback to help you improve it.

    Powered by Google Gemini 2.0 Flash via OpenRouter.
    """)

    sidebar.markdown("---")
    sidebar.markdown("### Features")
    sidebar.markdown("""
    - 📄 Supports PDF, DOCX, and TXT formats
    - 🎯 Job-specific analysis
    - 🤖 AI-powered feedback
    - 📊 Comprehensive insights
    - 🔒 Privacy-focused
    """)

    sidebar.markdown("---")
    sidebar.markdown("### Need Help?")
    sidebar.markdown(
        "[Documentation](https://github.com/RYZHAIEV-SERHII/resume-analyzer) | [Report Issues](https://github.com/RYZHAIEV-SERHII/resume-analyzer/issues)"
    )
