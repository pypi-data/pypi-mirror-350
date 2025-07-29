
"""Pydantic schemas for Preferences."""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.auth.schemas import User, UserBase, UserCreate

class PreferencesBase(BaseModel):
    pass

class PreferencesCreate(PreferencesBase):
    pass

class Preferences(PreferencesBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    timezone: Optional[str] = None
    locale: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True