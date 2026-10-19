from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    EMPTY_CART_MSG = (By.XPATH, "//*[contains(text(), 'в корзине пока пусто')]")
    TOTAL_PRICE = (By.XPATH, "//*[contains(text(), 'Итого:')]")
    CHECKOUT_BTN = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    PLUS_BUTTONS = (By.XPATH, "//span[text()='add']")
    MINUS_BUTTONS = (By.XPATH, "//span[text()='remove']")
    QUANTITY_INPUTS = (By.XPATH, "//input[@type='text' and contains(@class, 'form-control')]")
    ITEM_PRICES = (By.XPATH, "//div[contains(@class, 'text-nowrap') and contains(text(), '₽')]")

    def get_empty_message(self):
        return self.find_element(self.EMPTY_CART_MSG)

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def get_total_text(self):
        element = self.wait.until(EC.visibility_of_element_located(self.TOTAL_PRICE))
        return element.text

    def get_total_price(self):
        raw_text = self.get_total_text()
        digits = "".join(filter(str.isdigit, raw_text))
        return int(digits) if digits else 0

    def click_plus_button(self, index=0):
        buttons = self.wait.until(EC.presence_of_all_elements_located(self.PLUS_BUTTONS))
        buttons[index].click()

    def click_minus_button(self, index=0):
        buttons = self.wait.until(EC.presence_of_all_elements_located(self.MINUS_BUTTONS))
        buttons[index].click()

    def get_item_quantity(self, index=0):
        inputs = self.wait.until(EC.presence_of_all_elements_located(self.QUANTITY_INPUTS))
        return inputs[index].get_attribute("value")

    def get_item_price(self, index=0):
        prices = self.wait.until(EC.presence_of_all_elements_located(self.ITEM_PRICES))
        raw_text = prices[index].text
        digits = "".join(filter(str.isdigit, raw_text))
        return int(digits) if digits else 0
