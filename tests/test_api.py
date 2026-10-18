import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_get_projects_public():
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_profile_public():
    response = client.get("/api/v1/content/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Shashidhar P C"

def test_unauthorized_dashboard_access():
    response = client.get("/api/v1/dashboard/layout")
    assert response.status_code == 401
