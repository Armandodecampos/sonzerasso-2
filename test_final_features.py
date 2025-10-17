import re
from playwright.sync_api import Page, expect, sync_playwright
import os

def test_final_features(page: Page):
    """
    Verifica de forma focada as últimas alterações solicitadas:
    1. O título da pesquisa não tem prefixo.
    2. A animação do leitor de música foi removida.
    3. O histórico de "anterior/próximo" funciona no modo aleatório.
    4. A nova cor de fundo da UI é #141414.
    """
    page.goto("file://" + os.path.abspath("index.htm"))

    # --- SETUP INICIAL ---
    page.evaluate("""() => {
        toggleUI(true);
        playRandomSong();
    }""")

    music_player = page.locator("#music-player")
    player_title = page.locator("#player-song-title")

    expect(music_player).to_be_visible()
    expect(player_title).not_to_have_text("Nome da Música", timeout=10000)
    initial_song_title = player_title.inner_text()
    print(f"Música inicial: {initial_song_title}")

    # --- 1. TESTE DO TÍTULO DA PESQUISA ---
    print("\n--- Testando o título da pesquisa ---")
    page.click("#explore-nav-button")
    explore_modal = page.locator("#explore-modal")
    expect(explore_modal).to_be_visible()

    search_input = page.locator("#explore-search-input")
    explore_title = page.locator("#explore-title")

    search_term = "night"
    search_input.fill(search_term)
    page.wait_for_timeout(500)

    expect(explore_title).to_have_text(search_term)
    print(f"✅ Título da pesquisa verificado.")

    page.click("#close-explore-modal")
    expect(explore_modal).to_be_hidden()

    # --- 2. TESTE DA ANIMAÇÃO REMOVIDA ---
    print("\n--- Verificando a remoção da animação ---")
    player_classes = music_player.get_attribute("class")
    assert "transition-transform" not in player_classes
    print("✅ Animação do leitor removida.")

    # --- 3. TESTE DO HISTÓRICO DE REPRODUÇÃO ---
    print("\n--- Testando o histórico de Próximo/Anterior ---")
    page.locator("#player-song-title").dispatch_event('click')
    fullscreen_player = page.locator("#fullscreen-player")
    expect(fullscreen_player).to_be_visible()

    next_button = page.locator("#next-btn")
    prev_button = page.locator("#prev-btn")

    next_button.click()
    page.wait_for_timeout(1000)
    second_song_title = player_title.inner_text()
    print(f"Segunda música: {second_song_title}")
    assert initial_song_title != second_song_title

    prev_button.click()
    page.wait_for_timeout(500)
    expect(player_title).to_have_text(initial_song_title)
    print(f"✅ Voltou para a primeira música.")

    next_button.click()
    page.wait_for_timeout(500)
    expect(player_title).to_have_text(second_song_title)
    print(f"✅ Avançou para a segunda música.")

    # --- 4. TESTE DA NOVA COR DE FUNDO ---
    print("\n--- Verificando a nova cor de fundo #141414 ---")
    expected_color = "rgb(20, 20, 20)"
    expect(fullscreen_player).to_have_css("background-color", expected_color)
    print("✅ Cor do leitor em tela cheia verificada.")

    page.click("#close-fullscreen-player")

# Boilerplate
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_final_features(page)
            print("\n✅ Todos os testes passaram!")
        except Exception as e:
            print(f"\n❌ Teste falhou: {e}")
        finally:
            browser.close()