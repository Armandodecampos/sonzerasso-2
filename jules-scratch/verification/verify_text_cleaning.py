from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        page.goto("http://localhost:8000")

        # Espera até que a função de limpeza esteja disponível no objeto window
        page.wait_for_function("window.cleanTextForAPI")

        # Casos de teste: entrada e saída esperada
        test_cases = {
            "Song Title (feat. Some Artist)": "Song Title",
            "Another Song (with Another Artist)": "Another Song",
            "Track Name [Awesome Remix]": "Track Name",
            "My Song (Official Video)": "My Song",
            "Hit Song - Remastered 2024": "Hit Song",
            "Complex (feat. X) [Y Remix] - Remastered": "Complex"
        }

        # Executa os testes
        for test_input, expected_output in test_cases.items():
            cleaned_text = page.evaluate(f"window.cleanTextForAPI('{test_input}')")
            print(f"Testing '{test_input}': Got '{cleaned_text}', Expected '{expected_output}'")
            assert cleaned_text == expected_output

        # Se todas as asserções passarem, a lógica está correta.
        # Tira uma captura de tela de uma página de sucesso para o fluxo.
        page.set_content("<html><body><h1>Verificação da função cleanTextForAPI concluída com sucesso!</h1></body></html>")
        page.screenshot(path="jules-scratch/verification/text_cleaning_verification.png")
        print("\\nVerificação da lógica de limpeza de texto concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro durante a execução do script Playwright: {e}")
        page.set_content(f"<html><body><h1>Erro na verificação</h1><p>{e}</p></body></html>")
        page.screenshot(path="jules-scratch/verification/text_cleaning_error.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
