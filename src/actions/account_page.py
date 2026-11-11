import allure
from selenium.webdriver.common.by import By

from src.actions.base import BasePage

ACCOUNT_URL = 'https://pizzeria.skillbox.cc/my-account/'
ACCOUNT_LINK = (By.XPATH, '//div[@id="menu"]//a[@href="http://pizzeria.skillbox.cc/my-account/"]')
LOGIN_FORM = (By.CSS_SELECTOR, 'form.login')
REGISTER_BUTTON = (By.CSS_SELECTOR, 'button.custom-register-button')

REGISTER_FORM = (By.CSS_SELECTOR, 'form.woocommerce-form-register')
REG_USERNAME = (By.CSS_SELECTOR, 'input#reg_username')
REG_EMAIL = (By.CSS_SELECTOR, 'input#reg_email')
REG_PASSWORD = (By.CSS_SELECTOR, 'input#reg_password')
REG_SUBMIT = (By.CSS_SELECTOR, 'button[name="register"]')

REGISTER_COMPLETE = (By.XPATH, '//div[@class="content-page"]//div[normalize-space(.)="Регистрация завершена"]')

ACCOUNT_NAV = (By.CSS_SELECTOR, 'nav.woocommerce-MyAccount-navigation')
LOGOUT_LINK = (By.CSS_SELECTOR, 'a[href*="customer-logout"]')
ACCOUNT_GREETING = (By.CSS_SELECTOR, '.woocommerce-MyAccount-content p')


class AccountPage(BasePage):

    @allure.step("Перейти во вкладку «Мой аккаунт» не авторизованным")
    def open_by_header_link(self):
        self.click(ACCOUNT_LINK)
        self.find(LOGIN_FORM)
        return self

    @allure.step("Перейти во вкладку «Мой аккаунт» авторизованным")
    def open_by_header_link_auth(self):
        self.click(ACCOUNT_LINK)
        self.find(ACCOUNT_NAV)
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

    @allure.step("Дождаться загрузки формы регистрации")
    def wait_register_form(self):
        self.find(REGISTER_FORM)
        return self

    @allure.step("Заполнить форму регистрации")
    def fill_register_form(self, username, email, password):
        self.find(REG_USERNAME).clear()
        self.find(REG_USERNAME).send_keys(username)
        self.find(REG_EMAIL).clear()
        self.find(REG_EMAIL).send_keys(email)
        self.find(REG_PASSWORD).clear()
        self.find(REG_PASSWORD).send_keys(password)
        return self

    @allure.step("Отправить форму регистрации")
    def submit_register(self):
        self.click(REG_SUBMIT)
        return self

    @allure.step("Дождаться сообщения «Регистрация завершена»")
    def wait_registration_complete(self):
        return self.find(REGISTER_COMPLETE)

    @allure.step("Проверить, что пользователь авторизован")
    def is_logged_in(self):
        navs = self.driver.find_elements(*ACCOUNT_NAV)
        return len(navs) > 0 and navs[0].is_displayed()

    @allure.step("Получить приветствие пользователя")
    def get_greeting(self):
        return self.find(ACCOUNT_GREETING).text.strip()

    @allure.step("Зарегистрировать пользователя {username}")
    def register(self, username, email, password):
        self.open_by_header_link()
        self.click_register()
        self.wait_register_form()
        self.fill_register_form(username, email, password)
        self.submit_register()
        self.wait_registration_complete()
        return self
