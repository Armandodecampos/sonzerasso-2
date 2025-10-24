from playwright.sync_api import sync_playwright, expect
import time

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Navega para a página
        page.goto("http://localhost:8000/index.htm")

        # Espera a UI principal carregar (expondo a função `toggleUI`)
        page.wait_for_function("window.toggleUI")

        # Bypassa o login e mostra a UI principal
        page.evaluate("() => window.toggleUI(true)")

        # Espera o botão Explorar aparecer
        fab_explore = page.locator("#fab-explore")
        expect(fab_explore).to_be_visible()
        fab_explore.click()

        # Espera o modal Explorar abrir e o campo de busca estar visível
        explore_modal = page.locator("#explore-modal")
        expect(explore_modal).to_be_visible()
        search_input = page.locator("#explore-search-input")
        expect(search_input).to_be_visible()

        # Digita um termo de busca que deve encontrar um artista
        # Usando um artista genérico que provavelmente existe nos dados de teste
        search_input.type("Artista")

        # Espera os resultados da busca aparecerem
        # O primeiro resultado deve conter o nome do artista
        artist_link = page.locator('.music-artist-display:has-text("Artista")').first
        expect(artist_link).to_be_visible(timeout=10000)

        # Clica no link do artista
        artist_link.click()

        # Verifica se a visão mudou para a lista de músicas do artista
        explore_title = page.locator("#explore-title")
        expect(explore_title).to_have_text("Artista")

        # Verifica se o botão de voltar está visível
        back_button = page.locator("#explore-back-button")
        expect(back_button).to_be_visible()

        # Tira a screenshot
        screenshot_path = "jules-scratch/verification/verification.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot salva em {screenshot_path}")

    except Exception as e:
        print(f"Ocorreu um erro durante a verificação: {e}")
        # Tira uma screenshot de erro para depuração
        page.screenshot(path="jules-scratch/verification/error.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)
