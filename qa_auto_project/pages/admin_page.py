import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages.base_page import BasePage


class AdminPage(BasePage):
    MENU_CREATE_ITEM: tuple[str, str] = (By.XPATH, '//*[@id="offcanvasNavbar"]/div[2]/ul[1]/a')
    MENU_TOGGLE_BTN: tuple[str, str] = (By.XPATH, "/html/body/div/div/nav/div/button/span")
    ADD_PRODUCT_BTN: tuple[str, str] = (By.XPATH, "//button[contains(text(), 'Добавить товар')]")
    NAME_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Наименование']")
    DESC_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Описание']")
    CAT_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Ожидаемая категория']")
    PRICE_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Цена']")
    IMG_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Image Source']")
    SUBMIT_CREATE_BTN: tuple[str, str] = (By.XPATH, "//button[contains(text(), 'Создать товар')]")
    DELETE_BTN: tuple[str, str] = (By.XPATH, "(//button[span[text()='delete']])[last()]")
    EDIT_PRODUCT_LINK: tuple[str, str] = (By.XPATH, "(//a[contains(@href, 'editProduct')])[1]")
    SUBMIT_EDIT_BTN: tuple[str, str] = (By.XPATH, "//*[@id=\"app\"]/div/div/div[1]/div/div[2]/div/button")

    def create_product(self, name: str, desc: str, cat: str, price: str, img: str) -> None:
        self.click(self.MENU_TOGGLE_BTN)
        time.sleep(0.4)
        self.click(self.MENU_CREATE_ITEM)
        self.click(self.ADD_PRODUCT_BTN)
        self.enter_text(self.NAME_INPUT, name)
        self.enter_text(self.DESC_INPUT, desc)
        self.enter_text(self.CAT_INPUT, cat)
        self.enter_text(self.PRICE_INPUT, price)
        self.enter_text(self.IMG_INPUT, img)
        self.click(self.SUBMIT_CREATE_BTN)

    def delete_product(self) -> None:
        self.click(self.MENU_TOGGLE_BTN)
        time.sleep(0.4)
        self.click(self.MENU_CREATE_ITEM)
        delete_btn: WebElement = self.wait.until(EC.element_to_be_clickable(self.DELETE_BTN))
        self.driver.execute_script("arguments[0].click();", delete_btn)

    def go_to_edit_product(self) -> None:
        self.click(self.MENU_TOGGLE_BTN)
        time.sleep(0.4)
        self.click(self.MENU_CREATE_ITEM)
        self.click(self.EDIT_PRODUCT_LINK)
        self.wait.until(EC.url_contains("editProduct"))

    def edit_product(self, new_name: str, new_price: str) -> None:
        name_input: WebElement = self.find_element(self.NAME_INPUT)
        name_input.clear()
        name_input.send_keys(new_name)

        price_input: WebElement = self.find_element(self.PRICE_INPUT)
        price_input.clear()
        price_input.send_keys(new_price)

        self.click(self.SUBMIT_EDIT_BTN)

    def delete_product_by_name(self, product_name: str) -> None:
        self.click(self.MENU_TOGGLE_BTN)
        time.sleep(0.4)
        self.click(self.MENU_CREATE_ITEM)

        xpath: str = f"//div[contains(@class, 'store-card')][.//div[contains(text(), '{product_name}')]]//button[contains(., 'delete')]"
        delete_btn: WebElement = self.find_element((By.XPATH, xpath))
        self.driver.execute_script("arguments[0].click();", delete_btn)
        self.wait.until(EC.staleness_of(delete_btn))

    def is_create_product_link_visible(self) -> bool:
        try:
            self.click(self.MENU_TOGGLE_BTN)
            time.sleep(0.4)
            menu_items: list[WebElement] = self.driver.find_elements(By.XPATH, '//*[@id="offcanvasNavbar"]/div[2]/ul[1]/a')
            if not menu_items or not menu_items[0].is_displayed():
                return False
            self.click(self.MENU_CREATE_ITEM)
            add_btns: list[WebElement] = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Добавить товар')]")
            return len(add_btns) > 0 and add_btns[0].is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False