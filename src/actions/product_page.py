import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.actions.base import BasePage

PRODUCT_TITLE = (By.CSS_SELECTOR, 'h1.product_title')
BOARD_SELECT = (By.CSS_SELECTOR, 'select#board_pack')
ADD_TO_CART_SINGLE = (By.CSS_SELECTOR, 'button.single_add_to_cart_button')


class ProductPage(BasePage):

    PIZZA_URL = 'https://pizzeria.skillbox.cc/product/пицца-4-в-1/'

    @allure.step("Открыть страницу пиццы")
    def open_page(self, url):
        self.open(url)
        self.find(PRODUCT_TITLE)
        return self

    @allure.step("Получить название пиццы")
    def get_title(self):
        return self.find(PRODUCT_TITLE).text.strip()

    @allure.step("Выбрать борт «{board}»")
    def select_board(self, board):
        Select(self.find(BOARD_SELECT)).select_by_visible_text(board)
        return self

    @allure.step("Получить выбранный борт")
    def get_selected_board(self):
        return Select(self.find(BOARD_SELECT)).first_selected_option.text.strip()

    @allure.step("Добавить пиццу в корзину")
    def add_to_cart(self):
        self.click(ADD_TO_CART_SINGLE)
        return self
