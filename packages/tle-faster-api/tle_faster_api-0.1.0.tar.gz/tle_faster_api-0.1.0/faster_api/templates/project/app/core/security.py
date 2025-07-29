from passlib.context import CryptContext
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# static pepper for password hashing
_PEPPER = settings.password_pepper

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__type="ID",
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # include pepper when verifying
    return pwd_context.verify(plain_password + _PEPPER, hashed_password)

def get_password_hash(password: str) -> str:
    # include pepper when hashing
    return pwd_context.hash(password + _PEPPER)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return (encoded_jwt, expire)

def create_refresh_token(data: dict) -> str:
    """Create a new JWT refresh token with a unique identifier."""
    to_encode = data.copy()
    # include a unique JWT ID to ensure tokens differ even with same payload
    import uuid
    jti = str(uuid.uuid4())
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh", "jti": jti})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception, token_type: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != token_type:
            raise JWTError()
        return payload
    except JWTError:
        raise credentials_exception