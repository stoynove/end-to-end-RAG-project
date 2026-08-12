import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG API"
    OPENAI_API_KEY: str = ""
    CHROMA_DB_DIR: str = "./chroma_db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
