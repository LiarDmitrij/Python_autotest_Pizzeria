import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.actions.base import BasePage

CART_URL = 'https://pizzeria.skillbox.cc/cart/'
CART_TABLE = (By.CSS_SELECTOR, 'table.shop_table.cart')
CART_ITEM = (By.CSS_SELECTOR, '.cart_item')
CART_ITEM_NAME = (By.CSS_SELECTOR, '.cart_item td.product-name')
CART_ITEM_OPTION = (By.CSS_SELECTOR, '.cart_item dl.variation dd.variation- p')
CART_LINK = (By.CSS_SELECTOR, 'a.cart-contents')
CART_ITEM_REMOVE_BUTTON = (By.CSS_SELECTOR, '.cart_item a.remove')
CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, '.cart-empty')
QUANTITY_INPUT = (By.CSS_SELECTOR, '.cart_item input.qty')
UPDATE_CART_BUTTON = (By.CSS_SELECTOR, 'button[name="update_cart"]')
ORDER_TOTAL = (By.CSS_SELECTOR, '.order-total .amount')


class CartPage(BasePage):

    @allure.step("Перейти в корзину по ссылке в шапке")
    def open_by_header_link(self):
        self.find(CART_LINK)
        self.click(CART_LINK)
        self.find(CART_TABLE)
        return self

    @allure.step("Открыть страницу корзины")
    def open_page(self):
        self.open(CART_URL)
        self.find(CART_TABLE)
        return self

    @allure.step("Получить названия товаров в корзине")
    def get_item_names(self):
        return [
            item.text.strip()
            for item in self.driver.find_elements(*CART_ITEM_NAME)
        ]

    @allure.step("Получить опцию в позиции корзины")
    def get_item_option(self):
        return self.find(CART_ITEM_OPTION).text.strip()

    @allure.step("Получить количество в позиции")
    def get_quantity(self):
        return self.find(QUANTITY_INPUT).get_attribute("value")

    @allure.step("Изменить количество на {value}")
    def set_quantity(self, value):
        field = self.find(QUANTITY_INPUT)
        field.clear()
        field.send_keys(str(value))
        return self

    @allure.step("Нажать «Обновить корзину»")
    def click_update(self):
        self.click(UPDATE_CART_BUTTON)
        return self

    @allure.step("Получить итоговую сумму")
    def get_total(self):
        return self.find(ORDER_TOTAL).text.strip()

    @allure.step("Дождаться изменения суммы заказа")
    def wait_total_changed(self, previous, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(
                *ORDER_TOTAL
            ).text.strip() != previous,
            message="Сумма заказа не пересчиталась",
        )
        return self.get_total()

    @allure.step("Удалить позицию из корзины")
    def remove_item(self):
        self.click(CART_ITEM_REMOVE_BUTTON)
        return self

    @allure.step("Дождаться, что позиция удалена")
    def wait_item_removed(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(CART_ITEM),
            message="Позиция не удалилась из корзины",
        )
        return self

    @allure.step("Получить количество позиций в корзине")
    def get_items_count(self):
        return len(self.driver.find_elements(*CART_ITEM))

    @allure.step("Получить сообщение о пустой корзине")
    def get_empty_message(self):
        return self.find(CART_EMPTY_MESSAGE).text.strip()
