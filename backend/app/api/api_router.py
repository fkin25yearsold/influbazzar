from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.creator.profile import router as creator_profile_router
from app.api.brand.profile import router as brand_profile_router
from app.api.agency.profile import router as agency_profile_router

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include profile management routes
api_router.include_router(creator_profile_router, tags=["Creator Profile"])
api_router.include_router(brand_profile_router, tags=["Brand Profile"])
api_router.include_router(agency_profile_router, tags=["Agency Profile"])