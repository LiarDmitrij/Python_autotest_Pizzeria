import allure
from selenium.webdriver.common.by import By

from src.actions.base import BasePage

ACCOUNT_URL = 'https://pizzeria.skillbox.cc/my-account/'
ACCOUNT_LINK = (By.XPATH, '//div[@id="menu"]//a[@href="http://pizzeria.skillbox.cc/my-account/"]')
LOGIN_FORM = (By.CSS_SELECTOR, 'form.login')
REGISTER_BUTTON = (By.CSS_SELECTOR, 'button.custom-register-button')


class AccountPage(BasePage):

    @allure.step("Перейти во вкладку «Мой аккаунт»")
    def open_by_header_link(self):
        self.click(ACCOUNT_LINK)
        self.find(LOGIN_FORM)
        return self

    @allure.step("Дождаться загрузки страницы «Мой аккаунт»")
    def wait_account_page(self):
        self.find(LOGIN_FORM)
        return self

    @allure.step("Проверить, что отображается кнопка «Зарегистрироваться»")
    def is_register_button_visible(self):
        return self.find(REGISTER_BUTTON).is_displayed()

    @allure.step("Нажать кнопку «Зарегистрироваться»")
    def click_register(self):
        self.click(REGISTER_BUTTON)
        return self