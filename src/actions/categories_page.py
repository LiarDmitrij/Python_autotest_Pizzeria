import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.actions.base import BasePage

PRODUCT = (By.CSS_SELECTOR, 'li.product')
PRODUCT_FIRST = (By.CSS_SELECTOR, 'li.product.first')
PRODUCT_TITLE = (By.CSS_SELECTOR, 'h3')
PRODUCT_PRICE = (By.CSS_SELECTOR, '.price .amount')
ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '.add_to_cart_button')
ADDED_TO_CART = (By.CSS_SELECTOR, 'a.added_to_cart')

PRICE_SLIDER_MAX_INPUT = (By.CSS_SELECTOR, 'input#max_price')
PRICE_APPLY_BUTTON = (By.CSS_SELECTOR, '.price_slider_wrapper button[type="submit"]')


class CategoriesPage(BasePage):
    TITLE = (By.CSS_SELECTOR, 'h1.product_title')

    @allure.step("Получить название пиццы")
    def get_title(self):
        return self.find(self.TITLE).text.strip()

    @allure.step("Открыть страницу категории {url}")
    def open_page(self, url):
        self.open(url)
        self.find_all(PRODUCT)
        return self

    @allure.step("Применить фильтр цены до {max_price} руб.")
    def filter_by_max_price(self, max_price=135):
        max_input = self.wait.until(
            EC.presence_of_element_located(PRICE_SLIDER_MAX_INPUT)
        )
        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('change'));",
            max_input,
            str(max_price),
        )
        self.click(PRICE_APPLY_BUTTON)
        self.find_all(PRODUCT)
        return self

    @allure.step("Получить цены всех товаров")
    def get_prices(self):
        prices = []
        for product in self.driver.find_elements(*PRODUCT):
            price_text = product.find_element(
                *PRODUCT_PRICE
            ).text.strip()
            prices.append(
                float(
                    price_text.replace("₽", "")
                    .replace(",", ".")
                    .replace("\u00a0", "")
                    .strip()
                )
            )
        return prices

    @allure.step("Получить название первого товара")
    def get_first_product_name(self):
        first_product = self.find(PRODUCT_FIRST)
        return first_product.find_element(
            *PRODUCT_TITLE
        ).text.strip()

    @allure.step("Добавить первый товар в корзину")
    def add_first_to_cart(self):
        first_product = self.find(PRODUCT_FIRST)
        first_product.find_element(*ADD_TO_CART_BUTTON).click()
        self.find_all(ADDED_TO_CART)
        return self

    @allure.step("Открыть «Десерты» с фильтром до {max_price} руб.")
    def open_desserts_filtered(self, max_price=135):
        self.open('https://pizzeria.skillbox.cc/product-category/menu/deserts/')
        self.find_all(PRODUCT)
        self.filter_by_max_price(max_price)
        return self