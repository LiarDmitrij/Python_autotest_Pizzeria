import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.actions.base import BasePage

BONUS_URL = 'https://pizzeria.skillbox.cc/bonus/'
NAME_INPUT = (By.CSS_SELECTOR, 'input#bonus_username')
PHONE_INPUT = (By.CSS_SELECTOR, 'input#bonus_phone')
SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[name="bonus"]')
BONUS_CONTENT = (By.CSS_SELECTOR, 'div#bonus_content')
BONUS_SUCCESS = (By.CSS_SELECTOR, 'div#bonus_main h3')


class BonusPage(BasePage):

    @allure.step("Открыть страницу бонусной программы")
    def open_page(self):
        self.open(BONUS_URL)
        return self

    @allure.step("Ввести имя: {name}")
    def enter_name(self, name):
        self.find(NAME_INPUT).clear()
        self.find(NAME_INPUT).send_keys(name)
        return self

    @allure.step("Ввести телефон: {phone}")
    def enter_phone(self, phone):
        self.find(PHONE_INPUT).clear()
        self.find(PHONE_INPUT).send_keys(phone)
        return self

    @allure.step("Нажать «Оформить карту»")
    def submit(self):
        self.click(SUBMIT_BUTTON)
        return self

    @allure.step("Принять alert")
    def accept_alert(self):
        self.wait.until(EC.alert_is_present()).accept()
        return self

    @allure.step("Дождаться сообщения об оформлении карты")
    def wait_success(self):
        return self.find(BONUS_SUCCESS)

    @allure.step("Получить текст ошибки валидации")
    def get_validation_error(self):
        return self.find(BONUS_CONTENT).text.strip()

    @allure.step("Проверить, что alert отсутствует")
    def is_alert_absent(self):
        try:
            _ = self.driver.switch_to.alert
            return False
        except Exception:
            return True

    @allure.step("Получить цвет рамки поля «Имя»")
    def get_name_border_color(self):
        return self.find(NAME_INPUT).value_of_css_property(
            "border-color"
        )

    @allure.step("Получить цвет рамки поля «Телефон»")
    def get_phone_border_color(self):
        return self.find(PHONE_INPUT).value_of_css_property(
            "border-color"
        )
