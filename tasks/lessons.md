# Suppliers — Lessons Learned

## Lesson — Supabase PostgREST can't run DDL
**Rule**: Cannot CREATE TABLE via the PostgREST API (supabase-py client). Must use Management API with SUPABASE_ACCESS_TOKEN or paste SQL directly in Supabase Dashboard SQL Editor.

## Lesson — Same Supabase project across hotel apps
**Rule**: InstaHotel, hotelPandL, and Suppliers all share the same Supabase project (lngrockgpnwaizzyvwsk). Same SUPABASE_URL and SUPABASE_KEY. Copy from any sibling project's .env.

## Lesson — Streamlit + OAuth PKCE: code_verifier must be cached
**Rule**: Streamlit reruns the entire script on every interaction, which calls `sign_in_with_oauth()` repeatedly, generating new code_verifier/code_challenge pairs. By the time the user returns from Google, the stored code_verifier no longer matches the code_challenge in the URL they clicked. Fix: generate OAuth URL + code_verifier ONCE using `st.cache_resource` and reuse until consumed.

## Lesson — Streamlit config.toml requires correct working directory
**Rule**: Streamlit reads `.streamlit/config.toml` relative to the working directory, NOT relative to the app file. Run `streamlit run app/main.py` from the project root (where `.streamlit/` lives), not from a parent directory.

## Lesson — Supabase Site URL controls OAuth fallback redirect
**Rule**: If the `redirect_to` in an OAuth URL doesn't match the Supabase Redirect URLs allowlist, Supabase silently falls back to the **Site URL** setting. Always ensure both Site URL and Redirect URLs are configured correctly in Supabase Auth > URL Configuration.
