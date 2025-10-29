from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        page.goto("http://localhost:8000")

        # Mockar o Supabase para evitar erros de rede
        page.evaluate("""
            window.supabase = {
                createClient: () => ({
                    auth: {
                        onAuthStateChange: (callback) => {
                            const mockSession = { user: { id: 'mock-id', email: 'test@test.com' } };
                            callback('SIGNED_IN', mockSession);
                        }
                    },
                    from: () => ({
                        select: () => ({
                            eq: () => ({
                                single: () => ({ data: { preferences: {} }, error: null })
                            })
                        }),
                        upsert: () => ({})
                    })
                })
            };
        """)

        # Forçar a UI para o estado logado e inicializar a aplicação
        page.wait_for_function("window.showMainApp")
        page.evaluate("window.showMainApp()")

        # Espera a renderização dos apps, indicando que a UI principal carregou
        page.wait_for_selector('.app-container', state='visible')

        # Toca uma música aleatória para o player aparecer
        page.evaluate("window.playRandomSong()")

        # Espera o player minimizado aparecer
        music_player = page.locator("#music-player")
        music_player.wait_for(state='visible')

        # Clica no player para abrir a tela cheia
        music_player.click()

        # Espera o contêiner da letra estar visível no player de tela cheia
        lyrics_container = page.locator("#lyrics-container")
        lyrics_container.wait_for(state='visible')

        # Tira a captura de tela
        page.screenshot(path="jules-scratch/verification/lyrics_fallback_verification.png")

    except Exception as e:
        print(f"Ocorreu um erro durante a execução do script Playwright: {e}")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
