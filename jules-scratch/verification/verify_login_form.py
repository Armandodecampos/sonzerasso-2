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

        # Verify that the new login form elements are visible
        expect(page.get_by_label("Email")).to_be_visible()
        # Use a more specific locator by chaining it to the visible form container
        expect(page.locator("#login-form-container").get_by_label("Senha")).to_be_visible()
        expect(page.get_by_role("button", name="Entrar")).to_be_visible()

        # Take a screenshot of the login form
        page.screenshot(path="jules-scratch/verification/login_form_verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()