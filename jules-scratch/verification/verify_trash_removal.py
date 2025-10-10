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
        """)

        # Manually trigger the logged-in UI
        page.evaluate("window.toggleUI(true)")

        # Verify that the trash bin button is NOT visible
        expect(page.locator("#trash-bin-button")).not_to_be_visible()

        # Take a screenshot of the dashboard
        page.screenshot(path="jules-scratch/verification/trash_removal_verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()