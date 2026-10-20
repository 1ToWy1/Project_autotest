from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.base_url: str = "http://91.197.96.80/"
        self.driver.implicitly_wait(10)
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    def open(self, path: str = "") -> None:
        self.driver.get(self.base_url + path)

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple[str, str]) -> None:
        element: WebElement = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator: tuple[str, str], text: str) -> None:
        element: WebElement = self.find_element(locator)
        element.click()
        element.clear()
        element.send_keys(text)