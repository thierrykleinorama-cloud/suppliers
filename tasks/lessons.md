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

## Lesson — supabase-py 2.28+ ClientOptions: use the package-level import only
**Rule**: Always `from supabase import ClientOptions`, never `from supabase.lib.client_options import ClientOptions`. In supabase-py 2.28+, the package init monkey-patches the re-exported `ClientOptions` so instances carry `storage` and `httpx_client` attributes — which `Client._init_supabase_auth_client` reads. The raw class from `supabase.lib.client_options` has no such fields and triggers `AttributeError: 'ClientOptions' object has no attribute 'storage'` on `create_client(..., options=ClientOptions(...))`. Verified 2026-05-16: suppliers' `src/database.py` uses the safe import and works on 2.28.0. A sibling project (hotelPandL) hit the raw-import path and needed a class-attribute fallback workaround.

## Lesson — Streamlit Cloud secrets: APP_URL must NOT live under a TOML section
**Rule**: In Streamlit Cloud → Settings → Secrets, any key placed below a `[section]` header (e.g. `[gcp_service_account]`) becomes a sub-key of that section. `st.secrets.get("APP_URL")` then returns `None`, the auth code falls back to `localhost`, and Google OAuth fails in production with no visible error. Put `APP_URL` on the first line of the secrets editor, above any section headers.

## Lesson — Local OAuth port must match the actual Streamlit port
**Rule**: `.env`'s `APP_URL=http://localhost:<port>` must match the port `streamlit run` actually binds. If a stale Streamlit process holds the expected port and the new one falls back to another, OAuth redirects land at the wrong process and surface as cryptic "code challenge does not match" errors. Kill the stale process (don't just switch ports), then restart.

## Lesson — Avast IDP.HELU.PSD11 false-flags Chrome + CDP automation
**Rule**: Driving debug Chrome (launched with `--remote-debugging-port=9222`) via Playwright triggers Avast's IDP behavioral engine — "IDP.HELU.PSD11" alert — and blocks the process mid-session. Avast pattern-matches "browser launched with remote debugging + external automation hammering it via CDP" as info-stealer behavior; it doesn't care that the binary is unmodified Chrome.exe. Fix: add Avast exceptions for `chrome.exe`, the `DebugProfile` directory, AND the `python.exe` driving Playwright. Same Avast environment that requires `pip-system-certs` for HTTPS — this machine has multiple AV-vs-dev frictions.

## Lesson — chrome_debug_setup.md junction approach can break DPAPI on Chrome 148+
**Rule**: The `tasks/chrome_debug_setup.md` junction procedure (junction `%USERPROFILE%\ChromeDebug` → real `User Data` dir + launch with real `--profile-directory`) was VERIFIED 2026-05-17 to corrupt the user's Profile 2 on Chrome 148.x — lost avatar, full Google account name, and all session cookies, same failure mode as the older `subst` incident. The doc may have worked on an older Chrome / different machine, but Chrome's `os_crypt` now regenerates encryption keys aggressively when it detects path inconsistency. Before using the junction shortcut, verify on a throwaway profile-directory FIRST. Safer fallback: use a brand-new isolated `--user-data-dir` like `DebugProfile` (no aliasing), accept the trade-off of having to re-sign into sites once.
