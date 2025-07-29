"""User endpoints."""
from typing import List
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import deps
from app.core.config import settings
from .crud import (
    create_user,
    get_user_by_email,
    create_refresh_token as create_refresh_token_db,
    get_refresh_token as get_refresh_token_db,
    revoke_refresh_token as revoke_refresh_token_db,
)
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from .schemas import (
    UserCreate, 
    Token, 
    User as UserSchema
)

from app.user.crud import create_preferences, create_profile

router = APIRouter()


@router.post("/join", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_new_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):

    existing = get_user_by_email(db, email=user_in.email)

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user=user_in)

    create_profile(db, {"user_id": new_user.id})
    create_preferences(db, {"user_id": new_user.id})

    return new_user


@router.post("/login", response_model=Token)
def request_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Authenticate user and issue access & refresh tokens."""
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token, access_token_expires = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})

    # Calculate cookie expiration in seconds
    max_age = settings.refresh_token_expire_days * 24 * 3600

    # Persist the refresh token in the database along with expiry details
    expires_at = datetime.now(timezone.utc) + \
        timedelta(days=settings.refresh_token_expire_days)
    create_refresh_token_db(db, user.id, refresh_token, expires_at)

    # Set the refresh token as an HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=max_age,
        secure=False,  # Support HTTP and HTTPS
        samesite="lax",
    )

    # Return only the access token in the response body
    return {"access_token": access_token, "expiry": round(access_token_expires.timestamp()), "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(deps.get_db),
):
    """Refresh access token using a valid refresh token from an HttpOnly cookie."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Retrieve the refresh token from the cookie
    refresh_token_cookie = request.cookies.get("refresh_token")
    if not refresh_token_cookie:
        raise credentials_exception

    # Verify the token signature and type
    payload = verify_token(refresh_token_cookie,
                           credentials_exception, token_type="refresh")

    # Check refresh token existence and validity in the database.
    # Use datetime.now(timezone.utc) to ensure a timezone-aware datetime for comparison.
    if (
        not (token_in_db := get_refresh_token_db(db, refresh_token_cookie))
        or token_in_db.revoked
        or token_in_db.expires_at < datetime.now(timezone.utc)
    ):
        raise credentials_exception

    # Revoke the old refresh token in the database
    revoke_refresh_token_db(db, token_in_db)

    # Issue new tokens
    user_id = payload.get("sub")
    access_token, access_token_expires = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})
    expires_at = datetime.now(timezone.utc) + \
        timedelta(days=settings.refresh_token_expire_days)
    create_refresh_token_db(db, user_id, new_refresh_token, expires_at)

    # Calculate cookie expiration in seconds
    max_age = settings.refresh_token_expire_days * 24 * 3600

    # Set the new refresh token as an HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=max_age,
        secure=False,       # Set secure=True if you are serving over HTTPS
        samesite="lax",    # Adjust samesite as needed ("lax" or "strict")
    )

    # Return only the access token and token type in the response body
    return {"access_token": access_token, "expiry": round(access_token_expires.timestamp()), "token_type": "bearer"}