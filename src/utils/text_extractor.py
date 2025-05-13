"""
Text extraction utilities for different file formats.
"""

import io
import PyPDF2
from docx import Document


def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.

    Args:
        pdf_file: A file-like object containing PDF data

    Returns:
        str: Extracted text from the PDF
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(docx_file):
    """
    Extract text from a DOCX file.

    Args:
        docx_file: A file-like object containing DOCX data

    Returns:
        str: Extracted text from the DOCX
    """
    doc = Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def extract_text_from_file(uploaded_file):
    """
    Extract text from supported file formats (PDF, DOCX, TXT).

    Args:
        uploaded_file: A file object (typically from Streamlit's file_uploader)

    Returns:
        str: Extracted text from the file
    """
    # Get the file content
    file_content = uploaded_file.read()

    # Handle different file types
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(file_content))

    elif (
        uploaded_file.type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        return extract_text_from_docx(io.BytesIO(file_content))

    # Default case: assume it's a text file
    try:
        return file_content.decode("utf-8")
    except UnicodeDecodeError:
        return (
            "Could not decode the file. Please upload a valid text, PDF, or DOCX file."
        )
