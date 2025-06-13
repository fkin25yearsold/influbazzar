from pydantic import BaseModel, HttpUrl, UUID4, EmailStr
from typing import Optional, Dict, List
from datetime import datetime
from app.db.models.agency import AgencyTypeEnum

class TeamMember(BaseModel):
    """Team member information"""
    name: str
    role: str
    email: EmailStr
    phone: Optional[str] = None

class AgencyProfileBase(BaseModel):
    """Base agency profile schema with all editable fields"""
    agency_name: str
    agency_type: Optional[AgencyTypeEnum] = None
    industry: Optional[str] = None
    bio: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    language: Optional[str] = "English"
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None
    team_notes: Optional[List[TeamMember]] = None

class AgencyProfileCreate(AgencyProfileBase):
    """Schema for creating a new agency profile during onboarding"""
    pass

class AgencyProfileUpdate(BaseModel):
    """Schema for updating agency profile - all fields optional"""
    agency_name: Optional[str] = None
    agency_type: Optional[AgencyTypeEnum] = None
    industry: Optional[str] = None
    bio: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    language: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None
    team_notes: Optional[List[TeamMember]] = None

class AgencyProfileOut(AgencyProfileBase):
    """Complete agency profile response with computed fields"""
    id: UUID4
    user_id: UUID4
    is_verified: bool = False
    total_brands_managed: int = 0
    total_creators_managed: int = 0
    total_campaigns_run: int = 0
    total_earnings: float = 0.0
    total_spend_managed: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgencyProfilePublic(BaseModel):
    """Public agency profile for discovery"""
    id: UUID4
    agency_name: str
    agency_type: Optional[AgencyTypeEnum] = None
    industry: Optional[str] = None
    bio: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    total_campaigns_run: int = 0
    is_verified: bool = False

    class Config:
        from_attributes = True