from playwright.sync_api import sync_playwright
from pages.login_po import LoginPage

def test_login_with_empty_fields():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Запуск браузера
        context = browser.new_context()
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.open()
        
        login_page.input_username("")  # Оставляем поле username пустым
        login_page.input_password("")  # Оставляем поле password пустым
        login_page.click_login()
        
        error_message = login_page.get_error_message()
        assert error_message == "Epic sadface: Username is required", f"Unexpected error message: {error_message}"
        
        context.clear_cookies()
        browser.close()

