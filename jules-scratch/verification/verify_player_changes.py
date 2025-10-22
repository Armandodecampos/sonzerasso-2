
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    page.goto("http://localhost:8000/index.htm")

    # A página pode não inicializar completamente, então pulamos a espera
    # e tentamos interagir diretamente.

    # 1. Verificar se o player está oculto inicialmente
    music_player = page.locator("#music-player")
    expect(music_player).to_be_hidden()
    page.screenshot(path="jules-scratch/verification/01_player_hidden.png")

    # 2. Carregar uma música e verificar se o player aparece
    song_data = {
        "src": "http://example.com/song.mp3",
        "title": "Test Title",
        "artist": "Test Artist",
        "albumArt": "http://example.com/album.jpg"
    }
    # Tenta chamar a função diretamente
    page.evaluate('(song) => window.playSong(song, false, false)', song_data)
    expect(music_player).to_be_visible()
    page.screenshot(path="jules-scratch/verification/02_player_visible.png")

    # 3. Simular erro de imagem e verificar o background
    broken_song_data = {
        "src": "http://example.com/song2.mp3",
        "title": "Broken Image Song",
        "artist": "Error Artist",
        "albumArt": "http://invalid-url/broken.jpg"
    }
    page.evaluate('(song) => window.playSong(song, false, false)', broken_song_data)

    page.wait_for_timeout(500)

    album_art = page.locator("#player-album-art")
    expect(album_art).to_have_css("background-color", "rgb(26, 26, 26)")
    page.screenshot(path="jules-scratch/verification/03_broken_image.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
