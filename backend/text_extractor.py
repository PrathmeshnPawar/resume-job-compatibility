import os
import PyPDF2
from docx import Document
from typing import Optional

def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extract text from PDF or DOCX files
    """
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['.doc', '.docx']:
            return extract_text_from_docx(file_path)
        else:
            print(f"Unsupported file type: {file_extension}")
            return None
            
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        text = f"Error extracting text from PDF: {e}"
    
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file
    """
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        text = f"Error extracting text from DOCX: {e}"
    
    return text.strip()

def clean_extracted_text(text: str) -> str:
    """
    Clean and normalize extracted text
    """
    if not text:
        return "No text extracted from file"
    
    # Remove excessive whitespace
    text = " ".join(text.split())
    
    # Remove common PDF artifacts
    text = text.replace("\x00", "")  # Remove null characters
    text = text.replace("\ufeff", "")  # Remove BOM
    
    return text.strip()
