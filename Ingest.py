import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

def start_fresh():
    # 1. Load documents
    print("📂 Loading Blockchain PDFs...")
    loader = DirectoryLoader("docs/", glob="./*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    
    # 2. Split into chunks
    print("✂️ Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(docs)

    # 3. Create math vectors (Ensure Ollama app is OPEN)
    print("🧠 Generating embeddings...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 4. Save safely
    print("💾 Saving to faiss_index...")
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("faiss_index")
    print("✅ SUCCESS! Fresh Blockchain index created.")

if __name__ == "__main__":
    start_fresh()