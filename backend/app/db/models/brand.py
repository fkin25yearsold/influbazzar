import uuid
import enum
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey,
    JSON, Integer, Float, Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class BrandTypeEnum(str, enum.Enum):
    """Brand classification types"""
    D2C = "D2C"                    # Direct-to-consumer
    AGENCY = "Agency"              # Marketing agency
    ENTERPRISE = "Enterprise"      # Large corporation
    STARTUP = "Startup"            # Early-stage company

class BrandProfile(Base):
    """
    Brand profile model for businesses who run influencer campaigns.
    Contains company information, campaign preferences, and budget data.
    """
    __tablename__ = "brand_profiles"

    # Primary identifiers
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    # Basic brand information
    brand_name = Column(String, nullable=False, comment="Official brand/company name")
    industry = Column(String, comment="Industry sector (e.g., Fashion, Tech, Food)")
    bio = Column(Text, comment="Brand description and values")
    
    # Brand assets and online presence
    logo_url = Column(String, comment="Brand logo URL")
    website_url = Column(String, comment="Official website URL")
    
    # Contact and location
    location = Column(String, comment="Brand headquarters location")
    language = Column(String, comment="Primary business language")
    contact_email = Column(String, comment="Business contact email")

    # Campaign preferences and targeting
    campaign_preferences = Column(JSON, nullable=True, comment="Preferred platforms, niches: {'platforms': ['instagram'], 'niches': ['fashion']}")
    budget_range = Column(JSON, nullable=True, comment="Budget range: {'min': 5000, 'max': 20000}")

    # Performance metrics
    total_campaigns = Column(Integer, default=0, comment="Total campaigns launched")
    total_spend = Column(Float, default=0.0, comment="Total amount spent on campaigns")
    
    # Verification and classification
    is_verified = Column(Boolean, default=False, comment="Brand verification status")
    brand_type = Column(Enum(BrandTypeEnum), nullable=True, comment="Brand classification")

    # Social presence
    social_links = Column(JSON, nullable=True, comment="Brand social media links")
    
    # Agency relationship (if managed by an agency)
    agency_id = Column(UUID(as_uuid=True), ForeignKey("agency_profiles.id"), nullable=True, comment="Managing agency ID if applicable")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="brand_profile")
    # agency = relationship("AgencyProfile", backref="managed_brands")