import streamlit as st
from src.utils.text_extractor import extract_text_from_file
from src.services.ai_analyzer import analyze_resume


# Set up Streamlit UI
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📃", layout="centered")
st.title("AI Resume Analyzer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")

# UI Elements
uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
job_role = st.text_input("Enter the job role you are applying for (optional)")
analyze = st.button("Analyze Resume")

# Main application logic
if analyze and uploaded_file:
    try:
        # Extract text from the uploaded file
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content...")
            st.stop()

        # Analyze the resume using AI
        analysis_result = analyze_resume(file_content, job_role)

        # Display results
        st.markdown("### Analysis Results")
        st.markdown(analysis_result)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
