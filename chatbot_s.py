import streamlit as st
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from unstructured.partition.pdf import partition_pdf
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# -------------------------------
# Load PDF
# -------------------------------
def load_pdf(file):
    elements = partition_pdf(file)
    text = "\n".join([str(el) for el in elements])
    return text

# -------------------------------
# Chunk Text
# -------------------------------
def chunk_text(text, chunk_size=500, overlap=50):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)

# -------------------------------
# Create Embeddings & Vector DB
# -------------------------------
def create_embeddings(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.from_texts(chunks, embeddings)
    return vector_db

# -------------------------------
# Setup Local LLM
# -------------------------------
def setup_local_llm():
    model_name = "TheBloke/wizardLM-7B-uncensored-HF"  # Example local model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16
    )
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7
    )
    return pipe

# -------------------------------
# Query Function (No LLMChain)
# -------------------------------
def answer_question(vector_db, llm_pipe, question, k=3):
    docs = vector_db.similarity_search(question, k=k)
    context = "\n".join([doc.page_content for doc in docs])
    
    prompt = f"Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    
    output = llm_pipe(prompt)
    return output[0]['generated_text']

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("📄 Multi-PDF Chatbot (Local RAG)")

uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    all_chunks = []
    for pdf_file in uploaded_files:
        raw_text = load_pdf(pdf_file)
        chunks = chunk_text(raw_text)
        all_chunks.extend(chunks)

    vector_db = create_embeddings(all_chunks)
    llm_pipe = setup_local_llm()

    st.session_state.vector_db = vector_db
    st.session_state.llm_pipe = llm_pipe

    st.success("✅ All PDFs processed and embeddings created!")

    question = st.text_input("Ask a question:")
    if question:
        answer = answer_question(st.session_state.vector_db, st.session_state.llm_pipe, question)
        st.markdown(f"**Answer:** {answer}")
