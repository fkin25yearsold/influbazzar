from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import require_creator, require_onboarded_creator
from app.db.models.user import User
from app.schemas.creator.profile import (
    CreatorProfileCreate, 
    CreatorProfileUpdate, 
    CreatorProfileOut,
    CreatorProfilePublic
)
from app.schemas.shared.token import LoginResponse
from app.schemas.shared.user import UserProfile
from app.core.security import create_token_with_onboarding_status
from app.crud.creator import (
    create_creator_profile,
    get_creator_profile_by_user_id,
    get_creator_profile_by_id,
    get_creator_profile_by_handle,
    update_creator_profile,
    get_public_creator_profiles
)

router = APIRouter(prefix="/creator/profile", tags=["Creator Profile"])

@router.post("/onboarding", response_model=LoginResponse)
async def complete_creator_onboarding(
    profile_data: CreatorProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator)
):
    """
    Complete creator onboarding by creating profile.
    This endpoint is called after email verification to set up the creator's profile.
    Returns a new JWT token with updated onboarding status.
    """
    # Check if profile already exists
    existing_profile = get_creator_profile_by_user_id(db, str(current_user.id))
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Creator profile already exists. Use PUT /creator/profile to update."
        )
    
    # Check if handle is already taken
    existing_handle = get_creator_profile_by_handle(db, profile_data.handle)
    if existing_handle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Handle already taken. Please choose a different handle."
        )
    
    # Create profile and mark user as onboarded
    profile = create_creator_profile(db, str(current_user.id), profile_data)
    
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

@router.get("/me", response_model=CreatorProfileOut)
async def get_my_creator_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_creator)
):
    """
    Get the current creator's profile.
    Requires completed onboarding.
    """
    profile = get_creator_profile_by_user_id(db, str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator profile not found."
        )
    return profile

@router.put("/", response_model=CreatorProfileOut)
async def update_my_creator_profile(
    profile_data: CreatorProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_creator)
):
    """
    Update the current creator's profile.
    Only provided fields will be updated.
    """
    # Check handle uniqueness if being updated
    if profile_data.handle:
        existing_handle = get_creator_profile_by_handle(db, profile_data.handle)
        if existing_handle and str(existing_handle.user_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Handle already taken. Please choose a different handle."
            )
    
    profile = update_creator_profile(db, str(current_user.id), profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator profile not found."
        )
    return profile

@router.get("/{profile_id}", response_model=CreatorProfilePublic)
async def get_public_creator_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a public creator profile by ID.
    Only returns public profiles for discovery by brands.
    """
    profile = get_creator_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator profile not found."
        )
    
    if not profile.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This creator profile is private."
        )
    
    return profile

@router.get("/", response_model=List[CreatorProfilePublic])
async def discover_creators(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    location: Optional[str] = Query(None, description="Filter by location"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by")
):
    """
    Discover public creator profiles with filtering.
    Used by brands to find creators for campaigns.
    """
    # Parse tags if provided
    tag_list = tags.split(",") if tags else None
    
    profiles = get_public_creator_profiles(
        db=db,
        skip=skip,
        limit=limit,
        content_type=content_type,
        location=location,
        tags=tag_list
    )
    
    return profiles

@router.patch("/visibility", response_model=CreatorProfileOut)
async def update_profile_visibility(
    is_public: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_creator)
):
    """
    Update creator profile visibility.
    Allows creators to make their profile public or private.
    """
    profile_data = CreatorProfileUpdate(is_public=is_public)
    profile = update_creator_profile(db, str(current_user.id), profile_data)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator profile not found."
        )
    
    return profile