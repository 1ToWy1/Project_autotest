import time
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.login_page import LoginPage
from pages.admin_page import AdminPage


@pytest.mark.id("7")
def test_create_product(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login("admin", "admin")
    admin: AdminPage = AdminPage(driver)
    admin.create_product("Тест Товар", "Описание", "Категория", "1000", "/img/test.png")
    time.sleep(0.5)
    assert "manageProductsPage" in driver.current_url, \
        "Ошибка создания товара: административная панель управления товарами не открылась"


@pytest.mark.id("8")
def test_user_cannot_see_create_product_link(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login("покупатель", "покупатель")
    admin: AdminPage = AdminPage(driver)
    assert not admin.is_create_product_link_visible(), \
        "Ошибка безопасности: обычный покупатель видит ссылку/элементы создания товара"


@pytest.mark.id("9")
def test_edit_product(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login("admin", "admin")
    admin: AdminPage = AdminPage(driver)
    admin.go_to_edit_product()
    assert "editProduct" in driver.current_url, \
        "Ошибка редактирования товара: страница редактирования не была открыта"

    new_title: str = "Обновленный Товар"
    new_price: str = "1500"
    admin.edit_product(new_title, new_price)
    time.sleep(1)
    assert new_title in driver.page_source, \
        f"Ошибка редактирования: название '{new_title}' не отображается на странице"
    assert new_price in driver.page_source, \
        f"Ошибка редактирования: цена '{new_price}' не отображается на странице"


@pytest.mark.id("10")
def test_delete_product(driver: WebDriver) -> None:
    login_page: LoginPage = LoginPage(driver)
    login_page.login("admin", "admin")
    admin: AdminPage = AdminPage(driver)
    unique_product_name: str = "Товар для удаления 123"
    admin.create_product(unique_product_name, "Описание", "Категория", "500", "/img/test.png")
    admin.delete_product_by_name(unique_product_name)
    assert unique_product_name not in driver.page_source, \
        "Ошибка удаления: товар остался на странице и не был удален из DOM"