import streamlit as st
import os
from dotenv import load_dotenv

from dashboard import render_dashboard

# Load .env file
load_dotenv()

# --- Auth toggle ---
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"

if AUTH_ENABLED:
    from keycloak import (
        get_login_url,
        handle_auth_callback,
        ensure_valid_token,
        is_authenticated,
        logout,
    )

# --- Page Config ---
st.set_page_config(
    page_title="📊 Dashboard Sample",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    if not AUTH_ENABLED:
        render_dashboard()
        return

    # Already authenticated
    if is_authenticated():
        if ensure_valid_token():
            render_dashboard(st.session_state.user_info, logout_fn=logout)
        else:
            st.link_button("� Login with Keycloak", get_login_url(), width="stretch")
        return

    # Handle OAuth callback
    if handle_auth_callback():
        st.rerun()
        return

    # Not authenticated — show login button
    st.title("📊 Dashboard Sample")
    st.info("Please login to access the dashboard.")
    st.link_button("🔑 Login with Keycloak", get_login_url(), width="stretch")


if __name__ == "__main__":
    main()
