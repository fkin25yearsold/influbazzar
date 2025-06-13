from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User, UserRole
from app.db.models.otp import UserOTP
from app.schemas.shared.user import UserCreate
from app.schemas.shared.otp import OTPResponse
from app.utils.hash import hash_password
from app.utils.email import generate_otp, send_otp_email

router = APIRouter()

@router.post("/creator/signup", response_model=OTPResponse)
async def creator_signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Sign up a new creator and send OTP for verification."""
    return await _signup_user(user_data, UserRole.CREATOR, db)

@router.post("/brand/signup", response_model=OTPResponse)
async def brand_signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Sign up a new brand and send OTP for verification."""
    return await _signup_user(user_data, UserRole.BRAND, db)

@router.post("/agency/signup", response_model=OTPResponse)
async def agency_signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Sign up a new agency and send OTP for verification."""
    return await _signup_user(user_data, UserRole.AGENCY, db)

async def _signup_user(user_data: UserCreate, role: UserRole, db: Session):
    """Common signup logic for all user types."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        role=role,
        is_verified=False,
        has_completed_onboarding=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate and store OTP
    otp_code = generate_otp()
    otp = UserOTP.create_with_expiry(
        user_id=user.id,
        otp_code=otp_code,
        destination=user.email
    )
    
    db.add(otp)
    db.commit()
    
    # Send OTP email (mocked)
    send_otp_email(user.email, otp_code)
    
    return OTPResponse(
        message="OTP sent to your email. Please verify to complete registration.",
        email=user.email
    )