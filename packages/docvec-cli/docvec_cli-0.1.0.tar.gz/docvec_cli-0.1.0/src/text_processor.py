import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clean_text(text: str) -> str:

    if not isinstance(text, str):
        return ""

    clean_text = re.sub(r'<[^>]+>', '', text)

    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
    clean_text = re.sub(r'\r\n', '\n', clean_text)

    clean_text = re.sub(r'\s+', ' ', clean_text)

    clean_text = '\n'.join([line.strip() for line in clean_text.split('\n')])
    clean_text = clean_text.strip()

    return clean_text

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:

    if not isinstance(text, str) or not text:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunks = text_splitter.split_text(text)
    return chunks