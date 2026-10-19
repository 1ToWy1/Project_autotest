import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Generator


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    options: Options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    driver_path: str = os.path.join(base_dir, "..", "chromedriver.exe")

    service: Service = Service(driver_path)

    driver: WebDriver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()
