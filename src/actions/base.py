import logging

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step("Открыть страницу {url}")
    def open(self, url):
        self.logger.info("Открываю страницу: %s", url)
        self.driver.get(url)
        return self

    def find(self, locator):
        self.logger.debug("Ищу элемент: %s", locator)
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def find_all(self, locator):
        self.logger.debug("Ищу элементы: %s", locator)
        return self.wait.until(
            EC.visibility_of_all_elements_located(locator)
        )

    def click(self, locator):
        self.logger.info("Кликаю по элементу: %s", locator)
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()
