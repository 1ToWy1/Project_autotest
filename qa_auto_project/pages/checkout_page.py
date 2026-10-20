from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    NAME_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Имя']")
    SURNAME_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Фамилия']")
    MIDDLE_NAME_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Отчество']")
    ADDRESS_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Адрес доставки']")
    CARD_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Номер карты']")
    TOTAL_PRICE_LOCATOR: tuple[str, str] = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[2]/div[1]")
    SUBMIT_ORDER_BTN: tuple[str, str] = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    FINISH_ORDER_BTN: tuple[str, str] = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div[11]/div/a[2]/button")
    ERROR_MESSAGE_BOX: tuple[str, str] = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/form/div[1]/div[1]")
    SUCCESS_TEXT_ELEMENT: tuple[str, str] = (By.XPATH, "//*[@id='app']/div/div/div[1]/div/div/div[2]")
    SUCCESS_MSG: tuple[str, str] = (By.XPATH, "//*[contains(text(), 'успешно')]")

    def fill_order_form(self, name: str, surname: str, middle_name: str, address: str, card: str) -> None:
        self.enter_text(self.NAME_INPUT, name)
        self.enter_text(self.SURNAME_INPUT, surname)
        self.enter_text(self.MIDDLE_NAME_INPUT, middle_name)
        self.enter_text(self.ADDRESS_INPUT, address)
        self.enter_text(self.CARD_INPUT, card)
        submit_btn: WebElement = self.find_element(self.SUBMIT_ORDER_BTN)
        self.driver.execute_script("arguments[0].click();", submit_btn)

    def click_submit_empty_form(self) -> None:
        submit_btn: WebElement = self.find_element(self.SUBMIT_ORDER_BTN)
        self.driver.execute_script("arguments[0].click();", submit_btn)

    def finish_checkout(self) -> None:
        finish_btn: WebElement = self.find_element(self.FINISH_ORDER_BTN)
        self.driver.execute_script("arguments[0].click();", finish_btn)

    def get_error_message_text(self) -> str:
        return self.find_element(self.ERROR_MESSAGE_BOX).text

    def get_success_message_text(self) -> str:
        return self.find_element(self.SUCCESS_TEXT_ELEMENT).text

    def get_total_price(self) -> int:
        element: WebElement = self.wait.until(
            EC.visibility_of_element_located(self.TOTAL_PRICE_LOCATOR)
        )
        digits: str = "".join(filter(str.isdigit, element.text))
        return int(digits) if digits else 0