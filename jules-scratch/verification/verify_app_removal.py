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

        # Manually trigger the logged-in UI
        page.evaluate("window.toggleUI(true)")

        # Manually render the apps using the exposed function and data
        page.evaluate("window.renderApps(window.fixedAppsMasterList, [])")

        # Wait for the main app container to be visible
        expect(page.locator("#logged-in-app")).to_be_visible()

        # Verify that the "Notas" app is visible
        expect(page.locator("#button-grid-container").get_by_text("Notas")).to_be_visible()

        # Verify that the "Compras" and "Receitas" apps are NOT visible
        expect(page.get_by_text("Compras")).not_to_be_visible()
        expect(page.get_by_text("Receitas")).not_to_be_visible()

        # Take a screenshot of the dashboard
        page.screenshot(path="jules-scratch/verification/app_removal_verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()