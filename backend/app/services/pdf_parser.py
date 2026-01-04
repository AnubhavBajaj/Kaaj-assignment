import pdfplumber
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text_content = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
                
                # Also try to extract tables if needed, but for now simple text extraction
                # is often enough if the layout is preserved well.
                # tables = page.extract_tables()
                # for table in tables:
                #     text_content.append(str(table))

        return "\n".join(text_content)
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}")
        raise
