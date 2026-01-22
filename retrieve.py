import os
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class BlockchainRAG:
    def __init__(self, db_path="faiss_index"):
        #loading the index
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vector_db = FAISS.load_local(
            db_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        
        #Llama 3.2
        self.llm = ChatOllama(model="llama3.2", temperature=0,timeout=120)

    def ask(self, query_text):
        template = """
        SYSTEM: You are a Blockchain Expert. Answer the question using the provided context.
        If the answer is not in the documents, say "I cannot find this in the technical whitepapers."
        Keep your answer technical and precise.
        
        QUESTION: {question}
        
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
       
    
if __name__ == "__main__":
    bot = BlockchainRAG()
    print("\nBlockBot is online!")
    while True:
        user_input = input("\nAsk a question (or type 'exit'): ")
        if user_input.lower() == 'exit':
            break
        response = bot.ask(user_input)
        print(f"\nAI: {response}")