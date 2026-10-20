from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Логин']")
    PASSWORD_INPUT: tuple[str, str] = (By.XPATH, "//input[@placeholder='Пароль']")
    LOGIN_BUTTON: tuple[str, str] = (By.XPATH, "//button[contains(text(), 'Войти')]")
    MENU_TOGGLE_BTN: tuple[str, str] = (By.XPATH, "/html/body/div/div/nav/div/button/span")
    LOGOUT_BUTTON: tuple[str, str] = (By.XPATH, "/html/body/div/div/nav/div/div[1]/div[2]/ul[4]/li/div")

    def login(self, username: str, password: str) -> None:
        self.open()
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def logout(self) -> None:
        self.click(self.MENU_TOGGLE_BTN)
        self.click(self.LOGOUT_BUTTON)