from playwright.sync_api import sync_playwright, expect
import time
import json

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto("http://localhost:8000")

        # Fazer login
        page.locator("#email").fill("test@test.com")
        page.locator("#password").fill("password")
        page.locator("#login-button").click()

        # Forçar a UI a aparecer
        page.evaluate("() => window.toggleUI(true)")

        # Simular a renderização de muitos apps/pastas para forçar a scrollbar na grelha principal
        mock_apps = [{"id": f"folder_{i}", "title": f"Pasta {i}", "isFolder": True} for i in range(50)]
        page.evaluate("mock_apps => window.renderApps(mock_apps, [])", mock_apps)

        # 1. Verificar a Grelha Principal (#button-grid-container)
        time.sleep(1) # Pequena pausa para garantir a renderização
        page.screenshot(path="jules-scratch/verification/01_main_grid.png")
        print("Captura de tela da grelha principal tirada.")

        # 2. Verificar a Lista de Artistas (#explore-content-container)
        fab_explore = page.locator("#fab-explore")
        expect(fab_explore).to_be_visible(timeout=10000)
        fab_explore.click()

        explore_modal = page.locator("#explore-modal")
        expect(explore_modal).to_be_visible(timeout=5000)

        # Esperar que o conteúdo seja carregado
        expect(page.locator('#explore-content-container .music-item').first).to_be_visible(timeout=15000)
        page.screenshot(path="jules-scratch/verification/02_artist_list.png")
        print("Captura de tela da lista de artistas tirada.")

        page.locator("#close-explore-modal").click()
        expect(explore_modal).to_be_hidden()

        # 3. Verificar o Conteúdo da Pasta (#folder-music-list-container)
        folder_item = page.locator(".app-container[data-is-folder='true']").first
        expect(folder_item).to_be_visible(timeout=5000)
        folder_item.click()

        open_folder_button = page.locator("#folder-action-open")
        expect(open_folder_button).to_be_visible()
        open_folder_button.click()

        folder_content_modal = page.locator("#folder-content-modal")
        expect(folder_content_modal).to_be_visible()

        # Simular conteúdo para forçar a scrollbar
        page.evaluate("() => window.fetchAndDisplayFolderContent('mock_folder_id')")

        time.sleep(1) # Pausa para renderizar
        page.screenshot(path="jules-scratch/verification/03_folder_content.png")
        print("Captura de tela do conteúdo da pasta tirada.")

    except Exception as e:
        print(f"Ocorreu um erro durante a verificação: {e}")
        page.screenshot(path="jules-scratch/verification/error.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
