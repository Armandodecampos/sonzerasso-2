from playwright.sync_api import sync_playwright, expect
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('index.htm')

        # Navigate to the local HTML file
        page.goto(f'file://{file_path}')

        # Temporarily expose necessary functions to the window object for testing
        page.evaluate("""
            window.toggleUI = toggleUI;
            window.renderApps = renderApps;
            window.fixedAppsMasterList = fixedAppsMasterList;
        """)

        # Manually trigger the logged-in UI
        page.evaluate("window.toggleUI(true)")

        # Manually render the apps
        page.evaluate("window.renderApps(window.fixedAppsMasterList, [])")

        # Verify that the "Explorar" app is visible
        expect(page.locator("#button-grid-container").get_by_text("Explorar")).to_be_visible()

        # Verify that the "Notas" app is NOT visible
        expect(page.get_by_text("Notas")).not_to_be_visible()

        # Take a screenshot of the dashboard
        page.screenshot(path="jules-scratch/verification/notes_removal_verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()