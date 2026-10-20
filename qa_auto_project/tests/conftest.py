import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Generator
from pages.login_page import LoginPage


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or edge"
    )


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    browser_name: str = request.config.getoption("--browser").lower()
    base_dir: str = os.path.dirname(os.path.abspath(__file__))

    driver: WebDriver

    if browser_name == "chrome":
        options: ChromeOptions = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver_path: str = os.path.join(base_dir, "..", "chromedriver.exe")
        service: ChromeService = ChromeService(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "edge":
        options: EdgeOptions = webdriver.EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver_path: str = os.path.join(base_dir, "..", "msedgedriver.exe")
        service: EdgeService = EdgeService(driver_path)
        driver = webdriver.Edge(service=service, options=options)
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported. Use 'chrome' or 'edge'.")

    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def admin_driver(driver: WebDriver) -> WebDriver:
    """Фикстура, которая открывает браузер и сразу авторизует администратора."""
    login_page = LoginPage(driver)
    login_page.login("admin", "admin")
    return driver
