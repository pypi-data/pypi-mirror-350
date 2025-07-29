"""Endpoints for <<APP_NAME>>"""
from fastapi import APIRouter, Depends
from app.core import deps
from .schemas import ExampleSchema 

router = APIRouter()

@router.get("/", response_model=ExampleSchema)
def example(current_user=Depends(deps.get_current_user)):
    """Example endpoint for <<APP_NAME>>."""
    return {"result": "success", "signed_in_as": current_user.email}