import pdfplumber
import docx
import os

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file with page metadata."""
    extracted_data = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_data.append({'page': i + 1, 'text': page_text})
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return []
    return extracted_data

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file with mock page metadata (paragraphs)."""
    extracted_data = []
    try:
        doc = docx.Document(file_path)
        # DOCX doesn't have strict pages, so we'll group paragraphs or just treat them as semantic units.
        # For simplicity in this MVP, let's treat every 10 paragraphs as a "page" or just return raw text blocks.
        # Better yet, let's just return the whole thing as Page 1 for now if pagination isn't critical,
        # OR better: treat each section/paragraph as a unit. 
        # Let's stick to a simple accumulation for now, but wrapped in a list.
        
        full_text = ""
        for para in doc.paragraphs:
            if para.text.strip():
                full_text += para.text + "\n"
        
        if full_text:
            extracted_data.append({'page': 1, 'text': full_text})
            
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return []
    return extracted_data

def extract_text(file_path):
    """Dispatcher function to extract text based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return []
