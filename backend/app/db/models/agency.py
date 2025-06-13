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

class AgencyTypeEnum(str, enum.Enum):
    """Agency service type classification"""
    CREATOR_MANAGEMENT = "Creator Management"    # Manages influencers
    BRAND_MANAGEMENT = "Brand Management"        # Manages brand campaigns
    FULL_SERVICE = "Full Service"                # Both creators and brands

class AgencyProfile(Base):
    """
    Agency profile model for firms that manage multiple creators and/or brands.
    Contains agency information, team details, and performance metrics.
    """
    __tablename__ = "agency_profiles"

    # Primary identifiers
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    # Basic agency information
    agency_name = Column(String, nullable=False, comment="Official agency name")
    agency_type = Column(Enum(AgencyTypeEnum), nullable=True, comment="Type of agency services")
    industry = Column(String, comment="Primary industry focus")
    bio = Column(Text, comment="Agency description and expertise")

    # Agency branding and online presence
    logo_url = Column(String, comment="Agency logo URL")
    website_url = Column(String, comment="Agency website URL")
    
    # Contact and location information
    location = Column(String, comment="Agency headquarters location")
    language = Column(String, comment="Primary business language")
    contact_email = Column(String, comment="Business contact email")
    contact_phone = Column(String, comment="Business phone number")
    
    # Social presence
    social_links = Column(JSON, nullable=True, comment="Agency social media links")

    # Verification status
    is_verified = Column(Boolean, default=False, comment="Agency verification status")

    # Performance and analytics metrics
    total_brands_managed = Column(Integer, default=0, comment="Number of brands under management")
    total_creators_managed = Column(Integer, default=0, comment="Number of creators under management")
    total_campaigns_run = Column(Integer, default=0, comment="Total campaigns executed")
    total_earnings = Column(Float, default=0.0, comment="Total agency earnings/commissions")
    total_spend_managed = Column(Float, default=0.0, comment="Total campaign spend managed")

    # Team management (optional feature for larger agencies)
    team_notes = Column(JSON, nullable=True, comment="Team member information: [{'name': 'John', 'role': 'Manager', 'email': 'john@agency.com'}]")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship back to user
    user = relationship("User", backref="agency_profile")