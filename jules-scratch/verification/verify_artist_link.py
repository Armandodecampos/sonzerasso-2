
from playwright.sync_api import sync_playwright

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("http://localhost:8000/index.htm")

            # Bypass login and show main app UI
            page.evaluate("() => window.toggleUI(true)")

            # Wait for the main app to be visible
            page.wait_for_selector("#logged-in-app", state="visible")

            # Click the explore FAB to open the modal
            page.click("#fab-explore")
            page.wait_for_selector("#explore-modal", state="visible")

            # Perform a search
            page.fill("#explore-search-input", "Artista")

            # Wait for search results to appear
            page.wait_for_selector("#explore-content-container .music-item", state="visible")

            # Take a screenshot of the search results
            page.screenshot(path="jules-scratch/verification/verification.png")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
