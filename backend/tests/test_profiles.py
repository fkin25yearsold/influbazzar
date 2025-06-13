import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_creator_profile_onboarding_without_auth():
    """Test that creator profile onboarding requires authentication"""
    response = client.post(
        "/api/creator/profile/onboarding",
        json={
            "display_name": "Test Creator",
            "handle": "testcreator",
            "bio": "I create amazing content!",
            "content_type": "Posts"
        }
    )
    assert response.status_code == 401

def test_brand_profile_onboarding_without_auth():
    """Test that brand profile onboarding requires authentication"""
    response = client.post(
        "/api/brand/profile/onboarding",
        json={
            "brand_name": "Test Brand",
            "industry": "Fashion",
            "bio": "We make great products!"
        }
    )
    assert response.status_code == 401

def test_agency_profile_onboarding_without_auth():
    """Test that agency profile onboarding requires authentication"""
    response = client.post(
        "/api/agency/profile/onboarding",
        json={
            "agency_name": "Test Agency",
            "agency_type": "Full Service",
            "bio": "We manage everything!"
        }
    )
    assert response.status_code == 401

def test_discover_creators():
    """Test creator discovery endpoint"""
    response = client.get("/api/creator/profile/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_discover_brands():
    """Test brand discovery endpoint"""
    response = client.get("/api/brand/profile/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_discover_agencies():
    """Test agency discovery endpoint"""
    response = client.get("/api/agency/profile/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_discover_creators_with_filters():
    """Test creator discovery with filters"""
    response = client.get(
        "/api/creator/profile/",
        params={
            "content_type": "Posts",
            "location": "New York",
            "limit": 10
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)