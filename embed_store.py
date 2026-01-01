# Import correct class
from langchain_huggingface import HuggingFaceEmbeddings
from pdf_loader import load_pdf
from textsplit import split_text
import chromadb

# Load PDF & split text
pdf_path = "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Internship_Data.pdf"
text = load_pdf(pdf_path)
chunks = split_text(text)

print("Total chunks:", len(chunks))
print("\nSample chunk:\n", chunks[0])
print("-"*80)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = [embedding_model.embed_query(chunk) for chunk in chunks]

# Initialize Chroma DB
client = chromadb.Client()
collection = client.create_collection("sunbeam_docs")

# Add chunks + embeddings + metadata
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embeddings[i]],
        metadatas=[{"page": i}]
    )

print("Vector DB created with", collection.count(), "entries")
print("-"*80)

# --------------------------
# Example Query
# --------------------------
query = "internship duration"
query_emb = embedding_model.embed_query(query)

results = collection.query(
    query_embeddings=[query_emb],
    n_results=3
)

print("Top relevant chunks for query:", query)
for doc in results['documents'][0]:
    print(doc)
    print("-"*80)
