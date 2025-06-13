from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import require_brand, require_onboarded_brand
from app.db.models.user import User
from app.schemas.brand.profile import (
    BrandProfileCreate, 
    BrandProfileUpdate, 
    BrandProfileOut,
    BrandProfilePublic
)
from app.schemas.shared.token import LoginResponse
from app.schemas.shared.user import UserProfile
from app.core.security import create_token_with_onboarding_status
from app.crud.brand import (
    create_brand_profile,
    get_brand_profile_by_user_id,
    get_brand_profile_by_id,
    update_brand_profile,
    get_public_brand_profiles
)

router = APIRouter(prefix="/brand/profile", tags=["Brand Profile"])

@router.post("/onboarding", response_model=LoginResponse)
async def complete_brand_onboarding(
    profile_data: BrandProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_brand)
):
    """
    Complete brand onboarding by creating profile.
    This endpoint is called after email verification to set up the brand's profile.
    Returns a new JWT token with updated onboarding status.
    """
    # Check if profile already exists
    existing_profile = get_brand_profile_by_user_id(db, str(current_user.id))
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brand profile already exists. Use PUT /brand/profile to update."
        )
    
    # Create profile and mark user as onboarded
    profile = create_brand_profile(db, str(current_user.id), profile_data)
    
    # Refresh user to get updated onboarding status
    db.refresh(current_user)
    
    # Generate new token with updated onboarding status
    access_token = create_token_with_onboarding_status(current_user)
    
    return LoginResponse(
        access_token=access_token,
        user=UserProfile(
            id=str(current_user.id),
            email=current_user.email,
            role=current_user.role,
            has_completed_onboarding=True
        )
    )

@router.get("/me", response_model=BrandProfileOut)
async def get_my_brand_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_brand)
):
    """
    Get the current brand's profile.
    Requires completed onboarding.
    """
    profile = get_brand_profile_by_user_id(db, str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand profile not found."
        )
    return profile

@router.put("/", response_model=BrandProfileOut)
async def update_my_brand_profile(
    profile_data: BrandProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_brand)
):
    """
    Update the current brand's profile.
    Only provided fields will be updated.
    """
    profile = update_brand_profile(db, str(current_user.id), profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand profile not found."
        )
    return profile

@router.get("/{profile_id}", response_model=BrandProfilePublic)
async def get_public_brand_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a public brand profile by ID.
    Used by creators and agencies to view brand information.
    """
    profile = get_brand_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand profile not found."
        )
    
    return profile

@router.get("/", response_model=List[BrandProfilePublic])
async def discover_brands(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    location: Optional[str] = Query(None, description="Filter by location"),
    brand_type: Optional[str] = Query(None, description="Filter by brand type")
):
    """
    Discover brand profiles with filtering.
    Used by creators and agencies to find potential brand partners.
    """
    profiles = get_public_brand_profiles(
        db=db,
        skip=skip,
        limit=limit,
        industry=industry,
        location=location,
        brand_type=brand_type
    )
    
    return profiles