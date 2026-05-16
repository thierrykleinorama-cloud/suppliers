# Adding Auth to a Streamlit + Supabase Project

## Prerequisites
- Project already uses Supabase (same instance: `lngrockgpnwaizzyvwsk`)
- Google OAuth already configured in Supabase (done once, shared across all projects)
- `supabase` and `python-dotenv` in requirements.txt

## Steps

### 1. Copy the auth file
Copy `tasks/auth_template.py` from the suppliers repo into your project as `auth.py` (or `src/auth.py` — adapt the import accordingly).

### 2. Set APP_URL in .env
```
APP_URL=https://your-app-name.streamlit.app
```
For local dev, use `http://localhost:8501` (or whichever port you use).

### 3. Set APP_URL in Streamlit Cloud secrets
In Streamlit Cloud dashboard → your app → Settings → Secrets:
```toml
APP_URL = "https://your-app-name.streamlit.app"
```
If you DON'T set this, it defaults to `http://localhost:8502` and Google login won't work in production.

### 4. Add redirect URL in Supabase
Go to: https://supabase.com/dashboard/project/lngrockgpnwaizzyvwsk/auth/url-configuration

Add your production URL to the **Redirect URLs** list:
```
https://your-app-name.streamlit.app
```
Also add your local dev URL if not already there:
```
http://localhost:8501
```

### 5. Add to your main.py
Add these lines near the top, after `st.set_page_config()`:

```python
from auth import check_auth, handle_oauth_callback, login_form, logout

# Handle Google OAuth callback (must be before check_auth)
handle_oauth_callback()

# Auth gate
if not check_auth():
    login_form("Your App Name")
    st.stop()
```

Add a logout button in the sidebar:
```python
with st.sidebar:
    st.caption(f"Logged in as {st.session_state.get('auth_user_email', '')}")
    if st.button(":material/logout: Logout"):
        logout()
```

### 6. Ensure database.py uses PKCE
If your project has its own `database.py` with a Supabase client, make sure it uses PKCE:
```python
from supabase import create_client, ClientOptions
client = create_client(url, key, options=ClientOptions(flow_type="pkce"))
```
If you use the auth_template.py as-is, it creates its own client — no change needed.

### 7. Deploy
Push to main, verify on Streamlit Cloud.

## What users will see
1. Login page with "Sign in with Google" button + email/password form
2. Click Google → pick Google account → redirected back → logged in
3. Session persists on page refresh
4. Logout button in sidebar

## Shared across all projects
- Same Supabase project = same users
- Same Google OAuth credentials = same "Sign in with Google" experience
- Users created in one app can log in to all apps
