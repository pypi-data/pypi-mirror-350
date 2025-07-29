

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid 

from app.core.db.base import Base
from app.auth.models import User # Allows import from app.models.user 

class Profile(Base):
    __tablename__ = "user_profiles"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), primary_key=True, index=True)
    timezone = Column(String, nullable=True)
    locale = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Preferences(Base):
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

