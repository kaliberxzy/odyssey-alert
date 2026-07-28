from playwright.sync_api import sync_playwright

URL = "https://www.cinemark.com/movies/the-odyssey-imax-70mm"

def get_show_dates() -> set[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_selector("#showdatesCarousel a.showdate-link", state="attached")
        dates = {
            a.get_attribute("data-datevalue")
            for a in page.query_selector_all("#showdatesCarousel a.showdate-link")
        }
        browser.close()
        return dates