from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()
ZIP_CODE = os.getenv("ZIP_CODE")
TARGET_URL = os.getenv("TARGET_URL")

def get_show_dates() -> set[str]:
    with sync_playwright() as p:
        # slow_mo=200 prevents race conditions; headless=True for production
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        page.goto(TARGET_URL, wait_until="domcontentloaded")

        # Fill and fire required events
        page.fill("#ZipSearchText", ZIP_CODE)
        page.evaluate("document.getElementById('ZipSearchText').dispatchEvent(new Event('change', {bubbles: true}))")
        page.evaluate("document.getElementById('ZipSearchText').dispatchEvent(new Event('blur', {bubbles: true}))")

        # Click the submit button (reliable)
        page.click("input[value='Search by ZIP Code']")

        # Wait for the carousel to load all dates
        # 10 seconds is more than enough (debug worked with 5s)
        page.wait_for_timeout(10000)

        # Collect all date links
        links = page.query_selector_all("#showdatesCarousel a.showdate-link")
        show_dates = {link.get_attribute("data-datevalue") for link in links if link.get_attribute("data-datevalue")}
        browser.close()
        return show_dates