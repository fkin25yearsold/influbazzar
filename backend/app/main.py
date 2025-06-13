from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.creator.profile import router as creator_profile_router
from app.api.brand.profile import router as brand_profile_router
from app.api.agency.profile import router as agency_profile_router
from app.db.base import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Influbazzar API",
    description="""
    Interactive influencer collaboration marketplace API
    
    ## Features
    
    * **Multi-role Authentication** - Support for creators, brands, and agencies
    * **Profile Management** - Complete onboarding and profile management for all user types
    * **Discovery System** - Find creators, brands, and agencies with advanced filtering
    * **JWT Security** - Secure authentication with role-based access control
    
    ## User Types
    
    * **Creators** - Influencers who apply to campaigns and earn money
    * **Brands** - Businesses who run influencer campaigns
    * **Agencies** - Firms that manage multiple creators and/or brands
    
    ## Getting Started
    
    1. Sign up with your role (creator/brand/agency)
    2. Verify your email with OTP
    3. Complete your profile onboarding
    4. Start discovering and connecting!
    """,
    version="1.0.0",
    contact={
        "name": "Influbazzar API Support",
        "email": "support@influbazzar.com",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth")
app.include_router(creator_profile_router, prefix="/api")
app.include_router(brand_profile_router, prefix="/api")
app.include_router(agency_profile_router, prefix="/api")

@app.get("/")
async def root():
    """
    Welcome endpoint with API information
    """
    return {
        "message": "Welcome to Influbazzar API",
        "description": "Interactive influencer collaboration marketplace",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "features": [
            "Multi-role authentication (Creator/Brand/Agency)",
            "Profile management and onboarding",
            "Discovery and search functionality",
            "JWT-based security",
            "Role-based access control"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Influbazzar API",
        "version": "1.0.0"
    }

@app.get("/api/version")
async def api_version():
    """API version endpoint for auto-refresh functionality"""
    return {
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }