from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timedelta
from app.db.base import Base

class UserOTP(Base):
    __tablename__ = "user_otps"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    otp_code = Column(String(6), nullable=False)
    destination = Column(String, nullable=False)  # email
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Relationship
    user = relationship("User", backref="otps")
    
    @classmethod
    def create_with_expiry(cls, **kwargs):
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        return cls(expires_at=expires_at, **kwargs)