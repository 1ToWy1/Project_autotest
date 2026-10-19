import time
import pytest
from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.cart_page import CartPage


@pytest.mark.id("5")
def test_add_to_cart_precise_price(driver):
    login_page = LoginPage(driver)
    login_page.login("admin", "admin")
    store = StorePage(driver)
    expected_digits = store.get_product_price_digits()
    store.add_product_to_cart()
    store.go_to_cart()
    cart = CartPage(driver)
    total_text = cart.get_total_text()
    assert expected_digits in total_text, \
        f"Ошибка: сумма '{expected_digits}' не найдена в итоговой стоимости корзины. Итог: '{total_text}'"


@pytest.mark.id("6")
def test_empty_cart(driver):
    login_page = LoginPage(driver)
    login_page.login("admin", "admin")
    store = StorePage(driver)
    store.go_to_cart()
    cart = CartPage(driver)
    assert cart.get_empty_message().is_displayed(), \
        "Ошибка пустой корзины: сообщение о том, что корзина пуста, отсутствует"


@pytest.mark.id("16")
def test_max_product_quantity_limit_bug(driver):
    """Тест на баг: система позволяет добавить более 100 единиц товара через плюс в магазине"""
    login_page = LoginPage(driver)
    login_page.login("admin", "admin")
    store = StorePage(driver)
    store.add_product_to_cart()
    time.sleep(0.5)
    store.click_plus_button_multiple_times(100)
    quantity_input = store.find_element(store.QUANTITY_INPUT)
    actual_quantity = int(quantity_input.get_attribute("value"))
    assert actual_quantity <= 100, \
        f"БАГ ОБНАРУЖЕН: Система позволила добавить {actual_quantity} шт. одного товара (превышен лимит в 100 единиц)!"
