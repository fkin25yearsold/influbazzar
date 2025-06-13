from pydantic import BaseModel, HttpUrl, UUID4
from typing import List, Optional, Dict
from datetime import datetime
from app.db.models.creator import ContentTypeEnum, CreatorTypeEnum

class PlatformInfo(BaseModel):
    """Platform follower information for creators"""
    platform: str
    followers: int
    engagement_rate: Optional[float] = None

class PricingInfo(BaseModel):
    """Pricing structure for different content types"""
    platform: str
    content_type: str  # post, story, reel, video
    price: float
    currency: str = "USD"

class PortfolioItem(BaseModel):
    """Portfolio/case study items"""
    title: str
    description: Optional[str] = None
    url: HttpUrl
    thumbnail_url: Optional[str] = None

class CreatorProfileBase(BaseModel):
    """Base creator profile schema with all editable fields"""
    display_name: str
    handle: str
    bio: Optional[str] = None
    content_type: ContentTypeEnum
    platforms: Optional[List[PlatformInfo]] = None
    location: Optional[str] = None
    language: Optional[str] = "English"
    pricing_info: Optional[List[PricingInfo]] = None
    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_public: Optional[bool] = True
    creator_type: Optional[CreatorTypeEnum] = None
    social_links: Optional[Dict[str, str]] = None
    media_kit_url: Optional[str] = None
    portfolio_items: Optional[List[PortfolioItem]] = None
    tags: Optional[List[str]] = None

class CreatorProfileCreate(CreatorProfileBase):
    """Schema for creating a new creator profile during onboarding"""
    pass

class CreatorProfileUpdate(BaseModel):
    """Schema for updating creator profile - all fields optional"""
    display_name: Optional[str] = None
    bio: Optional[str] = None
    content_type: Optional[ContentTypeEnum] = None
    platforms: Optional[List[PlatformInfo]] = None
    location: Optional[str] = None
    language: Optional[str] = None
    pricing_info: Optional[List[PricingInfo]] = None
    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_public: Optional[bool] = None
    creator_type: Optional[CreatorTypeEnum] = None
    social_links: Optional[Dict[str, str]] = None
    media_kit_url: Optional[str] = None
    portfolio_items: Optional[List[PortfolioItem]] = None
    tags: Optional[List[str]] = None

class CreatorProfileOut(CreatorProfileBase):
    """Complete creator profile response with computed fields"""
    id: UUID4
    user_id: UUID4
    avg_engagement_rate: Optional[float] = None
    total_campaigns: int = 0
    total_earnings: float = 0.0
    xp_score: float = 0.0
    is_verified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CreatorProfilePublic(BaseModel):
    """Public creator profile for discovery (excludes sensitive data)"""
    id: UUID4
    display_name: str
    handle: str
    bio: Optional[str] = None
    content_type: ContentTypeEnum
    platforms: Optional[List[PlatformInfo]] = None
    location: Optional[str] = None
    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    creator_type: Optional[CreatorTypeEnum] = None
    tags: Optional[List[str]] = None
    avg_engagement_rate: Optional[float] = None
    total_campaigns: int = 0
    xp_score: float = 0.0
    is_verified: bool = False

    class Config:
        from_attributes = True