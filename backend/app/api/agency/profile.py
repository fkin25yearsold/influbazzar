from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.dependencies import require_agency, require_onboarded_agency
from app.db.models.user import User
from app.schemas.agency.profile import (
    AgencyProfileCreate, 
    AgencyProfileUpdate, 
    AgencyProfileOut,
    AgencyProfilePublic
)
from app.schemas.shared.token import LoginResponse
from app.schemas.shared.user import UserProfile
from app.core.security import create_token_with_onboarding_status
from app.crud.agency import (
    create_agency_profile,
    get_agency_profile_by_user_id,
    get_agency_profile_by_id,
    update_agency_profile,
    get_public_agency_profiles,
    get_agency_dashboard_stats
)

router = APIRouter(prefix="/agency/profile", tags=["Agency Profile"])

@router.post("/onboarding", response_model=LoginResponse)
async def complete_agency_onboarding(
    profile_data: AgencyProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_agency)
):
    """
    Complete agency onboarding by creating profile.
    This endpoint is called after email verification to set up the agency's profile.
    Returns a new JWT token with updated onboarding status.
    """
    # Check if profile already exists
    existing_profile = get_agency_profile_by_user_id(db, str(current_user.id))
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agency profile already exists. Use PUT /agency/profile to update."
        )
    
    # Create profile and mark user as onboarded
    profile = create_agency_profile(db, str(current_user.id), profile_data)
    
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

@router.get("/me", response_model=AgencyProfileOut)
async def get_my_agency_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_agency)
):
    """
    Get the current agency's profile.
    Requires completed onboarding.
    """
    profile = get_agency_profile_by_user_id(db, str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency profile not found."
        )
    return profile

@router.put("/", response_model=AgencyProfileOut)
async def update_my_agency_profile(
    profile_data: AgencyProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_agency)
):
    """
    Update the current agency's profile.
    Only provided fields will be updated.
    """
    profile = update_agency_profile(db, str(current_user.id), profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency profile not found."
        )
    return profile

@router.get("/{profile_id}", response_model=AgencyProfilePublic)
async def get_public_agency_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a public agency profile by ID.
    Used by brands and creators to view agency information.
    """
    profile = get_agency_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency profile not found."
        )
    
    return profile

@router.get("/", response_model=List[AgencyProfilePublic])
async def discover_agencies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
    agency_type: Optional[str] = Query(None, description="Filter by agency type"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    location: Optional[str] = Query(None, description="Filter by location")
):
    """
    Discover agency profiles with filtering.
    Used by brands and creators to find agency partners.
    """
    profiles = get_public_agency_profiles(
        db=db,
        skip=skip,
        limit=limit,
        agency_type=agency_type,
        industry=industry,
        location=location
    )
    
    return profiles

@router.get("/me/dashboard", response_model=dict)
async def get_agency_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_onboarded_agency)
):
    """
    Get agency dashboard statistics.
    Returns key metrics for the agency dashboard UI.
    """
    stats = get_agency_dashboard_stats(db, str(current_user.id))
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency profile not found."
        )
    
    return {
        "dashboard_stats": stats,
        "message": "Agency dashboard data retrieved successfully"
    }