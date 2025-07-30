import os
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from docx import Document
from docx.opc.exceptions import OpcError

def read_txt_file(file_path: str) -> str:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
        return content
    except Exception as e:
        raise IOError(f"Error reading TXT file {file_path}: {e}")

def read_pdf_file(file_path: str) -> str:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    full_text = []
    try:
        reader = PdfReader(file_path)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                full_text.append(text)
    except PdfReadError as e:
        raise IOError(f"Error parsing PDF file {file_path}: {e}. Ensure it's not password-protected or corrupted.")
    except Exception as e:
        raise IOError(f"Unexpected error reading PDF file {file_path}: {e}")

    return "\n".join(full_text)

def read_docx_file(file_path: str) -> str:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    full_text = []
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            if para.text:
                full_text.append(para.text)
    except OpcError as e:
        raise IOError(f"Error parsing DOCX file {file_path}: {e}. Ensure it's a valid DOCX file.")
    except Exception as e:
        raise IOError(f"Unexpected error reading DOCX file {file_path}: {e}")

    return "\n".join(full_text)


def parse_document(file_path: str) -> str:

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.txt':
        return read_txt_file(file_path)
    elif file_extension == '.pdf':
        return read_pdf_file(file_path)
    elif file_extension == '.docx':
        return read_docx_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Currently only .txt, .pdf, and .docx are supported.")