import uuid
import enum
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, Enum, ForeignKey, JSON, Integer, Float, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ContentTypeEnum(str, enum.Enum):
    """Content types that creators can produce"""
    REELS = "Reels"
    STORIES = "Stories"
    POSTS = "Posts"
    YOUTUBE = "YouTube"
    BLOGS = "Blogs"
    ALL = "All"

class CreatorTypeEnum(str, enum.Enum):
    """Creator tier based on follower count and engagement"""
    NANO = "Nano"        # 1K-10K followers
    MICRO = "Micro"      # 10K-100K followers
    MACRO = "Macro"      # 100K-1M followers
    CELEBRITY = "Celebrity"  # 1M+ followers

class CreatorProfile(Base):
    """
    Creator profile model for influencers who apply to campaigns and earn money.
    Contains all necessary information for brand discovery and campaign matching.
    """
    __tablename__ = "creator_profiles"

    # Primary identifiers
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    # Basic profile information
    display_name = Column(String, nullable=False, comment="Public display name for the creator")
    handle = Column(String, unique=True, nullable=False, comment="Unique handle/username")
    bio = Column(Text, comment="Creator's bio/description")
    content_type = Column(Enum(ContentTypeEnum), nullable=False, comment="Primary content type")
    
    # Platform and audience data
    platforms = Column(JSON, nullable=True, comment="Platform data: [{'platform': 'instagram', 'followers': 50000}]")
    location = Column(String, comment="Geographic location")
    language = Column(String, comment="Primary language")
    
    # Pricing and business information
    pricing_info = Column(JSON, nullable=True, comment="Pricing structure: [{'platform': 'instagram', 'type': 'post', 'price': 500}]")
    
    # Media assets
    profile_image_url = Column(String, comment="Profile picture URL")
    cover_image_url = Column(String, comment="Cover/banner image URL")
    
    # Visibility and verification
    is_public = Column(Boolean, default=True, comment="Whether profile is publicly discoverable")
    is_verified = Column(Boolean, default=False, comment="Platform verification status")
    
    # Performance metrics (calculated fields)
    avg_engagement_rate = Column(Float, comment="Average engagement rate across platforms")
    total_campaigns = Column(Integer, default=0, comment="Total campaigns completed")
    total_earnings = Column(Float, default=0.0, comment="Total earnings from platform")
    xp_score = Column(Float, default=0.0, comment="Experience/reputation score")
    creator_type = Column(Enum(CreatorTypeEnum), nullable=True, comment="Creator tier classification")

    # Additional profile enhancements
    social_links = Column(JSON, nullable=True, comment="Social media links: {'instagram': 'url', 'tiktok': 'url'}")
    media_kit_url = Column(String, nullable=True, comment="Media kit PDF URL")
    portfolio_items = Column(JSON, nullable=True, comment="Portfolio items: [{'title': 'Campaign Name', 'url': 'link'}]")
    tags = Column(ARRAY(String), nullable=True, comment="Skill/niche tags for discovery")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship back to user
    user = relationship("User", backref="creator_profile")