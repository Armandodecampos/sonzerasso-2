from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("http://localhost:8000/index.htm", wait_until="networkidle")

            page.wait_for_function("() => window.toggleUI")
            page.evaluate("() => window.toggleUI(true)")
            expect(page.locator("#button-grid-container")).to_be_visible()

            mock_folders = [{'id': f'folder-{i}', 'title': f'Pasta de Teste {i}', 'isFolder': True} for i in range(20)]
            page.evaluate("items => window.renderApps(items, items.map(i => i.id))", mock_folders)

            # Com a nova estrutura de wrapper, a barra de rolagem deve inicializar automaticamente.
            # Aumentei o timeout para dar tempo para a biblioteca carregar e inicializar.
            expect(page.locator("#button-grid-container .ss-track")).to_be_visible(timeout=10000)
            page.screenshot(path="jules-scratch/verification/folders_scrollbar_final.png")

            page.locator("#fab-explore").click()
            expect(page.locator("#explore-modal")).to_be_visible()

            mock_artists = [f"Artista de Teste {i}" for i in range(30)]
            page.evaluate("artists => window.renderArtists(artists)", mock_artists)

            expect(page.locator("#explore-content-container .ss-track")).to_be_visible(timeout=10000)
            page.screenshot(path="jules-scratch/verification/artists_scrollbar_final.png")

        except Exception as e:
            print(f"Ocorreu um erro durante a execução do script Playwright: {e}")
            page.screenshot(path="jules-scratch/verification/error_screenshot.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
