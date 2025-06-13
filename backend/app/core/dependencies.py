from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.user import User, UserRole

def require_creator(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure the current user has creator role.
    Raises 403 if user is not a creator.
    """
    if current_user.role != UserRole.CREATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Creator role required."
        )
    return current_user

def require_brand(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure the current user has brand role.
    Raises 403 if user is not a brand.
    """
    if current_user.role != UserRole.BRAND:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Brand role required."
        )
    return current_user

def require_agency(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure the current user has agency role.
    Raises 403 if user is not an agency.
    """
    if current_user.role != UserRole.AGENCY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Agency role required."
        )
    return current_user

def require_onboarded_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure the current user has completed onboarding.
    Raises 403 if user hasn't completed onboarding.
    """
    if not current_user.has_completed_onboarding:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please complete your profile onboarding first."
        )
    return current_user

def require_onboarded_creator(current_user: User = Depends(require_creator)) -> User:
    """Combined dependency for onboarded creator"""
    if not current_user.has_completed_onboarding:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please complete your creator profile onboarding first."
        )
    return current_user

def require_onboarded_brand(current_user: User = Depends(require_brand)) -> User:
    """Combined dependency for onboarded brand"""
    if not current_user.has_completed_onboarding:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please complete your brand profile onboarding first."
        )
    return current_user

def require_onboarded_agency(current_user: User = Depends(require_agency)) -> User:
    """Combined dependency for onboarded agency"""
    if not current_user.has_completed_onboarding:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please complete your agency profile onboarding first."
        )
    return current_user