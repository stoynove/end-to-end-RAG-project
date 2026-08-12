import os
from typing import List
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from backend.core.config import settings

class VectorStoreManager:
    def __init__(self):
        # We use a default model (text-embedding-3-small) to ensure lower cost and good performance
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        self.persist_directory = settings.CHROMA_DB_DIR
        
        # Initialize chroma db
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="rag_documents"
        )

    def add_documents(self, documents: List[Document]):
        """
        Add document chunks to the vector store.
        """
        if not documents:
            return
        self.vector_store.add_documents(documents=documents)

    def get_retriever(self, search_kwargs={"k": 4}):
        """
        Returns a retriever interface to search the vector store.
        """
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
