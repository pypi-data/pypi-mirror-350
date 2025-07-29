"""Dependencies for API routes."""
from typing import Generator
from functools import wraps

from sqlalchemy.orm import Session
from fastapi import WebSocket, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.core.db.session import SessionLocal
from app.core.security import verify_token
from app.auth.crud import get_user

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 

# OAuth2 scheme for access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, credentials_exception, token_type="access")
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user


async def authenticate_websocket(websocket: WebSocket) -> any:
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        raise HTTPException(status_code=403, detail="Missing token")

    try:
        db: Session = next(get_db())
        payload = verify_token(token, HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        ), token_type="access")

        user_id: str = payload.get("sub")
        if user_id is None:
            await websocket.close(code=1008)
            raise HTTPException(status_code=403, detail="Invalid user ID in token")

        user = get_user(db, user_id)
        if user is None:
            await websocket.close(code=1008)
            raise HTTPException(status_code=403, detail="User not found")

        return user

    except Exception as e:
        await websocket.close(code=1008)
        raise e