import pytest
from fastapi import HTTPException

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
import time

def test_password_hash_and_verify():
    password = "supersecret"
    hashed = get_password_hash(password)
    assert hashed != password
    # Correct password verifies
    assert verify_password(password, hashed)
    # Incorrect password fails
    assert not verify_password("wrongpass", hashed)

def test_create_and_verify_access_token():
    data = {"sub": "user123"}
    token, expiry = create_access_token(data)
    # verify_token should decode correctly
    payload = verify_token(token, HTTPException(status_code=401), token_type="access")
    assert payload.get("sub") == "user123"
    assert payload.get("type") == "access"
    # Wrong token type should raise
    with pytest.raises(HTTPException):
        verify_token(token, HTTPException(status_code=401), token_type="refresh")

def test_create_and_verify_refresh_token():
    data = {"sub": "user456"}
    token = create_refresh_token(data)
    # verify_token should decode correctly
    payload = verify_token(token, HTTPException(status_code=401), token_type="refresh")
    assert payload.get("sub") == "user456"
    assert payload.get("type") == "refresh"

def test_verify_token_invalid_raises():
    bad_token = "not.a.valid.token"
    exc = HTTPException(status_code=401)
    with pytest.raises(HTTPException):
        verify_token(bad_token, exc, token_type="access")