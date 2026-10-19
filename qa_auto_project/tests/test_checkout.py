import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.checkout_page import CheckoutPage


@pytest.mark.id("11")
def test_successful_checkout(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login("admin", "admin")
    store: StorePage = StorePage(driver)
    store.add_product_to_cart()
    store.go_to_cart_and_checkout()
    checkout: CheckoutPage = CheckoutPage(driver)
    checkout.fill_order_form("Иван", "Иванов", "Иванович", "ул. Ленина 1", "1234567812345678")
    checkout.finish_checkout()
    success_text: str = checkout.get_success_message_text()
    assert "ваш заказ успешно создан" in success_text.lower(), \
        f"Ошибка: Ожидалась надпись о создании заказа, но получено: '{success_text}'"


@pytest.mark.id("12")
def test_empty_checkout_validation(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login("admin", "admin")
    store: StorePage = StorePage(driver)
    store.add_product_to_cart()
    store.go_to_cart_and_checkout()
    checkout: CheckoutPage = CheckoutPage(driver)
    checkout.click_submit_empty_form()
    error_text: str = checkout.get_error_message_text()
    assert "Введите имя, фамилию, отчество" in error_text, \
        f"Ошибка валидации не сработала, получено: '{error_text}'"


@pytest.mark.id("13")
def test_max_order_amount_limit_bug(driver: WebDriver) -> None:
    """Тест на баг: система не должна разрешать оформление заказа свыше 100 000 ₽"""
    login_page: LoginPage = LoginPage(driver)
    login_page.login("admin", "admin")
    store: StorePage = StorePage(driver)
    store.add_product_to_cart()
    store.go_to_cart()
    checkout: CheckoutPage = CheckoutPage(driver)
    total_amount: float = checkout.get_total_price()
    store.go_to_cart_and_checkout()
    checkout.fill_order_form("Иван", "Иванов", "Иванович", "ул. Ленина 1", "1234567812345678")
    checkout.finish_checkout()
    success_text: str = checkout.get_success_message_text().lower()
    assert not (total_amount > 100000 and "ваш заказ успешно создан" in success_text), \
        f"БАГ ОБНАРУЖЕН: Сумма заказа составляет {total_amount} ₽ (превышает лимит 100 000 ₽), но система позволила успешно оформить заказ!"


@pytest.mark.id("14")
def test_checkout_fields_validation(driver: WebDriver) -> None:
    """Тест на баг: форма принимает некорректные данные в полях оформления заказа без валидации"""
    login_page: LoginPage = LoginPage(driver)
    login_page.login("admin", "admin")
    store: StorePage = StorePage(driver)
    store.add_product_to_cart()
    store.go_to_cart_and_checkout()
    checkout: CheckoutPage = CheckoutPage(driver)
    checkout.fill_order_form("!!!", "123", "@@@", "неверный_адрес", "abc")
    checkout.finish_checkout()
    success_text: str = checkout.get_success_message_text().lower()
    order_created: bool = "ваш заказ успешно создан" in success_text
    assert not order_created, \
        "БАГ ОБНАРУЖЕН: Система позволила успешно оформить заказ с полностью некорректными данными в форме (без валидации)!"