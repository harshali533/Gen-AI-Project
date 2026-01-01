from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf_loader import load_pdf  # your function to load PDFs

pdf_paths = [
    r"D:\Day-1(CDAC)\git d-1\GenAI-94611\chatboat-project\Sunbeam_About_Us.pdf",
    r"D:\Day-1(CDAC)\git d-1\GenAI-94611\chatboat-project\Sunbeam_Contact_Centres.pdf",
    r"D:\Day-1(CDAC)\git d-1\GenAI-94611\chatboat-project\Sunbeam_Internship_Data.pdf",
    r"D:\Day-1(CDAC)\git d-1\GenAI-94611\chatboat-project\Sunbeam_Modular_Courses.pdf"
]

# 1️⃣ Load all PDF text
all_text = ""
for path in pdf_paths:
    all_text += load_pdf(path) + "\n"

# 2️⃣ Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=50
)
chunks = text_splitter.split_text(all_text)

# 3️⃣ Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4️⃣ Create vectorstore from chunks
vectorstore = Chroma.from_texts(
    texts=chunks,          # ✅ Use your chunks here
    embedding=embeddings,
    persist_directory="vectordb"
)

# 5️⃣ Persist (optional; Chroma auto-persist now)
vectorstore.persist()

print("✅ Vector DB created and saved with all PDF chunks")
