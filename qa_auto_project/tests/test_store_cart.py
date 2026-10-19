import time
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.cart_page import CartPage


@pytest.mark.id("5")
def test_add_to_cart_precise_price(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login(username="admin", password="admin")
    store: StorePage = StorePage(driver)
    expected_digits: str = store.get_product_price_digits()
    store.add_product_to_cart()
    store.go_to_cart()
    cart: CartPage = CartPage(driver)
    total_text: str = cart.get_total_text()
    assert expected_digits in total_text, \
        f"Ошибка: сумма '{expected_digits}' не найдена в итоговой стоимости корзины. Итог: '{total_text}'"


@pytest.mark.id("6")
def test_empty_cart(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login(username="admin", password="admin")
    store: StorePage = StorePage(driver)
    store.go_to_cart()
    cart: CartPage = CartPage(driver)
    assert cart.get_empty_message().is_displayed(), \
        "Ошибка пустой корзины: сообщение о том, что корзина пуста, отсутствует"


@pytest.mark.id("16")
def test_max_product_quantity_limit_bug(driver: WebDriver) -> None:
    """Тест на баг: система позволяет добавить более 100 единиц товара через плюс в магазине"""
    login_page: LoginPage = LoginPage(driver)
    login_page.login(username="admin", password="admin")
    store: StorePage = StorePage(driver)
    store.add_product_to_cart()
    time.sleep(0.5)
    store.click_plus_button_multiple_times(100)
    quantity_input: WebElement = store.find_element(store.QUANTITY_INPUT)
    actual_quantity: int = int(quantity_input.get_attribute("value"))
    assert actual_quantity <= 100, \
        f"БАГ ОБНАРУЖЕН: Система позволила добавить {actual_quantity} шт. одного товара (превышен лимит в 100 единиц)!"
