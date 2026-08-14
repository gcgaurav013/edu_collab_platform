import PyPDF2
import io

def extract_text(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    Includes basic cleaning for research-ready processing.
    """
    try:
        # Read the PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        full_text = []
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text)
        
        # Join pages and clean whitespace
        combined_text = "\n".join(full_text)
        cleaned_text = " ".join(combined_text.split())
        
        return cleaned_text
    
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def get_document_stats(text):
    """
    Returns basic metadata about the extracted text for the UI.
    """
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "estimated_reading_time": len(words) // 200 # Standard 200 wpm
    }