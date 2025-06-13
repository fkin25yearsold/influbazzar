import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_creator_signup():
    """Test creator signup flow"""
    response = client.post(
        "/auth/creator/signup",
        json={
            "email": "creator@test.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "OTP sent to your email" in data["message"]
    assert data["email"] == "creator@test.com"

def test_brand_signup():
    """Test brand signup flow"""
    response = client.post(
        "/auth/brand/signup",
        json={
            "email": "brand@test.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "OTP sent to your email" in data["message"]
    assert data["email"] == "brand@test.com"

def test_agency_signup():
    """Test agency signup flow"""
    response = client.post(
        "/auth/agency/signup",
        json={
            "email": "agency@test.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "OTP sent to your email" in data["message"]
    assert data["email"] == "agency@test.com"

def test_duplicate_email_signup():
    """Test that duplicate email signup fails"""
    # First signup
    client.post(
        "/auth/creator/signup",
        json={
            "email": "duplicate@test.com",
            "password": "testpassword123"
        }
    )
    
    # Second signup with same email
    response = client.post(
        "/auth/creator/signup",
        json={
            "email": "duplicate@test.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Influbazzar API" in data["message"]
    assert "features" in data