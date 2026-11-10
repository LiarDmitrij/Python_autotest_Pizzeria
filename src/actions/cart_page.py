import allure
from selenium.webdriver.common.by import By

from src.actions.base import BasePage

CART_URL = 'https://pizzeria.skillbox.cc/cart/'
CART_TABLE = (By.CSS_SELECTOR, 'table.shop_table.cart')
CART_ITEM_NAME = (By.CSS_SELECTOR, '.cart_item td.product-name')
CART_LINK = (By.CSS_SELECTOR, 'a.cart-contents')


class CartPage(BasePage):

    @allure.step("Открыть страницу корзины")
    def open_page(self):
        self.open(CART_URL)
        self.find(CART_TABLE)
        return self

    @allure.step("Перейти в корзину по ссылке в шапке")
    def open_by_header_link(self):
        self.click(CART_LINK)
        self.find(CART_TABLE)
        return self

    @allure.step("Получить названия товаров в корзине")
    def get_item_names(self):
        return [
            item.text.strip()
            for item in self.driver.find_elements(*CART_ITEM_NAME)
        ]