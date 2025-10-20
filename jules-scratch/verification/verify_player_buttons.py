
import asyncio
from playwright.sync_api import sync_playwright, expect

def verify_player_buttons_theme():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 1. Navega para a aplicação
            page.goto("http://localhost:8000/index.htm", timeout=60000)

            # 2. Força o estado de "logado" e torna o player visível
            page.evaluate("window.showMainApp()")
            page.wait_for_timeout(500)
            page.evaluate("window.toggleUI(true)")
            page.evaluate("document.getElementById('music-player').classList.remove('hidden')")

            # --- VERIFICAÇÃO COM TEMA CLARO ---

            # 3. Aplica o tema "Claro"
            page.evaluate("window.applyPreferences({ theme: 'light' })")
            page.wait_for_timeout(500)

            # 4. Abre o player em tela cheia
            page.locator("#music-player").click()
            expect(page.locator("#fullscreen-player")).to_be_visible()
            page.wait_for_timeout(500)

            # 5. Tira a captura de tela do player com tema claro
            page.locator("#fullscreen-player").screenshot(path="jules-scratch/verification/player_light_theme.png")

            # 6. Fecha o player
            page.locator("#close-fullscreen-player").click()
            expect(page.locator("#fullscreen-player")).to_be_hidden()

            # --- VERIFICAÇÃO COM TEMA ESCURO ---

            # 7. Aplica o tema "Escuro"
            page.evaluate("window.applyPreferences({ theme: 'dark' })")
            page.wait_for_timeout(500)

            # 8. Reabre o player em tela cheia
            page.locator("#music-player").click()
            expect(page.locator("#fullscreen-player")).to_be_visible()
            page.wait_for_timeout(500)

            # 9. Tira a captura de tela do player com tema escuro
            page.locator("#fullscreen-player").screenshot(path="jules-scratch/verification/player_dark_theme.png")

            print("Verificação dos botões do player concluída. Capturas de tela salvas.")

        except Exception as e:
            print(f"Ocorreu um erro durante a verificação: {e}")
            page.screenshot(path="jules-scratch/verification/error_player_buttons.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_player_buttons_theme()
