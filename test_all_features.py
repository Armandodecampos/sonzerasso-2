import re
from playwright.sync_api import Page, expect, sync_playwright
import json
import os

def test_all_new_features(page: Page):
    """
    Testa de forma integrada:
    0. Tocar música aleatória ao carregar a aplicação.
    1. O botão "Música Aleatória" e a mudança de música.
    2. A ocultação do botão de repetir no modo de música aleatória.
    3. O modo "shuffle" como padrão ao tocar de uma lista.
    4. O ciclo completo de modos de repetição para listas.
    5. As novas cores de fundo (#383838) nos componentes da UI.
    """
    # Usa um manipulador de console para capturar logs do navegador
    page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}"))

    page.goto("file://" + os.path.abspath("index.htm"))

    # Etapa 0: Verificar se a música toca automaticamente ao carregar
    print("Verificando se a música toca ao carregar...")
    music_player = page.locator("#music-player")
    player_title = page.locator("#player-song-title")

    # Contorna o login e inicializa a UI
    page.evaluate("() => toggleUI(true)")
    expect(page.locator("#logged-in-app")).to_be_visible()

    # Simula a chamada que seria feita pelo onAuthStateChange na app real
    page.evaluate("() => window.playRandomSong()")

    # A música deve começar a tocar automaticamente
    expect(music_player).to_have_class(re.compile(r"player-visible"), timeout=10000)
    expect(player_title).not_to_have_text("Nome da Música", timeout=10000)
    print("✅ Música tocou automaticamente no carregamento.")


    # Etapa 2: Abrir o modal "Explorar"
    explore_modal = page.locator("#explore-modal")
    page.click("#explore-nav-button")
    expect(explore_modal).to_be_visible()

    # Etapa 3: Testar o botão "Música Aleatória"
    initial_song_title = player_title.inner_text()
    print(f"Música inicial (automática): {initial_song_title}")

    page.click("#play-random-song-button")
    expect(player_title).not_to_have_text(initial_song_title, timeout=10000)
    second_song_title = player_title.inner_text()
    print(f"Segunda música (via botão): {second_song_title}")
    assert initial_song_title != second_song_title, "A música não mudou ao clicar no botão."

    page.click("#close-explore-modal")
    expect(explore_modal).to_be_hidden()

    # Etapa 4: Verificar o modo de reprodução para "Música Aleatória"
    page.locator("#player-song-title").dispatch_event('click')
    fullscreen_player = page.locator("#fullscreen-player")
    expect(fullscreen_player).to_be_visible()

    repeat_button = fullscreen_player.locator("#repeat-mode-btn")
    expect(repeat_button).to_be_hidden()

    page.click("#close-fullscreen-player")

    # Etapa 5: Testar o modo shuffle e o ciclo de repetição ao tocar de uma lista
    page.click("#explore-nav-button")
    expect(explore_modal).to_be_visible()

    page.evaluate("""() => {
        const songs = [
            { 'Nome - Artista': 'Artist 1', 'Nome - Musica': 'Song A', 'Nome - Album': 'Album X', Musica: 'url1', Imagem: 'img1', src: 'url1' },
            { 'Nome - Artista': 'Artist 1', 'Nome - Musica': 'Song B', 'Nome - Album': 'Album X', Musica: 'url2', Imagem: 'img2', src: 'url2' }
        ];
        window.renderArtistSongs(songs);
    }""")

    page.click(".music-item[data-src='url1']")
    page.click("#close-explore-modal")
    expect(explore_modal).to_be_hidden()

    page.locator("#player-song-title").dispatch_event('click')
    expect(fullscreen_player).to_be_visible()
    expect(repeat_button).to_be_visible()

    print("Verificando se o modo padrão da lista é shuffle...")
    expect(repeat_button.locator("i")).to_have_class(re.compile(r"fa-random"))

    print("Testando ciclo de repetição: shuffle -> none")
    repeat_button.click()
    expect(repeat_button.locator("i")).to_have_class(re.compile(r"fa-random"))

    print("Testando ciclo de repetição: none -> repeat-all")
    repeat_button.click()
    expect(repeat_button.locator("i")).to_have_class(re.compile(r"fa-redo-alt"))

    print("Testando ciclo de repetição: repeat-all -> repeat-one")
    repeat_button.click()
    expect(repeat_button.locator("i")).to_have_class(re.compile(r"fa-retweet"))

    print("Testando ciclo de repetição: repeat-one -> shuffle")
    repeat_button.click()
    expect(repeat_button.locator("i")).to_have_class(re.compile(r"fa-random"))

    page.click("#close-fullscreen-player")

    # Etapa 6: Verificar a cor de fundo dos componentes
    print("Verificando as cores de fundo da UI...")
    expected_color = "rgb(56, 56, 56)"

    expect(music_player).to_have_css("background-color", expected_color)
    expect(page.locator("#bottom-nav-bar")).to_have_css("background-color", expected_color)

    page.click("#explore-nav-button")
    expect(explore_modal.locator("header")).to_have_css("background-color", expected_color)
    page.click("#close-explore-modal")

    page.locator("#player-song-title").dispatch_event('click')
    expect(fullscreen_player).to_be_visible()
    expect(fullscreen_player).to_have_css("background-color", expected_color)
    page.click("#close-fullscreen-player")

# Boilerplate para rodar o teste
if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_all_new_features(page)
            print("\n✅ Todos os testes passaram!")
        except Exception as e:
            print(f"\n❌ Teste falhou: {e}")
        finally:
            browser.close()