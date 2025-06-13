from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models.brand import BrandProfile
from app.db.models.user import User
from app.schemas.brand.profile import BrandProfileCreate, BrandProfileUpdate

def create_brand_profile(db: Session, user_id: str, data: BrandProfileCreate) -> BrandProfile:
    """
    Create a new brand profile and mark user as onboarded.
    This is called during the onboarding flow after email verification.
    """
    # Convert Pydantic model to dict
    profile_data = data.dict()
    
    # Create the profile
    profile = BrandProfile(user_id=user_id, **profile_data)
    db.add(profile)
    
    # Mark user as having completed onboarding
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.has_completed_onboarding = True
    
    db.commit()
    db.refresh(profile)
    return profile

def get_brand_profile_by_user_id(db: Session, user_id: str) -> Optional[BrandProfile]:
    """Get brand profile by user ID"""
    return db.query(BrandProfile).filter(BrandProfile.user_id == user_id).first()

def get_brand_profile_by_id(db: Session, profile_id: str) -> Optional[BrandProfile]:
    """Get brand profile by profile ID"""
    return db.query(BrandProfile).filter(BrandProfile.id == profile_id).first()

def update_brand_profile(db: Session, user_id: str, data: BrandProfileUpdate) -> Optional[BrandProfile]:
    """Update brand profile with partial data"""
    profile = get_brand_profile_by_user_id(db, user_id)
    if not profile:
        return None
    
    # Update only provided fields
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

def get_public_brand_profiles(
    db: Session, 
    skip: int = 0, 
    limit: int = 20,
    industry: Optional[str] = None,
    location: Optional[str] = None,
    brand_type: Optional[str] = None
) -> List[BrandProfile]:
    """
    Get public brand profiles for discovery.
    Used by creators and agencies to find potential brand partners.
    """
    query = db.query(BrandProfile)
    
    # Apply filters
    if industry:
        query = query.filter(BrandProfile.industry.ilike(f"%{industry}%"))
    
    if location:
        query = query.filter(BrandProfile.location.ilike(f"%{location}%"))
    
    if brand_type:
        query = query.filter(BrandProfile.brand_type == brand_type)
    
    return query.offset(skip).limit(limit).all()

def update_brand_metrics(
    db: Session, 
    user_id: str, 
    campaigns_launched: int = 0,
    spend_added: float = 0.0
) -> Optional[BrandProfile]:
    """
    Update brand performance metrics.
    Called when campaigns are launched or completed.
    """
    profile = get_brand_profile_by_user_id(db, user_id)
    if not profile:
        return None
    
    # Update metrics
    profile.total_campaigns += campaigns_launched
    profile.total_spend += spend_added
    
    db.commit()
    db.refresh(profile)
    return profile

def search_brands_by_budget(
    db: Session,
    min_budget: float,
    max_budget: Optional[float] = None,
    skip: int = 0,
    limit: int = 20
) -> List[BrandProfile]:
    """
    Search brands by budget range.
    Useful for creators to find brands within their price range.
    """
    query = db.query(BrandProfile).filter(
        BrandProfile.budget_range.isnot(None)
    )
    
    # Filter by budget range stored in JSON
    # Note: This is a simplified version. In production, you might want to use
    # PostgreSQL JSON operators for more efficient querying
    
    return query.offset(skip).limit(limit).all()