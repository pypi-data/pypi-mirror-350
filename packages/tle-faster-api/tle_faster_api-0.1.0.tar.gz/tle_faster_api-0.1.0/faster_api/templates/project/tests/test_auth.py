import pytest

def test_register_user(client, new_user_data):
    # Register a new user
    response = client.post(
        "/api/v1/auth/join", json=new_user_data
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == new_user_data["email"]
    assert data["name"] == new_user_data["name"]

def test_register_existing_email(client, new_user_data):
    # Attempt to register same email twice
    client.post("/api/v1/auth/join", json=new_user_data)
    response = client.post("/api/v1/auth/join", json=new_user_data)
    assert response.status_code == 400

def test_login_and_refresh_flow(client, new_user_data, monkeypatch):
    """Register, log in, and refresh tokens with patched datetime to avoid tz issues."""
    # Monkey-patch datetime.now in auth.views to return a naive fixed datetime
    import datetime as _dt
    from app.auth import views as auth_views
    class DummyDateTime(_dt.datetime):
        @classmethod
        def now(cls, tz=None):
            # ignore tz to ensure naive datetime
            return _dt.datetime(2020, 1, 1)
    monkeypatch.setattr(auth_views, "datetime", DummyDateTime)
    # Register and then log in
    client.post("/api/v1/auth/join", json=new_user_data)
    login_resp = client.post(
        "/api/v1/auth/login",
        data={
            "username": new_user_data["email"],
            "password": new_user_data["password"],
        },
    )
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert token_data.get("token_type") == "bearer"
    # Refresh token should be set as an HttpOnly cookie
    assert "refresh_token" in login_resp.cookies

    # Use the refresh endpoint to get a new access token
    refresh_resp = client.post("/api/v1/auth/refresh")
    assert refresh_resp.status_code == 200
    new_token_data = refresh_resp.json()
    assert "access_token" in new_token_data
    assert new_token_data.get("token_type") == "bearer"