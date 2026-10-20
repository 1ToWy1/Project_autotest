from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    EMPTY_CART_MSG: tuple[str, str] = (By.XPATH, "//*[contains(text(), 'в корзине пока пусто')]")
    TOTAL_PRICE: tuple[str, str] = (By.XPATH, "//*[contains(text(), 'Итого:')]")
    CHECKOUT_BTN: tuple[str, str] = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    PLUS_BUTTONS: tuple[str, str] = (By.XPATH, "//span[text()='add']")
    MINUS_BUTTONS: tuple[str, str] = (By.XPATH, "//span[text()='remove']")
    QUANTITY_INPUTS: tuple[str, str] = (By.XPATH, "//input[@type='text' and contains(@class, 'form-control')]")
    ITEM_PRICES: tuple[str, str] = (By.XPATH, "//div[contains(@class, 'text-nowrap') and contains(text(), '₽')]")

    def get_empty_message(self) -> WebElement:
        return self.find_element(self.EMPTY_CART_MSG)

    def go_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BTN)

    def get_total_text(self) -> str:
        element: WebElement = self.wait.until(EC.visibility_of_element_located(self.TOTAL_PRICE))
        return element.text

    def get_total_price(self) -> int:
        raw_text: str = self.get_total_text()
        digits: str = "".join(filter(str.isdigit, raw_text))
        return int(digits) if digits else 0

    def click_plus_button(self, index: int = 0) -> None:
        buttons: list[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.PLUS_BUTTONS))
        buttons[index].click()

    def click_minus_button(self, index: int = 0) -> None:
        buttons: list[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.MINUS_BUTTONS))
        buttons[index].click()

    def get_item_quantity(self, index: int = 0) -> str:
        inputs: list[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.QUANTITY_INPUTS))
        return inputs[index].get_attribute("value") or ""

    def get_item_price(self, index: int = 0) -> int:
        prices: list[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.ITEM_PRICES))
        raw_text: str = prices[index].text
        digits: str = "".join(filter(str.isdigit, raw_text))
        return int(digits) if digits else 0
