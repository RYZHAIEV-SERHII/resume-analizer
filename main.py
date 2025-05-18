import streamlit as st
from src.utils.text_extractor import extract_text_from_file
from src.services.ai_analyzer import analyze_resume
from src.utils.ui_utils import setup_ui


def main():
    # Initialize UI (includes sidebar setup)
    setup_ui()

    # Header section
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("<h1>📃 AI Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p>Upload your resume and get AI-powered feedback tailored to your needs!</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Info section
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown("""
        1. **Upload your resume** in PDF, DOCX, or TXT format
        2. **Enter the job role** you're applying for (optional but recommended)
        3. **Click Analyze** and get AI-powered feedback on:
            - Content clarity and impact
            - Skills presentation and relevance
            - Experience descriptions and achievements
            - ATS (Applicant Tracking System) optimization
            - Targeted improvements for specific roles
        """)

    # Upload section
    uploaded_file = st.file_uploader(
        "📤 Upload your resume", type=["pdf", "docx", "txt"]
    )

    # Job role input
    job_role = st.text_input("💼 Enter the job role you are applying for (optional)")

    # Analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze = st.button("🔍 Analyze Resume")

    # Main application logic
    if analyze and uploaded_file:
        try:
            # Extract text from the uploaded file first
            file_content = extract_text_from_file(uploaded_file)
            # Make sure to show error and stop execution for empty files
            if not file_content or not file_content.strip():
                st.error("⚠️ File does not have any content...")
                st.stop()

            with st.spinner("Analyzing your resume... This may take a moment."):
                # Show progress bar
                progress_bar = st.progress(0)

                st.info("📄 Extracting text from your resume...")
                progress_bar.progress(30)

                # Show file info
                file_info = f"File: {uploaded_file.name} ({round(len(file_content) / 1024, 2)} KB of text extracted)"
                st.success(f"✅ Text extraction complete! {file_info}")
                progress_bar.progress(50)

                # Analyze the resume using AI
                st.info("🧠 Analyzing your resume with AI...")
                if job_role:
                    st.info(f"🎯 Tailoring analysis for: {job_role}")

                try:
                    # Process the resume with the AI service
                    analysis_result = analyze_resume(file_content, job_role)
                    progress_bar.progress(100)

                    # Check if the result contains error info
                    if "Error Encountered" in analysis_result:
                        st.warning("⚠️ Analysis completed with limited functionality")

                except ValueError as e:
                    st.error(f"Configuration Error: {str(e)}")
                    st.error(
                        "Please check your .env file and make sure the OPENROUTER_API_KEY is set correctly."
                    )

                    # Provide a fallback result instead of stopping
                    analysis_result = f"""
                    # Resume Analysis (Offline Mode)
                    
                    We couldn't connect to our AI service due to a configuration error: {str(e)}
                    
                    ## General Resume Tips
                    1. Use clear, concise language to describe your experience
                    2. Quantify achievements with metrics when possible 
                    3. Tailor your resume for each job application
                    4. Ensure proper formatting and organization
                    5. Proofread carefully for errors
                    
                    Please check your API key configuration and try again.
                    """
                    progress_bar.progress(100)

                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")

                    # Provide a fallback result
                    analysis_result = f"""
                    # Resume Analysis (Offline Mode)
                    
                    We encountered an unexpected error: {str(e)}
                    
                    ## General Resume Tips
                    1. Use clear, concise language to describe your experience
                    2. Quantify achievements with metrics when possible
                    3. Tailor your resume for each job application
                    4. Ensure proper formatting and organization
                    5. Proofread carefully for errors
                    
                    Please try again later.
                    """
                    progress_bar.progress(100)

                # Display results
                st.markdown("### 📊 Analysis Results")

                st.markdown(analysis_result)

                # Add download button for results
                st.download_button(
                    label="📥 Download Analysis",
                    data=analysis_result,
                    file_name="resume_analysis.txt",
                    mime="text/plain",
                )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Footer
    st.markdown(
        """
        <div class="footer">
            <p>Made with ❤️ by <a href="https://github.com/RYZHAIEV-SERHII" target="_blank">Serhii Ryzhaiev</a></p>
            <p>Powered by <a href="https://streamlit.io" target="_blank">Streamlit</a> and
            <a href="https://openrouter.ai" target="_blank">OpenRouter</a> (Gemini 2.0)</p>
            <p><a href="https://github.com/RYZHAIEV-SERHII/resume-analyzer" target="_blank">GitHub Repository</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
