from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# -------------------------------
# Config
# -------------------------------
DB_DIR = "vectordb"
PDF_DIRS = [
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_About_Us_1767189715.pdf",
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Contact_Centres.pdf",
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Internship_Data.pdf",
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Modular_Courses.pdf"

    # Add all your PDF paths here
]

# -------------------------------
# Embeddings
# -------------------------------
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# -------------------------------
# Vector DB
# -------------------------------
vectorstore = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

# -------------------------------
# Load PDFs into Vector DB
# -------------------------------
for pdf_file in PDF_DIRS:
    loader = PyPDFLoader(pdf_file)
    docs = loader.load()
    vectorstore.add_documents(docs)

# Persist the DB
vectorstore.persist()

print("✅ All PDFs loaded into Vector DB")
