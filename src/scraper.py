from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()
ZIP_CODE = os.getenv("ZIP_CODE")
TARGET_URL = os.getenv("TARGET_URL")

def get_show_dates() -> set[str]:
    with sync_playwright() as p:
        # Use slow_mo to mimic human interaction and avoid race conditions
        browser = p.chromium.launch(headless=True, slow_mo=200)
        page = browser.new_page()
        page.goto(TARGET_URL, wait_until="domcontentloaded")

        # Fill and fire events (some sites require them)
        page.fill("#ZipSearchText", ZIP_CODE)
        page.evaluate("document.getElementById('ZipSearchText').dispatchEvent(new Event('change', {bubbles: true}))")
        page.evaluate("document.getElementById('ZipSearchText').dispatchEvent(new Event('blur', {bubbles: true}))")

        # Click the visible submit button – this is reliable
        page.click("input[value='Search by ZIP Code']")

        # Wait 10 seconds for the carousel to fully load
        # (this matched the debug version that never failed)
        page.wait_for_timeout(10000)

        # Now collect all date links – even if a navigation happened, the page is settled
        try:
            links = page.query_selector_all("#showdatesCarousel a.showdate-link")
            show_dates = {link.get_attribute("data-datevalue") for link in links if link.get_attribute("data-datevalue")}
        except Exception:
            # If the context is destroyed (rare with the fixed wait), return empty set
            show_dates = set()

        browser.close()
        return show_dates