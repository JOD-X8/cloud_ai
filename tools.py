import os
import subprocess
from browser import browser
from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================
# FIND BROWSER
# ==========================================

def find_browser(browser_name):

    browser_paths = {

        "chrome": [
            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
            ),
        ],

        "edge": [
            os.path.expandvars(
                r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
            ),
            os.path.expandvars(
                r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"
            ),
        ],

        "brave": [
            os.path.expandvars(
                r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
            os.path.expandvars(
                r"%LocalAppData%\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
        ],
    }


    for path in browser_paths.get(browser_name, []):

        if os.path.exists(path):
            return path


    return None


# ==========================================
# OPEN BROWSER
# ==========================================

def open_browser(url, browser=None):

    supported_browsers = [
        "chrome",
        "edge",
        "brave"
    ]


    # --------------------------------------
    # Specific browser requested
    # --------------------------------------

    if browser:

        browser = browser.lower()

        if browser not in supported_browsers:

            return (
                f"Unsupported browser: {browser}"
            )


        path = find_browser(browser)


        if not path:

            return (
                f"{browser.capitalize()} is not installed."
            )


        try:

            subprocess.Popen([
                path,
                url
            ])

            return (
                f"{browser.capitalize()} opened {url}."
            )

        except Exception as e:

            return (
                f"Failed to open {browser}: {e}"
            )


    # --------------------------------------
    # Automatically find browser
    # --------------------------------------

    for browser_name in supported_browsers:

        path = find_browser(browser_name)


        if path:

            try:

                subprocess.Popen([
                    path,
                    url
                ])

                return (
                    f"{browser_name.capitalize()} opened {url}."
                )

            except Exception as e:

                return (
                    f"Failed to open {browser_name}: {e}"
                )


    return (
        "No supported browser was found."
    )


# ==========================================
# CALCULATOR
# ==========================================

def calculate(expression):

    try:

        allowed = "0123456789+-*/(). %"


        if not all(
            char in allowed
            for char in expression
        ):

            return (
                "Invalid arithmetic expression."
            )


        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )


        return str(result)


    except Exception:

        return (
            "Calculation failed."
        )


# ==========================================
# TIME
# ==========================================

def get_time(timezone="Asia/Kolkata"):

    try:

        current_time = datetime.now(
            ZoneInfo(timezone)
        )


        return current_time.strftime(
            "%I:%M:%S %p (%Z)"
        )


    except Exception:

        return (
            f"Unknown timezone: {timezone}"
        )

# ==========================================
# PLAYWRIGHT BROWSER
# ==========================================

def browser_open(url):

    try:

        return browser.open(url)

    except Exception as e:

        return f"Browser automation failed: {e}"

# ==========================================
# PLAY VIDEO
# ==========================================

def browser_play():

    try:

        return browser.play()

    except Exception as e:

        return f"Browser play failed: {e}"

# ==========================================
# SEARCH YOUTUBE
# ==========================================

def browser_search(query):

    try:

        return browser.search_youtube(query)

    except Exception as e:

        return f"Browser search failed: {e}"