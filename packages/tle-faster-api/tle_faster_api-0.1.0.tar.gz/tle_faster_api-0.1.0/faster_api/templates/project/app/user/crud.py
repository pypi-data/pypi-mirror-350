
"""CRUD functions for User app."""
from sqlalchemy.orm import Session
from app.auth.crud import create_user, get_user, get_user_by_email
from .models import Preferences, Profile

def get_preferences(db: Session, user_id: str):
    return db.query(Preferences).filter(Preferences.user_id == user_id).first()

def create_preferences(db: Session, data: dict):
    """Create a new preferences entry. 'data' must include 'user_id' and any preferences fields."""
    db_prefs = Preferences(**data)
    db.add(db_prefs)
    db.commit()
    db.refresh(db_prefs)
    return db_prefs

def update_preferences(db: Session, user_id: str, updates: dict):
    db_prefs = get_preferences(db, user_id)
    if not db_prefs:
        return None
    for field, value in updates.items():
        setattr(db_prefs, field, value)
    db.commit()
    db.refresh(db_prefs)
    return db_prefs


def get_profile(db: Session, user_id: str):
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def create_profile(db: Session, data: dict):
    """Create a new profile entry. 'data' must include 'user_id' and any profile fields."""
    db_profile = Profile(**data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, user_id: str, updates: dict):
    db_profile = get_profile(db, user_id)
    if not db_profile:
        return None
    for field, value in updates.items():
        setattr(db_profile, field, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile
