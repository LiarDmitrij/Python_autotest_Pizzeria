import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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

COD_DESCRIPTION = (By.CSS_SELECTOR, '.payment_box.payment_method_cod p')

ORDER_SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.woocommerce-notice.woocommerce-notice--success')
ORDER_NUMBER = (By.CSS_SELECTOR, '.woocommerce-order-overview__order strong')
ORDER_DATE_RECIEVED = (By.CSS_SELECTOR, '.woocommerce-order-overview__date strong')
ORDER_EMAIL = (By.CSS_SELECTOR, '.woocommerce-order-overview__email strong')
ORDER_TOTAL = (By.CSS_SELECTOR, '.woocommerce-order-overview__total strong')
ORDER_PAYMENT = (By.CSS_SELECTOR, '.woocommerce-order-overview__payment-method strong')
ORDER_ITEM_NAME = (By.CSS_SELECTOR, '.woocommerce-table__product-name.product-name a')
CUSTOMER_ADDRESS = (By.CSS_SELECTOR, '.woocommerce-customer-details address')

CHECKOUT_TOTAL = (By.CSS_SELECTOR, '#order_review .order-total .amount')

SHOW_COUPON_LINK = (By.CSS_SELECTOR, 'a.showcoupon')
COUPON_FORM = (By.CSS_SELECTOR, 'form.checkout_coupon')
COUPON_INPUT = (By.CSS_SELECTOR, 'form.checkout_coupon input#coupon_code')
COUPON_APPLY_BUTTON = (By.CSS_SELECTOR, 'form.checkout_coupon button[name="apply_coupon"]')
COUPON_MESSAGE = (By.CSS_SELECTOR, '.woocommerce-message, .woocommerce-error')
COUPON_DISCOUNT_ROW = (By.CSS_SELECTOR, 'tr.cart-discount .amount')

COUPON_ROW = (By.CSS_SELECTOR, 'tr.cart-discount')
REMOVE_COUPON_LINK = (By.CSS_SELECTOR, 'a.woocommerce-remove-coupon')


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

    @allure.step("Выбрать: Оплата при доставке")
    def select_cod_payment(self):
        self.click(PAYMENT_COD)
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

    @allure.step("Получить дату заказа")
    def get_order_date(self):
        return self.find(ORDER_DATE).get_attribute("value")

    @allure.step("Дождаться описания оплаты при доставке")
    def wait_cod_description(self):
        return self.find(COD_DESCRIPTION)

    @allure.step("Получить текст описания оплаты при доставке")
    def get_cod_description(self):
        return self.find(COD_DESCRIPTION).text.strip()

    @allure.step("Принять условия доставки")
    def accept_terms(self):
        box = self.find(TERMS_CHECKBOX)
        if not box.is_selected():
            box.click()
        return self

    @allure.step("Дождаться страницы подтверждения заказа")
    def wait_order_received(self):
        self.find(ORDER_SUCCESS_MESSAGE)
        return self

    @allure.step("Получить сообщение об успешном заказе")
    def get_success_message(self):
        return self.find(ORDER_SUCCESS_MESSAGE).text.strip()

    @allure.step("Получить дату заказа")
    def get_order_date_received(self):
        return self.find(ORDER_DATE_RECIEVED).text.strip()

    @allure.step("Получить email заказа")
    def get_order_email(self):
        return self.find(ORDER_EMAIL).text.strip()

    @allure.step("Получить сумму заказа")
    def get_order_total(self):
        return self.find(ORDER_TOTAL).text.strip()

    @allure.step("Получить метод оплаты")
    def get_order_payment(self):
        return self.find(ORDER_PAYMENT).text.strip()

    @allure.step("Получить название заказанного товара")
    def get_order_item_name(self):
        return self.find(ORDER_ITEM_NAME).text.strip()

    @allure.step("Получить адрес доставки")
    def get_customer_address(self):
        return self.find(CUSTOMER_ADDRESS).text.strip()

    @allure.step("Получить итоговую сумму заказа на странице оформления")
    def get_checkout_total(self):
        return self.find(CHECKOUT_TOTAL).text.strip()

    @allure.step("Открыть форму ввода купона")
    def show_coupon_form(self):
        self.click(SHOW_COUPON_LINK)
        self.find(COUPON_FORM)
        return self

    @allure.step("Применить купон «{code}»")
    def apply_coupon(self, code):
        self.find(COUPON_INPUT).clear()
        self.find(COUPON_INPUT).send_keys(code)
        self.click(COUPON_APPLY_BUTTON)
        return self

    @allure.step("Дождаться сообщения о применении купона")
    def wait_coupon_message(self):
        return self.find(COUPON_MESSAGE)

    @allure.step("Получить текст сообщения о купоне")
    def get_coupon_message(self):
        return self.find(COUPON_MESSAGE).text.strip()

    @allure.step("Дождаться изменения итоговой суммы")
    def wait_total_changed(self, previous, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(
                *CHECKOUT_TOTAL
            ).text.strip() != previous,
            message="Итоговая сумма не пересчиталась",
        )
        return self.get_checkout_total()

    @allure.step("Получить сумму скидки по купону")
    def get_coupon_discount(self):
        return self.find(COUPON_DISCOUNT_ROW).text.strip()

    @allure.step("Удалить применённый купон, если он есть")
    def remove_coupon_if_present(self):
        if not self.driver.find_elements(*COUPON_ROW):
            return self

        link = self.driver.find_element(*REMOVE_COUPON_LINK)
        href = link.get_attribute("href")
        self.driver.get(href)
        self.find(CHECKOUT_FORM)
        return self
