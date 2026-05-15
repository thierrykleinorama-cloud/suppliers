---
name: Chrome Debug setup for Playwright
description: Instructions to set up Chrome with remote debugging so Claude can control the user's real browser via Playwright CDP
type: reference
---

# Chrome Debug Setup (Playwright CDP)

## What this does
Creates a desktop shortcut that launches Chrome with remote debugging enabled, allowing Claude to connect via Playwright and control the real browser with all cookies/logins intact.

## Steps

### 1. Find Chrome profile directory name
Chrome profiles are named `Default`, `Profile 1`, `Profile 2`, etc. Find which one the user wants:
```python
# List profiles and their display names
import json, os
user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
for d in os.listdir(user_data):
    pref = os.path.join(user_data, d, "Preferences")
    if os.path.isfile(pref):
        name = json.load(open(pref, encoding='utf-8')).get('profile', {}).get('name', '?')
        print(f"{d} -> {name}")
```

### 2. Create junction (symlink) to Chrome User Data
Chrome blocks `--remote-debugging-port` on the default data directory. Workaround: create a Windows junction that points to the same directory but with a different path.
```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\ChromeDebug" -Target "$env:LOCALAPPDATA\Google\Chrome\User Data"
```

### 3. Create desktop shortcut
```powershell
# Save as create_shortcut.ps1 and run with: powershell -ExecutionPolicy Bypass -File create_shortcut.ps1
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Chrome Debug.lnk")
$Shortcut.TargetPath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$Shortcut.Arguments = "--remote-debugging-port=9222 --user-data-dir=`"$env:USERPROFILE\ChromeDebug`" `"--profile-directory=PROFILE_NAME`""
$Shortcut.Description = "Chrome with Playwright debugging"
$Shortcut.Save()
```
Replace `PROFILE_NAME` with the actual profile directory name (e.g., `Profile 6`, `Default`).

### 4. Usage
- Close ALL Chrome windows and processes
- Double-click "Chrome Debug" on desktop
- Chrome opens normally with all cookies — plus port 9222 is open for Playwright

### 5. Connect from Playwright
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    context = browser.contexts[0]
    # Now you have full access to the user's real browser
```

### 6. Verify
```bash
curl -s http://127.0.0.1:9222/json/version
```
Should return JSON with Chrome version info.

## Notes
- The junction (`ChromeDebug`) is permanent — no need to recreate it
- The shortcut is session-only: no Chrome config is changed. Normal Chrome launch works as before
- If Chrome won't connect, it's usually because old Chrome processes are still running. Kill them all first.
- On Thierry's main machine: Profile 6 = "Thierry" personal profile
