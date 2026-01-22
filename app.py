import os
import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class BlockchainRAG:
    def __init__(self, db_path="faiss_index"):
        # Load embeddings
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # Load FAISS index
        self.vector_db = FAISS.load_local(
            db_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        # LLM
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0,
            timeout=120
        )

    def ask(self, query_text):
        template = """
        SYSTEM: You are a Blockchain Expert. Answer the question using the provided context.
        If the answer is not in the documents, say "I cannot find this in the technical whitepapers."
        Keep your answer technical and precise.

        CONTEXT:
        {context}

        QUESTION:
        {question}

        ANSWER:
        """
        prompt = ChatPromptTemplate.from_template(template)

        retriever = self.vector_db.as_retriever(search_kwargs={"k": 2})

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke(query_text)


# ---------------- Streamlit UI ---------------- #

st.set_page_config(page_title="BlockBot", layout="centered")

st.title("🔗 BlockBot – Blockchain RAG Assistant")
st.caption("Answers strictly from blockchain technical whitepapers")

@st.cache_resource
def load_bot():
    return BlockchainRAG()

bot = load_bot()

user_query = st.text_input("Ask a blockchain question:")

if st.button("Ask"):
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching whitepapers..."):
            response = bot.ask(user_query)
        st.markdown("### 🤖 Answer")
        st.write(response)
