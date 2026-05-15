"""
Suppliers — Authentication (Supabase Auth)
Gate the app behind email/password login.
"""
import streamlit as st
from src.database import get_supabase


def check_auth() -> bool:
    """Return True if the user has a valid session."""
    access_token = st.session_state.get("auth_access_token")
    refresh_token = st.session_state.get("auth_refresh_token")

    if not access_token or not refresh_token:
        return False

    try:
        client = get_supabase()
        client.auth.set_session(access_token, refresh_token)
        session = client.auth.get_session()
        if session:
            # Update tokens in case they were refreshed
            st.session_state["auth_access_token"] = session.access_token
            st.session_state["auth_refresh_token"] = session.refresh_token
            return True
    except Exception:
        # Session invalid or expired beyond refresh — clear and require login
        _clear_auth_state()

    return False


def login_form():
    """Render a centered login form. Call st.stop() after this."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## :material/lock: Suppliers Directory")
        st.caption("Sign in to continue")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button(
                "Sign in", type="primary", use_container_width=True
            )

        if submitted:
            if not email or not password:
                st.error("Please enter email and password.")
                return

            try:
                client = get_supabase()
                response = client.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )
                st.session_state["auth_access_token"] = response.session.access_token
                st.session_state["auth_refresh_token"] = response.session.refresh_token
                st.session_state["auth_user_email"] = response.user.email
                st.rerun()
            except Exception as e:
                msg = str(e)
                if "Invalid login credentials" in msg:
                    st.error("Invalid email or password.")
                else:
                    st.error(f"Login failed: {msg}")

        # Forgot password
        if st.button("Forgot password?", key="forgot_pw"):
            st.session_state["show_reset"] = True

        if st.session_state.get("show_reset"):
            reset_email = st.text_input("Enter your email to receive a reset link", key="reset_email")
            if st.button("Send reset link", key="send_reset"):
                if not reset_email:
                    st.error("Please enter your email.")
                else:
                    try:
                        get_supabase().auth.reset_password_for_email(reset_email)
                        st.success("Reset link sent! Check your inbox.")
                        st.session_state["show_reset"] = False
                    except Exception as e:
                        st.error(f"Failed to send reset link: {e}")


def logout():
    """Sign out and clear session."""
    try:
        get_supabase().auth.sign_out()
    except Exception:
        pass
    _clear_auth_state()
    st.rerun()


def _clear_auth_state():
    """Remove auth keys from session state."""
    for key in ("auth_access_token", "auth_refresh_token", "auth_user_email"):
        st.session_state.pop(key, None)
