import logging

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--selenium-browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture()
def selenium(request):
    browser_name = request.config.getoption("--selenium-browser")
    logging.info(f'Prepare {browser_name} browser')

    is_headless = request.config.getoption("--headless")

    options = Options()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,  # убираем сообщение об утечке пароля
    }
    options.add_experimental_option("prefs", prefs)
    options.page_load_strategy = "eager"

    if is_headless:
        options.add_argument("--headless=new")

    if browser_name == "chrome":
        driver = webdriver.Chrome(options=options)
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    logging.info(f'Browser {browser_name} has been started')
    yield driver

    try:
        driver.quit()
        logging.info(f'Browser {browser_name} closed')

    except Exception as e:
        print(f"Ошибка при закрытии браузера (проигнорирована): {e}")


@pytest.fixture
def go_to_url(selenium):
    @allure.step('Открытие страницы {url}')
    def callback(url):
        selenium.get(url)
    return callback
