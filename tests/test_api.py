import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the RAG API" in response.json()["message"]

def test_query_endpoint_missing_body():
    response = client.post("/api/query")
    assert response.status_code == 422 # Unprocessable Entity due to missing body

def test_upload_endpoint_missing_file():
    response = client.post("/api/upload")
    assert response.status_code == 422 # Unprocessable Entity
