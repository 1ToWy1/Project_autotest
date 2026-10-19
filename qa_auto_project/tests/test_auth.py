import pytest
from pages.login_page import LoginPage


@pytest.mark.id("1")
def test_auth_success(driver):
    login_page = LoginPage(driver)
    login_page.login("admin", "admin")
    assert "manageProductsPage" in driver.current_url or login_page.LOGOUT_BUTTON, \
        "Ошибка авторизации: не удалось войти в систему под учетной записью администратора"


@pytest.mark.id("2")
def test_auth_success_user(driver):
    login_page = LoginPage(driver)
    login_page.login("покупатель", "покупатель")
    assert "manageProductsPage" in driver.current_url or login_page.LOGOUT_BUTTON, \
        "Ошибка авторизации: не удалось войти в систему под учетной записью покупателя"


@pytest.mark.id("3")
def test_auth_success_invalid(driver):
    login_page = LoginPage(driver)
    login_page.open()
    initial_url = driver.current_url
    login_page.login("fake1", "fake1")
    assert driver.current_url == initial_url, \
        f"Ошибка: произошел переход на другой URL ({driver.current_url}), хотя данные неверные"


@pytest.mark.id("4")
def test_logout(driver):
    login_page = LoginPage(driver)
    login_page.login("admin", "admin")
    login_page.logout()
    assert len(driver.find_elements(*LoginPage.USERNAME_INPUT)) > 0, \
        "Ошибка выхода из системы: форма авторизации не отображается после логаута"


@pytest.mark.id("15")
def test_https_protocol(driver):
    """Тест на баг: проверка работы по HTTPS"""
    driver.get("http://91.197.96.80/")
    current_url = driver.current_url
    assert current_url.startswith("https://"), \
        f"Ошибка безопасности (баг): сайт доступен по небезопасному протоколу HTTP (Текущий URL: {current_url})"
