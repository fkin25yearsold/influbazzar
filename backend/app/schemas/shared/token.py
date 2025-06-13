from pydantic import BaseModel
from app.schemas.shared.user import UserProfile

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str
    role: str
    has_completed_onboarding: bool

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile