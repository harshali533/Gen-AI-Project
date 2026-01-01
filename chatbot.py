# rag_backend.py

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

from logger import logger

logger.info("Chatbot initialized")


# ------------------ GLOBAL VECTORSTORE ------------------
vectorstore = None

# ------------------ PDF PATHS ------------------
pdf_paths = [
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_About_Us_1767189715.pdf",
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Contact_Centres.pdf",
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Internship_Data.pdf",
    "D:/Day-1(CDAC)/git d-1/GenAI-94611/chatboat-project/Sunbeam_Modular_Courses.pdf"
]

# ------------------ LOAD PDF ------------------
def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ------------------ BUILD VECTORSTORE ------------------
def init_vectorstore():
    global vectorstore

    if vectorstore is not None:
        return vectorstore  # already loaded

    print("🔹 Loading PDFs...")
    all_text = ""
    for path in pdf_paths:
        all_text += load_pdf(path) + "\n"

    print("🔹 Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_text(all_text)

    print("🔹 Creating embeddings & vector DB...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="vectordb"
    )

    print("✅ Vectorstore ready")
    return vectorstore

# ------------------ LLM (LM STUDIO) ------------------
llm = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    model="local-model",
    temperature=0.3
)

prompt = PromptTemplate(
    template="""
You are a helpful AI assistant for Sunbeam Infotech.

Use retrieved context if relevant.
If not available, answer using general knowledge.

Context:
{context}

Question:
{question}

Answer clearly:
"""
,
    input_variables=["context", "question"]
)


chain = prompt | llm | StrOutputParser()

# ------------------ GET ANSWER ------------------
def get_answer(query):
    vs = init_vectorstore()

    docs = vs.similarity_search(query, k=4)

    MAX_CHARS = 2500
    context = ""
    for d in docs:
        if len(context) + len(d.page_content) > MAX_CHARS:
            break
        context += d.page_content + "\n\n"

    return chain.invoke({
        "context": context,
        "question": query
    })
