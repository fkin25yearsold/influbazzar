from pydantic import BaseModel, HttpUrl, UUID4, EmailStr
from typing import Optional, Dict, List
from datetime import datetime
from app.db.models.brand import BrandTypeEnum

class BudgetRange(BaseModel):
    """Budget range for campaigns"""
    min: float
    max: float
    currency: str = "USD"

class CampaignPreferences(BaseModel):
    """Campaign targeting preferences"""
    platforms: Optional[List[str]] = None  # instagram, tiktok, youtube
    niches: Optional[List[str]] = None     # fashion, tech, food
    creator_tiers: Optional[List[str]] = None  # nano, micro, macro
    content_types: Optional[List[str]] = None  # posts, stories, reels

class BrandProfileBase(BaseModel):
    """Base brand profile schema with all editable fields"""
    brand_name: str
    industry: Optional[str] = None
    bio: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    language: Optional[str] = "English"
    contact_email: Optional[EmailStr] = None
    campaign_preferences: Optional[CampaignPreferences] = None
    budget_range: Optional[BudgetRange] = None
    brand_type: Optional[BrandTypeEnum] = None
    social_links: Optional[Dict[str, str]] = None

class BrandProfileCreate(BrandProfileBase):
    """Schema for creating a new brand profile during onboarding"""
    pass

class BrandProfileUpdate(BaseModel):
    """Schema for updating brand profile - all fields optional"""
    brand_name: Optional[str] = None
    industry: Optional[str] = None
    bio: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    language: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    campaign_preferences: Optional[CampaignPreferences] = None
    budget_range: Optional[BudgetRange] = None
    brand_type: Optional[BrandTypeEnum] = None
    social_links: Optional[Dict[str, str]] = None

class BrandProfileOut(BrandProfileBase):
    """Complete brand profile response with computed fields"""
    id: UUID4
    user_id: UUID4
    total_campaigns: int = 0
    total_spend: float = 0.0
    is_verified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BrandProfilePublic(BaseModel):
    """Public brand profile for creator discovery"""
    id: UUID4
    brand_name: str
    industry: Optional[str] = None
    bio: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    total_campaigns: int = 0
    is_verified: bool = False

    class Config:
        from_attributes = True