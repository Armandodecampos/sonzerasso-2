import re
from playwright.sync_api import Page, expect, sync_playwright
import os

def test_player_and_search_updates(page: Page):
    """
    Verifica as seguintes atualizações de forma focada:
    1. O título da pesquisa não tem prefixo.
    2. A animação do leitor foi removida (verificação indireta).
    3. O histórico de "anterior/próximo" funciona no modo aleatório.
    """
    page.goto("file://" + os.path.abspath("index.htm"))

    # --- SETUP INICIAL ---
    # Simula o login e o arranque da aplicação
    page.evaluate("() => toggleUI(true)")
    page.evaluate("() => playRandomSong()")

    music_player = page.locator("#music-player")
    player_title = page.locator("#player-song-title")

    # Confirma que o leitor está visível
    expect(music_player).to_be_visible()
    initial_song_title = player_title.inner_text()
    print(f"Música inicial: {initial_song_title}")

    # --- 1. TESTE DO TÍTULO DA PESQUISA ---
    print("\n--- Testando o título da pesquisa ---")
    page.click("#explore-nav-button")
    explore_modal = page.locator("#explore-modal")
    expect(explore_modal).to_be_visible()

    search_input = page.locator("#explore-search-input")
    explore_title = page.locator("#explore-title")

    search_term = "love"
    search_input.fill(search_term)
    page.wait_for_timeout(500) # Espera pelo debounce da pesquisa

    expect(explore_title).to_have_text(search_term)
    print(f"✅ Título da pesquisa verificado. Mostrou: '{explore_title.inner_text()}'")

    page.click("#close-explore-modal")
    expect(explore_modal).to_be_hidden()

    # --- 2. TESTE DA ANIMAÇÃO REMOVIDA (VERIFICAÇÃO INDIRETA) ---
    print("\n--- Verificando a remoção da animação (indireto) ---")
    player_classes = music_player.get_attribute("class")
    assert "transition" not in player_classes
    assert "transform" not in player_classes
    print("✅ Classes de animação não encontradas no leitor.")

    # --- 3. TESTE DO HISTÓRICO DE REPRODUÇÃO ---
    print("\n--- Testando o histórico de Próximo/Anterior ---")
    page.locator("#player-song-title").dispatch_event('click')
    fullscreen_player = page.locator("#fullscreen-player")
    expect(fullscreen_player).to_be_visible()

    next_button = page.locator("#next-btn")
    prev_button = page.locator("#prev-btn")

    # Toca a próxima música (segunda música)
    next_button.click()
    page.wait_for_timeout(1000)
    second_song_title = player_title.inner_text()
    print(f"Segunda música: {second_song_title}")
    assert initial_song_title != second_song_title

    # Toca a próxima música (terceira música)
    next_button.click()
    page.wait_for_timeout(1000)
    third_song_title = player_title.inner_text()
    print(f"Terceira música: {third_song_title}")
    assert second_song_title != third_song_title

    # Volta para a música anterior (deve ser a segunda)
    prev_button.click()
    page.wait_for_timeout(500)
    expect(player_title).to_have_text(second_song_title)
    print(f"✅ Voltou para a segunda música: '{player_title.inner_text()}'")

    # Volta para a música anterior novamente (deve ser a primeira)
    prev_button.click()
    page.wait_for_timeout(500)
    expect(player_title).to_have_text(initial_song_title)
    print(f"✅ Voltou para a primeira música: '{player_title.inner_text()}'")

    # Avança novamente (deve ser a segunda)
    next_button.click()
    page.wait_for_timeout(500)
    expect(player_title).to_have_text(second_song_title)
    print(f"✅ Avançou para a segunda música: '{player_title.inner_text()}'")

    page.click("#close-fullscreen-player")


# Boilerplate para rodar o teste
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_player_and_search_updates(page)
            print("\n✅ Todos os testes passaram!")
        except Exception as e:
            print(f"\n❌ Teste falhou: {e}")
        finally:
            browser.close()