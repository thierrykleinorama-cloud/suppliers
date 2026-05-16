"""
Test Google OAuth flow end-to-end via Playwright CDP.
Requires: Chrome Debug running (see tasks/chrome_debug_setup.md)

Usage:
    python tasks/test_oauth.py [URL]
    python tasks/test_oauth.py http://localhost:8502
    python tasks/test_oauth.py https://coinmiaousuppliers.streamlit.app
"""
import sys
import time
from playwright.sync_api import sync_playwright


def get_oauth_url(page) -> str | None:
    """Extract the Google OAuth URL from Streamlit page (handles iframes)."""
    # Streamlit renders link_button inside iframes — search all frames
    for frame in page.frames:
        link = frame.locator("a[href*='supabase.co/auth']")
        if link.count() > 0:
            return link.first.get_attribute("href")
    return None


def test_oauth(app_url: str = "http://localhost:8502"):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()

        # Step 1: Load login page
        print(f"1. Loading {app_url}...")
        page.goto(app_url, wait_until="networkidle", timeout=20000)
        print(f"   Title: {page.title()}")

        # Step 2: Extract Google OAuth URL from iframes
        print("2. Looking for Google sign-in link...")
        oauth_url = get_oauth_url(page)
        if not oauth_url:
            print("   ERROR: Google OAuth link not found")
            page.screenshot(path="test_outputs/oauth_error.png")
            return False

        print(f"   Found OAuth URL")

        # Step 3: Navigate to Google
        print("3. Navigating to Google sign-in...")
        page.goto(oauth_url, wait_until="networkidle", timeout=30000)

        if "accounts.google.com" in page.url:
            # List available accounts
            accounts = page.locator("[data-email]")
            count = accounts.count()
            print(f"   Google account picker: {count} account(s)")
            for i in range(count):
                print(f"     - {accounts.nth(i).get_attribute('data-email')}")

            # Click first account
            if count > 0:
                email = accounts.first.get_attribute("data-email")
                print(f"4. Clicking {email}...")
                accounts.first.click()

                # Wait for redirect back to app
                try:
                    page.wait_for_url(f"**{app_url.split('//')[1].split('/')[0]}**", timeout=30000)
                    time.sleep(3)
                    print(f"   Redirected to: {page.url[:80]}")
                except Exception:
                    print(f"   Redirect timeout. URL: {page.url[:80]}")
                    page.screenshot(path="test_outputs/oauth_redirect_timeout.png")
                    return False

        # Step 5: Verify logged in
        body = page.inner_text("body")
        if "Logged in" in body or "Logout" in body:
            print("5. SUCCESS: Logged in!")
            page.screenshot(path="test_outputs/oauth_success.png")
            return True
        elif "OAuth login failed" in body or "OAuth session expired" in body:
            print(f"5. FAILED: {body[:200]}")
            page.screenshot(path="test_outputs/oauth_failed.png")
            return False
        else:
            print(f"5. UNCLEAR. Page: {body[:200]}")
            page.screenshot(path="test_outputs/oauth_unclear.png")
            return False


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8502"
    test_oauth(url)
