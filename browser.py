from playwright.sync_api import sync_playwright


# ==========================================
# BROWSER CONTROLLER
# ==========================================

class BrowserController:

    def __init__(self):

        self.playwright = None
        self.context = None
        self.page = None


    # ======================================
    # START / RESTART BROWSER
    # ======================================

    def start(self):

        # ----------------------------------
        # Check whether the current
        # Playwright session is actually alive
        # ----------------------------------

        if (
            self.context is not None
            and not self.context.is_closed()
            and self.page is not None
            and not self.page.is_closed()
        ):
            return


        # ----------------------------------
        # Clean up stale context
        # ----------------------------------

        if self.context is not None:

            try:
                self.context.close()
            except Exception:
                pass

            self.context = None
            self.page = None


        # ----------------------------------
        # Start Playwright if necessary
        # ----------------------------------

        if self.playwright is None:

            self.playwright = sync_playwright().start()


        # ----------------------------------
        # Launch controlled Chrome
        # ----------------------------------

        try:

            self.context = (
                self.playwright.chromium
                .launch_persistent_context(
                    "browser_data",
                    channel="chrome",
                    headless=False
                )
            )

        except Exception:

            # Playwright itself may also have died.
            # Restart the whole Playwright process.

            try:
                self.playwright.stop()
            except Exception:
                pass

            self.playwright = sync_playwright().start()

            self.context = (
                self.playwright.chromium
                .launch_persistent_context(
                    "browser_data",
                    channel="chrome",
                    headless=False
                )
            )


        # ----------------------------------
        # Get existing page or create one
        # ----------------------------------

        if self.context.pages:

            self.page = self.context.pages[0]

        else:

            self.page = self.context.new_page()

    # ======================================
    # OPEN URL
    # ======================================

    def open(self, url):

        self.start()

        self.page.goto(url)

        return f"Opened {url}"


    # ======================================
    # SEARCH YOUTUBE
    # ======================================

    def search_youtube(self, query):

        self.start()

        # Make sure we're on YouTube.
        if "youtube.com" not in self.page.url:

            self.page.goto(
                "https://www.youtube.com"
            )

        # Find YouTube search box.
        search_box = self.page.locator(
            'input[name="search_query"]'
        )

        search_box.fill(query)

        search_box.press("Enter")

        # Wait for results to appear.
        self.page.wait_for_timeout(2000)

        # --------------------------------------
        # Get video result titles
        # --------------------------------------

        titles = self.page.locator(
            "a#video-title"
        ).all_inner_texts()

        # --------------------------------------
        # Get video URLs
        # --------------------------------------

        links = self.page.locator(
            "a#video-title"
        ).evaluate_all(
            """
            elements => elements.map(
                element => element.href
            )
            """
        )

        # --------------------------------------
        # Build result list
        # --------------------------------------

        results = []

        for title, url in zip(titles, links):

            title = title.strip()

            if not title:
                continue

            results.append({
                "title": title,
                "url": url
            })

            if len(results) >= 5:
                break

        # --------------------------------------
        # Return real page data
        # --------------------------------------

        if not results:

            return (
                f'YouTube search completed for "{query}", '
                "but no video results were found."
            )

        return str(results)


    # ======================================
    # CURRENT URL
    # ======================================

    def current_url(self):

        if self.page is None:

            return "No browser page is open."

        return self.page.url

        # ======================================
    # PLAY VIDEO
    # ======================================

    def play(self):

        self.start()

        if "youtube.com/watch" not in self.page.url:

            return "No YouTube video is currently open."

        try:

            play_button = self.page.locator(
                "button.ytp-play-button"
            )

            play_button.click()

            self.page.wait_for_timeout(1000)

            return "Video play button clicked."

        except Exception as e:

            return f"Could not play video: {e}"


    # ======================================
    # CLOSE
    # ======================================

    def close(self):

        if self.context:

            self.context.close()

        if self.playwright:

            self.playwright.stop()

        self.page = None
        self.context = None
        self.playwright = None


# ==========================================
# GLOBAL BROWSER
# ==========================================

browser = BrowserController()