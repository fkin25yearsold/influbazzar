from pydantic import BaseModel, EmailStr

class OTPVerification(BaseModel):
    email: EmailStr
    otp_code: str

class OTPResponse(BaseModel):
    message: str
    email: str

class GoogleOAuthRequest(BaseModel):
    id_token: str
    role: str  # creator, brand, or agency