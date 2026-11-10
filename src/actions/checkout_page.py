import allure
from selenium.webdriver.common.by import By

from src.actions.base import BasePage

CHECKOUT_URL = 'https://pizzeria.skillbox.cc/checkout/'
CHECKOUT_BUTTON = (
    By.CSS_SELECTOR,
    'a.checkout-button.button.alt.wc-forward',
)
LOGIN_TOGGLE = (By.CSS_SELECTOR, '.woocommerce-form-login-toggle')
LOGIN_INFO = (
    By.CSS_SELECTOR,
    '.woocommerce-form-login-toggle .woocommerce-info',
)
LOGIN_LINK = (
    By.CSS_SELECTOR,
    '.woocommerce-form-login-toggle a.showlogin',
)


class CheckoutPage(BasePage):

    @allure.step("Нажать кнопку «Перейти к оплате»")
    def click_checkout(self):
        self.click(CHECKOUT_BUTTON)
        return self

    @allure.step("Дождаться запроса авторизации")
    def wait_login_request(self):
        return self.find(LOGIN_TOGGLE)

    @allure.step("Получить текст сообщения о необходимости входа")
    def get_login_message(self):
        return self.find(LOGIN_INFO).text.strip()