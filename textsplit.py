from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text, chunk_size=500, chunk_overlap=50):
    """
    Splits a text string into chunks using RecursiveCharacterTextSplitter.
    """
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", "!", "?", ",", " "],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    return chunks

if __name__ == "__main__":
    from pdf_loader import load_pdf
    pdf_path = "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Internship_Data.pdf"
    text = load_pdf(pdf_path)
    chunks = split_text(text)
    print("Total chunks:", len(chunks))
    print("Sample chunk:\n", chunks[0])

MAX_CHARS = 3000  # roughly under 4000 tokens
final_context = ""
for d in docs:
    if len(final_context) + len(d.page_content) > MAX_CHARS:
        break
    final_context += d.page_content + "\n\n"
