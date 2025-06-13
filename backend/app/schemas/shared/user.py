from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.db.models.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    role: UserRole
    is_verified: bool
    is_google_authenticated: bool
    has_completed_onboarding: bool  # Added for onboarding tracking
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    """Simplified user profile for JWT tokens and basic display"""
    id: str
    email: str
    role: UserRole
    has_completed_onboarding: bool
    
    class Config:
        from_attributes = True