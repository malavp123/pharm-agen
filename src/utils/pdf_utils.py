
import pdfplumber
import re

def extract_text_from_pdf(filepath):
    """Extract full text from a PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_text(text):
    """Basic cleaning: collapse whitespace, remove references like [1], [23], etc."""
    text = re.sub(r'\s+', ' ', text)  # normalize all whitespace
    text = re.sub(r'\[\d+\]', '', text)  # remove reference numbers like [1]
    text = re.sub(r'\s+([.,;:])', r'\1', text)  # remove spaces before punctuation
    return text.strip()

def chunk_text(text, max_tokens=200, overlap=50):
    """Break long text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_tokens
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap
    return chunks
