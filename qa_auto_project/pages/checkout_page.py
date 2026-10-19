from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage(BasePage):
    NAME_INPUT = (By.XPATH, "//input[@placeholder='Имя']")
    SURNAME_INPUT = (By.XPATH, "//input[@placeholder='Фамилия']")
    MIDDLE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Отчество']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='Адрес доставки']")
    CARD_INPUT = (By.XPATH, "//input[@placeholder='Номер карты']")
    TOTAL_PRICE_LOCATOR = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[1]")
    SUBMIT_ORDER_BTN = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    FINISH_ORDER_BTN = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[2]/button")
    ERROR_MESSAGE_BOX = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[1]")
    SUCCESS_TEXT_ELEMENT = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/div[2]")
    SUCCESS_MSG = (By.XPATH, "//*[contains(text(), 'успешно')]")

    def fill_order_form(self, name, surname, middle_name, address, card):
        self.enter_text(self.NAME_INPUT, name)
        self.enter_text(self.SURNAME_INPUT, surname)
        self.enter_text(self.MIDDLE_NAME_INPUT, middle_name)
        self.enter_text(self.ADDRESS_INPUT, address)
        self.enter_text(self.CARD_INPUT, card)
        submit_btn = self.find_element(self.SUBMIT_ORDER_BTN)
        self.driver.execute_script("arguments[0].click();", submit_btn)

    def click_submit_empty_form(self):
        submit_btn = self.find_element(self.SUBMIT_ORDER_BTN)
        self.driver.execute_script("arguments[0].click();", submit_btn)

    def finish_checkout(self):
        finish_btn = self.find_element(self.FINISH_ORDER_BTN)
        self.driver.execute_script("arguments[0].click();", finish_btn)

    def get_error_message_text(self):
        return self.find_element(self.ERROR_MESSAGE_BOX).text

    def get_success_message_text(self):
        return self.find_element(self.SUCCESS_TEXT_ELEMENT).text

    def get_total_price(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.TOTAL_PRICE_LOCATOR)
        )
        digits = "".join(filter(str.isdigit, element.text))
        return int(digits) if digits else 0
