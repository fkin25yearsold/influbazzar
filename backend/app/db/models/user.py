from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from app.db.base import Base

class UserRole(str, enum.Enum):
    CREATOR = "creator"
    BRAND = "brand"
    AGENCY = "agency"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)  # Nullable for Google users
    role = Column(Enum(UserRole), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_google_authenticated = Column(Boolean, default=False)
    has_completed_onboarding = Column(Boolean, default=False)  # Added for onboarding tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())