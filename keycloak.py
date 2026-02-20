import streamlit as st
import httpx
import os
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlencode


# --- Keycloak Config ---
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "myrealm")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "streamlit-app")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

# OIDC Endpoints
OIDC_BASE = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect"
AUTH_URL = f"{OIDC_BASE}/auth"
TOKEN_URL = f"{OIDC_BASE}/token"
USERINFO_URL = f"{OIDC_BASE}/userinfo"
LOGOUT_URL = f"{OIDC_BASE}/logout"


def get_login_url() -> str:
    """Build Keycloak authorization URL for Authorization Code Flow."""
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = secrets.token_urlsafe(32)

    params = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": REDIRECT_URI,
        "state": st.session_state.oauth_state,
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict | None:
    """Exchange authorization code for access token via Keycloak token endpoint."""
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": KEYCLOAK_CLIENT_ID,
    }
    if KEYCLOAK_CLIENT_SECRET:
        data["client_secret"] = KEYCLOAK_CLIENT_SECRET

    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(TOKEN_URL, data=data)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        st.error(f"❌ Token exchange failed: {e.response.status_code} — {e.response.text}")
        return None
    except httpx.RequestError as e:
        st.error(f"❌ Cannot reach Keycloak: {e}")
        return None


def fetch_userinfo(access_token: str) -> dict | None:
    """Fetch user info from Keycloak userinfo endpoint."""
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(
                USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            resp.raise_for_status()
            return resp.json()
    except (httpx.HTTPStatusError, httpx.RequestError):
        return None


def refresh_access_token(refresh_token: str) -> dict | None:
    """Use refresh token to get a new access token."""
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": KEYCLOAK_CLIENT_ID,
    }
    if KEYCLOAK_CLIENT_SECRET:
        data["client_secret"] = KEYCLOAK_CLIENT_SECRET

    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(TOKEN_URL, data=data)
            resp.raise_for_status()
            return resp.json()
    except (httpx.HTTPStatusError, httpx.RequestError):
        return None


def handle_auth_callback() -> bool:
    """Handle the OAuth2 callback — extract code from query params and exchange for token."""
    query_params = st.query_params
    code = query_params.get("code")
    state = query_params.get("state")

    if code:
        token_data = exchange_code_for_token(code)
        if token_data:
            st.session_state.access_token = token_data["access_token"]
            st.session_state.refresh_token = token_data.get("refresh_token")
            st.session_state.token_expiry = datetime.now() + timedelta(
                seconds=token_data.get("expires_in", 300)
            )

            user_info = fetch_userinfo(token_data["access_token"])
            if user_info:
                st.session_state.user_info = user_info
                st.session_state.authenticated = True

            st.query_params.clear()
            return True
    return False


def ensure_valid_token() -> bool:
    """Check if access token is expired and refresh if needed."""
    if "token_expiry" in st.session_state:
        if datetime.now() >= st.session_state.token_expiry:
            if "refresh_token" in st.session_state:
                token_data = refresh_access_token(st.session_state.refresh_token)
                if token_data:
                    st.session_state.access_token = token_data["access_token"]
                    st.session_state.refresh_token = token_data.get("refresh_token")
                    st.session_state.token_expiry = datetime.now() + timedelta(
                        seconds=token_data.get("expires_in", 300)
                    )
                    return True
            logout()
            return False
    return True


def logout():
    """Clear session state."""
    for key in ["access_token", "refresh_token", "token_expiry", "user_info", "authenticated", "oauth_state"]:
        st.session_state.pop(key, None)


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)
