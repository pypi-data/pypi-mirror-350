"""Pydantic schemas for <<APP_NAME>>."""
from pydantic import BaseModel

class ExampleSchema(BaseModel): 
    result: str
    signed_in_as: str 