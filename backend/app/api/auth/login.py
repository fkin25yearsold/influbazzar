from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User, UserRole
from app.schemas.shared.user import UserLogin
from app.schemas.shared.token import LoginResponse
from app.schemas.shared.user import UserProfile
from app.core.security import create_access_token
from app.utils.hash import verify_password

router = APIRouter()

@router.post("/creator/login", response_model=LoginResponse)
async def creator_login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login for creators."""
    return await _login_user(login_data, UserRole.CREATOR, db)

@router.post("/brand/login", response_model=LoginResponse)
async def brand_login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login for brands."""
    return await _login_user(login_data, UserRole.BRAND, db)

@router.post("/agency/login", response_model=LoginResponse)
async def agency_login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login for agencies."""
    return await _login_user(login_data, UserRole.AGENCY, db)

async def _login_user(login_data: UserLogin, expected_role: UserRole, db: Session):
    """Common login logic for all user types."""
    
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check role
    if user.role != expected_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid credentials for {expected_role.value} login"
        )
    
    # Check if user is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email before logging in"
        )
    
    # Verify password (skip for Google users)
    if not user.is_google_authenticated:
        if not user.hashed_password or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    
    # Generate JWT token
    token_data = {
        "sub": str(user.id),
        "role": user.role.value,
        "has_completed_onboarding": user.has_completed_onboarding
    }
    access_token = create_access_token(data=token_data)
    
    return LoginResponse(
        access_token=access_token,
        user=UserProfile(
            id=str(user.id),
            email=user.email,
            role=user.role,
            has_completed_onboarding=user.has_completed_onboarding
        )
    )