from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from backend.core.config import settings

class LLMClient:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
        
        # Define the system prompt for the RAG task
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the user's question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\n\nContext:\n{context}"),
            ("human", "{question}")
        ])

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def create_rag_chain(self, retriever):
        """
        Creates a RAG chain that connects the retriever, prompt, and LLM.
        """
        rag_chain = (
            {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        return rag_chain
