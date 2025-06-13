from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.otp import UserOTP
from app.schemas.shared.otp import OTPVerification
from app.schemas.shared.token import LoginResponse
from app.schemas.shared.user import UserProfile
from app.core.security import create_user_token  # Updated to use new helper function
from app.utils.email import send_welcome_email

router = APIRouter()

@router.post("/verify-otp", response_model=LoginResponse)
async def verify_otp(otp_data: OTPVerification, db: Session = Depends(get_db)):
    """Verify OTP and complete user registration with onboarding status."""
    
    # Find user by email
    user = db.query(User).filter(User.email == otp_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Find valid OTP
    otp = db.query(UserOTP).filter(
        UserOTP.user_id == user.id,
        UserOTP.otp_code == otp_data.otp_code,
        UserOTP.is_used == False,
        UserOTP.expires_at > datetime.utcnow()
    ).first()
    
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Mark OTP as used and verify user
    otp.is_used = True
    user.is_verified = True
    
    db.commit()
    db.refresh(user)
    
    # Send welcome email
    send_welcome_email(user.email, user.role.value)
    
    # Generate JWT token with onboarding status
    access_token = create_user_token(user)
    
    return LoginResponse(
        access_token=access_token,
        user=UserProfile(
            id=str(user.id),
            email=user.email,
            role=user.role,
            has_completed_onboarding=user.has_completed_onboarding
        )
    )