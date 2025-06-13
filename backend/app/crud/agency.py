from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models.agency import AgencyProfile
from app.db.models.user import User
from app.schemas.agency.profile import AgencyProfileCreate, AgencyProfileUpdate

def create_agency_profile(db: Session, user_id: str, data: AgencyProfileCreate) -> AgencyProfile:
    """
    Create a new agency profile and mark user as onboarded.
    This is called during the onboarding flow after email verification.
    """
    # Convert Pydantic model to dict
    profile_data = data.dict()
    
    # Create the profile
    profile = AgencyProfile(user_id=user_id, **profile_data)
    db.add(profile)
    
    # Mark user as having completed onboarding
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.has_completed_onboarding = True
    
    db.commit()
    db.refresh(profile)
    return profile

def get_agency_profile_by_user_id(db: Session, user_id: str) -> Optional[AgencyProfile]:
    """Get agency profile by user ID"""
    return db.query(AgencyProfile).filter(AgencyProfile.user_id == user_id).first()

def get_agency_profile_by_id(db: Session, profile_id: str) -> Optional[AgencyProfile]:
    """Get agency profile by profile ID"""
    return db.query(AgencyProfile).filter(AgencyProfile.id == profile_id).first()

def update_agency_profile(db: Session, user_id: str, data: AgencyProfileUpdate) -> Optional[AgencyProfile]:
    """Update agency profile with partial data"""
    profile = get_agency_profile_by_user_id(db, user_id)
    if not profile:
        return None
    
    # Update only provided fields
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

def get_public_agency_profiles(
    db: Session, 
    skip: int = 0, 
    limit: int = 20,
    agency_type: Optional[str] = None,
    industry: Optional[str] = None,
    location: Optional[str] = None
) -> List[AgencyProfile]:
    """
    Get public agency profiles for discovery.
    Used by brands and creators to find agency partners.
    """
    query = db.query(AgencyProfile)
    
    # Apply filters
    if agency_type:
        query = query.filter(AgencyProfile.agency_type == agency_type)
    
    if industry:
        query = query.filter(AgencyProfile.industry.ilike(f"%{industry}%"))
    
    if location:
        query = query.filter(AgencyProfile.location.ilike(f"%{location}%"))
    
    return query.offset(skip).limit(limit).all()

def update_agency_metrics(
    db: Session, 
    user_id: str, 
    brands_added: int = 0,
    creators_added: int = 0,
    campaigns_run: int = 0,
    earnings_added: float = 0.0,
    spend_managed: float = 0.0
) -> Optional[AgencyProfile]:
    """
    Update agency performance metrics.
    Called when agencies manage new clients or complete campaigns.
    """
    profile = get_agency_profile_by_user_id(db, user_id)
    if not profile:
        return None
    
    # Update metrics
    profile.total_brands_managed += brands_added
    profile.total_creators_managed += creators_added
    profile.total_campaigns_run += campaigns_run
    profile.total_earnings += earnings_added
    profile.total_spend_managed += spend_managed
    
    db.commit()
    db.refresh(profile)
    return profile

def get_agency_dashboard_stats(db: Session, user_id: str) -> Optional[dict]:
    """
    Get comprehensive dashboard statistics for an agency.
    Returns key metrics for the agency dashboard UI.
    """
    profile = get_agency_profile_by_user_id(db, user_id)
    if not profile:
        return None
    
    return {
        "total_brands": profile.total_brands_managed,
        "total_creators": profile.total_creators_managed,
        "total_campaigns": profile.total_campaigns_run,
        "total_earnings": profile.total_earnings,
        "total_spend_managed": profile.total_spend_managed,
        "avg_campaign_value": (
            profile.total_spend_managed / profile.total_campaigns_run 
            if profile.total_campaigns_run > 0 else 0
        ),
        "commission_rate": (
            (profile.total_earnings / profile.total_spend_managed * 100) 
            if profile.total_spend_managed > 0 else 0
        )
    }