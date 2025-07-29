"""CRUD functions for User model."""
import datetime 
from sqlalchemy.orm import Session
from app.auth.models import User as UserModel, RefreshToken
from app.auth.schemas import UserCreate

def get_user(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def create_user(db: Session, user: UserCreate):
    from app.core.security import get_password_hash
    db_user = UserModel(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_superuser(db: Session, name: str, email: str, password :str):
    from app.core.security import get_password_hash
    db_user = UserModel(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        is_admin=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_refresh_token(db: Session, user_id: str, token: str, expires_at: datetime) -> RefreshToken:
    """Create and persist a new refresh token."""
    db_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_refresh_token(db: Session, token: str) -> RefreshToken:
    """Retrieve a refresh token by its token string."""
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()

def revoke_refresh_token(db: Session, db_token: RefreshToken) -> None:
    """Mark a refresh token as revoked."""
    db_token.revoked = True
    db.add(db_token)
    db.commit()