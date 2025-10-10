import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 1. Navigate to the local server
        await page.goto('http://localhost:8000/index.htm')

        # 2. Expose the module-scoped function to the global window object
        await page.evaluate('window.fetchAndRenderApps = fetchAndRenderApps;')

        # 3. Wait for the function to be available
        await page.wait_for_function('window.fetchAndRenderApps !== undefined')

        # 4. Simulate logged-in state and manually trigger app rendering
        js_code = """
        async () => {
            document.getElementById('main-container').classList.add('hidden');
            document.getElementById('logged-in-app').classList.remove('hidden');
            document.getElementById('user-email-display').textContent = 'test@example.com';
            await window.fetchAndRenderApps(null);
        }
        """
        await page.evaluate(js_code)


        # 5. Click the "Explorar" app
        await page.click('div[data-id="explore-app"]')

        # 6. Wait for the modal to be visible
        explore_modal = page.locator('#explore-modal')
        await expect(explore_modal).to_be_visible()

        # 7. Get the music list container
        music_list_container = page.locator('#music-list-container')

        # 8. Scroll down to trigger infinite scroll
        for _ in range(5):
            await music_list_container.evaluate('(el) => el.scrollTop = el.scrollHeight')
            await page.wait_for_timeout(1000)

        # 9. Take a screenshot
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
