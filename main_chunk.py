from pdf_loader import text       # text from PDF
from textsplit import split_text

chunks = split_text(text)
print("Total chunks:", len(chunks))
print(chunks[0])