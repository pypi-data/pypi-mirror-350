"""Models for <<APP_NAME>>."""
from sqlalchemy.sql import func
from sqlalchemy import Column 
import uuid 

# Import Base declarative class
from app.core.db.base import Base

# TODO: Define your models below.
# Example:
# from sqlalchemy import String, DateTime
# class MyModel(Base):
#     __tablename__ = "my_model"
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())