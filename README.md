# BLOCKBOT  
### A Technical Blockchain Assistant  
**Author:** Mihika Jain

BLOCKBOT is a Retrieval-Augmented Generation (RAG) based technical assistant designed to answer blockchain-related queries strictly using trusted documentation.

---

## 🚀 Key Features
- End-to-end RAG pipeline implementation  
- Semantic document search using vector embeddings  
- Context-aware response generation  
- Fast and efficient similarity search  
- Interactive web-based user interface  
- Fully built using open-source tools  

---

## 🧠 System Architecture

1. Documents are loaded and split into manageable chunks  
2. Each chunk is converted into vector embeddings  
3. Embeddings are stored in a FAISS vector database  
4. User query is embedded and matched against stored vectors  
5. Relevant document chunks are retrieved  
6. Retrieved context is passed to the LLM  
7. The LLM generates a response strictly based on retrieved data  

---

## 🔄 How It Works (The RAG Pipeline)
It is broadly divided into two steps - **Ingestion and Retrieval.**

**1. Ingestion**  
Extracting raw text from technical blockchain PDFs

**2. Chunking**  
Breaking large documents into smaller, meaningful pieces (chunks) of text before creating embeddings and storing them in a vector database. 

**3. Embedding**  
Converting text into high-dimensional numerical vectors  

**4. Indexing**  
Storing and organizing vectors for rapid similarity search  

**5. Retrieval**  
Finding the most relevant context for a user’s question  

**6. Generation**  
Synthesizing a final answer using only the retrieved context  

---

## 🛠️ Tech Stack

- **Language:** Python 3.11  
- **Orchestration:** LangChain  
- **LLM:** Llama 3.2 (3B)  
- **Embeddings:** Ollama Embeddings  
- **Vector Database:** FAISS 
- **Frontend:** Streamlit
- **Documents:** Google 

It answers all the questions which are related to the documents provided , here those documents are blockchain documents.


Demo screenshot link - https://drive.google.com/file/d/1ukNALKAR_2uXp4iiQEbZBkcz87a9eH_w/view?usp=drive_link

