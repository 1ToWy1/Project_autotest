import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class StorePage(BasePage):
    ADD_TO_CART_BTN = (By.XPATH, "//button[span[text()='add']]")
    PLUS_BTN = (By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div[1]/div[4]/div/button[2]/span')
    CART_ICON_BTN = (By.XPATH, "//*[@id='app']/div/nav/div/a[2]/button/span[1]")
    PROCEED_TO_CHECKOUT_BTN = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[2]/a/button")
    QUANTITY_INPUT = (By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div[1]/div[4]/div/input')
    PRODUCT_PRICE = (By.XPATH, "(//div[contains(text(), '₽')])[1]")

    def add_product_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    def get_product_price_digits(self):
        price_text = self.find_element(self.PRODUCT_PRICE).text
        return price_text.split('.')[0]

    def go_to_cart_and_checkout(self):
        cart_btn = self.find_element(self.CART_ICON_BTN)
        self.driver.execute_script("arguments[0].click();", cart_btn)
        checkout_btn = self.wait.until(EC.element_to_be_clickable(self.PROCEED_TO_CHECKOUT_BTN))
        self.driver.execute_script("arguments[0].click();", checkout_btn)
        self.wait.until(EC.url_contains("checkout"))

    def click_plus_button_multiple_times(self, count):
        for _ in range(count):
            plus_btn = self.find_element(self.PLUS_BTN)
            self.driver.execute_script("arguments[0].click();", plus_btn)
            time.sleep(0.08)

    def go_to_cart(self):
        cart_btn = self.find_element(self.CART_ICON_BTN)
        self.driver.execute_script("arguments[0].click();", cart_btn)
