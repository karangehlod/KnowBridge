import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_paper():
    response = client.post("/papers/", json={"title": "Quantum Computing for Protein Folding", "abstract": "Abstract text", "publication_date": "2023-01-01", "keywords": "quantum, computing, protein, folding"})
    assert response.status_code == 200
    assert response.json()["title"] == "Quantum Computing for Protein Folding"

def test_add_researcher():
    response = client.post("/researchers/", json={"name": "Dr. Smith", "affiliation": "University X", "expertise": "Quantum Computing"})
    assert response.status_code == 200
    assert response.json()["name"] == "Dr. Smith"

def test_add_topic():
    response = client.post("/topics/", json={"name": "Quantum Computing"})
    assert response.status_code == 200
    assert response.json()["name"] == "Quantum Computing"
