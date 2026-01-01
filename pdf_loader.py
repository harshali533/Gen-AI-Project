from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from PyPDF2 import PdfReader

def load_pdf(pdf_path):
    """
    Loads a PDF file and returns its full text as a string.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

if __name__ == "__main__":
    pdf_path = r"D:\Day-1(CDAC)\git d-1\GenAI-94611\chatboat-project\data\Sunbeam_About_Us.pdf"
    text = load_pdf(pdf_path)
    print("Length of text:", len(text))
