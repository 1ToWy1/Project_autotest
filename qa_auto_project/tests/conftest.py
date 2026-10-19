import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(base_dir, "..", "chromedriver.exe")

    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()
