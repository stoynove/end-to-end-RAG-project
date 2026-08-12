from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from backend.services.document_processor import DocumentProcessor
from backend.services.vector_store import VectorStoreManager
from backend.services.llm_client import LLMClient

router = APIRouter()

# Initialize services
document_processor = DocumentProcessor()
vector_store_manager = VectorStoreManager()
llm_client = LLMClient()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    message: str
    filename: str

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a PDF document, processes it into chunks, and stores the embeddings in ChromaDB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        content = await file.read()
        
        # 1. Process document
        chunks = document_processor.process_pdf(content, file.filename)
        
        # 2. Store chunks in vector database
        vector_store_manager.add_documents(chunks)
        
        return UploadResponse(
            message=f"Successfully processed and stored {len(chunks)} chunks.",
            filename=file.filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Queries the RAG system using the provided question.
    """
    try:
        # 1. Get retriever
        retriever = vector_store_manager.get_retriever()
        
        # 2. Create RAG chain
        rag_chain = llm_client.create_rag_chain(retriever)
        
        # 3. Invoke chain
        response = rag_chain.invoke(request.question)
        
        return QueryResponse(answer=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
