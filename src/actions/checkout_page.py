import allure
from selenium.webdriver.common.by import By

from src.actions.base import BasePage

CHECKOUT_URL = 'https://pizzeria.skillbox.cc/checkout/'
CHECKOUT_BUTTON = (By.CSS_SELECTOR, 'a.checkout-button.button.alt.wc-forward')
LOGIN_TOGGLE = (By.CSS_SELECTOR, '.woocommerce-form-login-toggle')
LOGIN_INFO = (By.CSS_SELECTOR, '.woocommerce-form-login-toggle .woocommerce-info')
LOGIN_LINK = (By.CSS_SELECTOR, '.woocommerce-form-login-toggle a.showlogin')

CHECKOUT_FORM = (By.CSS_SELECTOR, 'form.checkout')
BILLING_FIRST_NAME = (By.CSS_SELECTOR, 'input#billing_first_name')
BILLING_LAST_NAME = (By.CSS_SELECTOR, 'input#billing_last_name')
BILLING_COUNTRY = (By.CSS_SELECTOR, 'select#billing_country')
BILLING_ADDRESS = (By.CSS_SELECTOR, 'input#billing_address_1')
BILLING_CITY = (By.CSS_SELECTOR, 'input#billing_city')
BILLING_STATE = (By.CSS_SELECTOR, 'input#billing_state')
BILLING_POSTCODE = (By.CSS_SELECTOR, 'input#billing_postcode')
BILLING_PHONE = (By.CSS_SELECTOR, 'input#billing_phone')
BILLING_EMAIL = (By.CSS_SELECTOR, 'input#billing_email')
ORDER_DATE = (By.CSS_SELECTOR, 'input#order_date')
ORDER_COMMENTS = (By.CSS_SELECTOR, 'textarea#order_comments')
PAYMENT_COD = (By.CSS_SELECTOR, 'input#payment_method_cod')
TERMS_CHECKBOX = (By.CSS_SELECTOR, 'input#terms')
PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, 'button#place_order')


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

    @allure.step("Дождаться загрузки формы оформления заказа")
    def wait_checkout_form(self):
        self.find(CHECKOUT_FORM)
        return self

    @allure.step("Заполнить данные доставки")
    def fill_billing(
        self,
        first_name,
        last_name,
        address,
        city,
        state,
        postcode,
        phone,
    ):
        self.find(BILLING_FIRST_NAME).clear()
        self.find(BILLING_FIRST_NAME).send_keys(first_name)
        self.find(BILLING_LAST_NAME).clear()
        self.find(BILLING_LAST_NAME).send_keys(last_name)
        self.find(BILLING_ADDRESS).clear()
        self.find(BILLING_ADDRESS).send_keys(address)
        self.find(BILLING_CITY).clear()
        self.find(BILLING_CITY).send_keys(city)
        self.find(BILLING_STATE).clear()
        self.find(BILLING_STATE).send_keys(state)
        self.find(BILLING_POSTCODE).clear()
        self.find(BILLING_POSTCODE).send_keys(postcode)
        self.find(BILLING_PHONE).clear()
        self.find(BILLING_PHONE).send_keys(phone)
        return self

    @allure.step("Указать дату заказа {order_date}")
    def set_order_date(self, order_date):
        field = self.find(ORDER_DATE)
        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('change'));",
            field,
            order_date,
        )
        return self

    @allure.step("Выбрать оплату при доставке")
    def select_cod_payment(self):
        self.click(PAYMENT_COD)
        return self

    @allure.step("Принять условия доставки")
    def accept_terms(self):
        self.click(TERMS_CHECKBOX)
        return self

    @allure.step("Подтвердить заказ")
    def place_order(self):
        self.click(PLACE_ORDER_BUTTON)
        return self

    @allure.step("Получить значения заполненных полей доставки")
    def get_billing_values(self):
        return {
            "first_name": self.find(BILLING_FIRST_NAME).get_attribute("value"),
            "last_name": self.find(BILLING_LAST_NAME).get_attribute("value"),
            "address": self.find(BILLING_ADDRESS).get_attribute("value"),
            "city": self.find(BILLING_CITY).get_attribute("value"),
            "state": self.find(BILLING_STATE).get_attribute("value"),
            "postcode": self.find(BILLING_POSTCODE).get_attribute("value"),
            "phone": self.find(BILLING_PHONE).get_attribute("value"),
        }