# Retrieval-Augmented Generation (RAG) System

This is an end-to-end RAG system built with FastAPI, Streamlit, ChromaDB, and OpenAI, designed to demonstrate practical engineering skills alongside data science concepts.

## Architecture

*   **Backend (FastAPI):** Exposes REST API endpoints for uploading documents and querying the RAG system. It utilizes object-oriented principles to decouple the `DocumentProcessor`, `VectorStoreManager`, and `LLMClient`.
*   **Frontend (Streamlit):** Provides a simple and interactive user interface for uploading PDF files and chatting with the embedded content.
*   **Vector Database (ChromaDB):** Used to store document embeddings locally.
*   **LLM (OpenAI):** Uses `gpt-4o-mini` for generation and `text-embedding-3-small` for embeddings via LangChain.
*   **Dependency Management:** `uv` is used for fast, modern dependency resolution and environment management.

## Project Structure

```
├── backend/            # FastAPI backend application
│   ├── api/            # API endpoints (routers)
│   ├── core/           # Configuration and settings
│   └── services/       # Core business logic (RAG, LLM, Vector Store)
├── frontend/           # Streamlit application
├── tests/              # Pytest unit tests
├── .env.example        # Environment variable template
├── pyproject.toml      # Project dependencies managed by uv
├── Dockerfile.backend  # Docker instructions for backend
├── Dockerfile.frontend # Docker instructions for frontend
└── docker-compose.yml  # Orchestrates both services
```

## Setup & Execution

### Option 1: Running with Docker (Recommended)

1.  Clone the repository and navigate into the folder.
2.  Copy the environment template:
    ```bash
    cp .env.example .env
    ```
3.  Add your OpenAI API key to the `.env` file:
    ```
    OPENAI_API_KEY=sk-your_api_key
    ```
4.  Run the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```
5.  Access the applications:
    *   **Frontend:** `http://localhost:8501`
    *   **Backend API Docs:** `http://localhost:8000/docs`

### Option 2: Running Locally (Development)

1.  Ensure you have [uv](https://github.com/astral-sh/uv) installed.
2.  Install dependencies:
    ```bash
    uv sync
    ```
3.  Set up your `.env` file (same as above).
4.  Run the backend:
    ```bash
    uv run uvicorn backend.main:app --reload --port 8000
    ```
5.  Run the frontend (in a new terminal):
    ```bash
    uv run streamlit run frontend/app.py
    ```

## CI/CD Pipeline

This repository uses GitHub Actions for continuous integration. On every push and pull request to the `main` branch, the pipeline will:
1. Setup Python and `uv`.
2. Install all dependencies.
3. Run the unit tests suite with `pytest`.
