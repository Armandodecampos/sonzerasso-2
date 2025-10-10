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

        # Manually trigger the logged-in UI and render the apps
        page.evaluate("""
            window.toggleUI = toggleUI;
            window.renderApps = renderApps;
            window.fixedAppsMasterList = fixedAppsMasterList;
            window.toggleUI(true);
            window.renderApps(window.fixedAppsMasterList, []);
        """)

        # Find the "Explorar" app container and click its icon to show the action bar
        explore_app_container = page.locator(".app-container", has_text="Explorar")
        explore_app_container.locator(".grid-item").click()

        # Wait for the action bar to appear and click the "Open" button
        expect(page.locator("#app-action-bar")).to_be_visible()
        page.locator("#open-app-button").click()

        # Verify that the "Explorar" modal is visible
        expect(page.locator("#explore-modal")).to_be_visible()
        expect(page.get_by_role("heading", name="Explorar")).to_be_visible()

        # Take a screenshot of the "Explorar" modal
        page.screenshot(path="jules-scratch/verification/explore_app_verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()