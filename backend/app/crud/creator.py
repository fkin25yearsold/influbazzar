from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models.creator import CreatorProfile
from app.db.models.user import User
from app.schemas.creator.profile import CreatorProfileCreate, CreatorProfileUpdate

def create_creator_profile(db: Session, user_id: str, data: CreatorProfileCreate) -> CreatorProfile:
    """
    Create a new creator profile and mark user as onboarded.
    This is called during the onboarding flow after email verification.
    """
    # Convert Pydantic model to dict, handling nested models
    profile_data = data.dict()
    
    # Create the profile
    profile = CreatorProfile(user_id=user_id, **profile_data)
    db.add(profile)
    
    # Mark user as having completed onboarding
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.has_completed_onboarding = True
    
    db.commit()
    db.refresh(profile)
    return profile

def get_creator_profile_by_user_id(db: Session, user_id: str) -> Optional[CreatorProfile]:
    """Get creator profile by user ID"""
    return db.query(CreatorProfile).filter(CreatorProfile.user_id == user_id).first()

def get_creator_profile_by_id(db: Session, profile_id: str) -> Optional[CreatorProfile]:
    """Get creator profile by profile ID"""
    return db.query(CreatorProfile).filter(CreatorProfile.id == profile_id).first()

def get_creator_profile_by_handle(db: Session, handle: str) -> Optional[CreatorProfile]:
    """Get creator profile by unique handle"""
    return db.query(CreatorProfile).filter(CreatorProfile.handle == handle).first()

def update_creator_profile(db: Session, user_id: str, data: CreatorProfileUpdate) -> Optional[CreatorProfile]:
    """Update creator profile with partial data"""
    profile = get_creator_profile_by_user_id(db, user_id)
    if not profile:
        return None
    
    # Update only provided fields
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

def get_public_creator_profiles(
    db: Session, 
    skip: int = 0, 
    limit: int = 20,
    content_type: Optional[str] = None,
    location: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> List[CreatorProfile]:
    """
    Get public creator profiles for discovery with filtering.
    Used by brands to find creators for campaigns.
    """
    query = db.query(CreatorProfile).filter(CreatorProfile.is_public == True)
    
    # Apply filters
    if content_type:
        query = query.filter(CreatorProfile.content_type == content_type)
    
    if location:
        query = query.filter(CreatorProfile.location.ilike(f"%{location}%"))
    
    if tags:
        # Filter by tags (PostgreSQL array contains)
        for tag in tags:
            query = query.filter(CreatorProfile.tags.any(tag))
    
    return query.offset(skip).limit(limit).all()

def update_creator_metrics(
    db: Session, 
    user_id: str, 
    campaigns_completed: int = 0,
    earnings_added: float = 0.0,
    engagement_rate: Optional[float] = None
) -> Optional[CreatorProfile]:
    """
    Update creator performance metrics.
    Called when campaigns are completed or metrics are recalculated.
    """
    profile = get_creator_profile_by_user_id(db, user_id)
    if not profile:
        return None
    
    # Update metrics
    profile.total_campaigns += campaigns_completed
    profile.total_earnings += earnings_added
    
    if engagement_rate is not None:
        profile.avg_engagement_rate = engagement_rate
    
    # Calculate XP score based on performance
    profile.xp_score = calculate_xp_score(profile)
    
    db.commit()
    db.refresh(profile)
    return profile

def calculate_xp_score(profile: CreatorProfile) -> float:
    """
    Calculate creator experience score based on various factors.
    This affects creator ranking in search results.
    """
    base_score = 0.0
    
    # Campaign completion bonus
    base_score += profile.total_campaigns * 10
    
    # Earnings factor
    base_score += min(profile.total_earnings / 100, 500)  # Cap at 500 points
    
    # Engagement rate bonus
    if profile.avg_engagement_rate:
        base_score += profile.avg_engagement_rate * 1000
    
    # Verification bonus
    if profile.is_verified:
        base_score += 100
    
    # Profile completeness bonus
    completeness = calculate_profile_completeness(profile)
    base_score += completeness * 50
    
    return round(base_score, 2)

def calculate_profile_completeness(profile: CreatorProfile) -> float:
    """Calculate profile completeness percentage (0.0 to 1.0)"""
    fields_to_check = [
        profile.bio,
        profile.profile_image_url,
        profile.platforms,
        profile.pricing_info,
        profile.tags,
        profile.location
    ]
    
    completed_fields = sum(1 for field in fields_to_check if field)
    return completed_fields / len(fields_to_check)