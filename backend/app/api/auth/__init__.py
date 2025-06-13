from fastapi import APIRouter
from . import signup, otp, login, google

router = APIRouter()

# Include all auth routers
router.include_router(signup.router, tags=["Authentication - Signup"])
router.include_router(otp.router, tags=["Authentication - OTP"])
router.include_router(login.router, tags=["Authentication - Login"])
router.include_router(google.router, tags=["Authentication - Google"])

@router.post("/logout")
async def logout():
    """Logout endpoint - stateless, just tells frontend to clear token."""
    return {"message": "Successfully logged out. Please clear your access token."}