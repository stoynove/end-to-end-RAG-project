from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.core.config import settings
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A Retrieval-Augmented Generation (RAG) system API.",
    version="0.1.0"
)

# Set up CORS for the frontend (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real production environment, specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API. Visit /docs for the interactive API documentation."}
