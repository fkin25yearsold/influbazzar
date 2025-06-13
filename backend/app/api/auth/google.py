from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import requests
from app.db.session import get_db
from app.db.models.user import User, UserRole
from app.schemas.shared.otp import GoogleOAuthRequest
from app.schemas.shared.token import LoginResponse
from app.schemas.shared.user import UserProfile
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/google", response_model=LoginResponse)
async def google_auth(google_data: GoogleOAuthRequest, db: Session = Depends(get_db)):
    """Authenticate or register user with Google OAuth."""
    
    # Verify Google ID token
    user_info = await verify_google_token(google_data.id_token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Google token"
        )
    
    email = user_info.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not provided by Google"
        )
    
    # Validate role
    try:
        role = UserRole(google_data.role)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be creator, brand, or agency"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Existing user - login
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User exists with different role: {user.role.value}"
            )
        
        # Update Google authentication status
        user.is_google_authenticated = True
        user.is_verified = True
        
    else:
        # New user - register
        user = User(
            email=email,
            role=role,
            is_verified=True,
            is_google_authenticated=True,
            has_completed_onboarding=False
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    
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

async def verify_google_token(id_token: str) -> dict:
    """Verify Google ID token and return user info."""
    try:
        # In production, use Google's token verification endpoint
        # For now, we'll mock this functionality
        
        # Mock Google user info (replace with actual verification)
        mock_user_info = {
            "email": "user@example.com",
            "name": "Test User",
            "picture": "https://example.com/avatar.jpg"
        }
        
        # In production, use this:
        # response = requests.get(
        #     f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        # )
        # if response.status_code == 200:
        #     return response.json()
        
        return mock_user_info
        
    except Exception:
        return None