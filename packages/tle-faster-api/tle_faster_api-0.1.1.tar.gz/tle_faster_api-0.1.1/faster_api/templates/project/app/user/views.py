"""User endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import deps
from .schemas import (User as UserSchema, Preferences, PreferencesCreate, Profile, ProfileCreate)
from .crud import get_preferences, update_preferences, get_profile, update_profile

router = APIRouter()

@router.get("/", response_model=UserSchema)
def my_account(current_user=Depends(deps.get_current_user)):
    """Get current authenticated user."""
    return current_user

# User Preferences
@router.get("/preferences", response_model=Preferences)
def read_preferences(db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    db_prefs = get_preferences(db, user_id=current_user.id)
    if not db_prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return db_prefs

@router.patch("/preferences", response_model=Preferences)
def update_preferences(prefs_in: PreferencesCreate, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    db_prefs = update_preferences(db, user_id=current_user.id, updates=prefs_in.model_dump(exclude_unset=True))
    if not db_prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return db_prefs

# User Profile
@router.get("/profile", response_model=Profile)
def read_profile(db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    db_profile = get_profile(db, user_id=current_user.id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.patch("/profile", response_model=Profile)
def update_profile(profile_in: ProfileCreate, db: Session = Depends(deps.get_db), current_user=Depends(deps.get_current_user)):
    db_profile = update_profile(db, user_id=current_user.id, updates=profile_in.model_dump(exclude_unset=True))
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile
